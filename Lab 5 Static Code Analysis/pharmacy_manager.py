"""Manage pharmacy inventory, prescriptions, and stock reports."""

import ast
import hashlib
import hmac
import operator
import os
import secrets
from datetime import date, datetime
from pathlib import Path

# Global pharmacy state
medicines = {}

# Read the password from an environment variable.
DB_PASSWORD = os.environ.get("PHARMACY_DB_PASSWORD")

# Store pharmacy data in the project directory.
STOCK_FILE = Path("pharmacy.json")

# Supported arithmetic operators for dosage calculation.
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def add_medicine(
    name, qty=0, price=0.0, expiry="2099-12-31", audit=None
):
    """Add medicine stock and record the transaction."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a non-empty string.")

    if qty < 0:
        raise ValueError("Quantity added cannot be negative.")

    if price < 0:
        raise ValueError("Price cannot be negative.")

    if audit is None:
        audit = []

    if name not in medicines:
        medicines[name] = {
            "qty": 0,
            "price": price,
            "expiry": expiry,
        }

    medicines[name]["qty"] += qty

    audit.append(
        f"{datetime.now()}: Stocked {qty} units of {name}"
    )
    return audit


def dispense_medicine(name, qty):
    """Dispense medicine and update inventory."""
    if not isinstance(qty, int) or qty <= 0:
        raise ValueError("Dispensed quantity must be a positive integer.")

    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")

    if medicines[name]["qty"] < qty:
        raise ValueError("Insufficient stock.")

    medicines[name]["qty"] -= qty

    if medicines[name]["qty"] == 0:
        del medicines[name]


def get_quantity(name):
    """Return the available quantity of a medicine."""
    return medicines[name]["qty"]


def is_expired(name):
    """Check whether a medicine has expired."""
    expiry = datetime.strptime(
        medicines[name]["expiry"], "%Y-%m-%d"
    ).date()
    return expiry < date.today()


def bill_amount(prescription):
    """Calculate the total bill for a prescription."""
    total = 0.0

    for medicine_name, quantity in prescription:
        if quantity < 0:
            raise ValueError("Prescription quantity cannot be negative.")

        total += medicines[medicine_name]["price"] * quantity

    return total


def calculate_dosage(formula):
    """Evaluate a simple arithmetic expression without eval."""
    try:
        expression = ast.parse(formula, mode="eval").body
    except (SyntaxError, TypeError) as error:
        raise ValueError("Invalid dosage formula.") from error

    def evaluate(node):
        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Division by zero is not allowed.")

            return OPERATORS[type(node.op)](left, right)

        raise ValueError("Only basic arithmetic is permitted.")

    result = evaluate(expression)

    if not isinstance(result, (int, float)):
        raise ValueError("Dosage result must be numeric.")

    return result


def patient_id(name, phone):
    """Create a pseudonymous patient identifier."""
    patient_data = f"{name}{phone}".encode("utf-8")
    return hashlib.sha256(patient_data).hexdigest()


def generate_rx_number():
    """Generate a prescription reference number."""
    return f"RX-{secrets.randbelow(900000) + 100000}"


def save_stock(file=STOCK_FILE):
    """Save inventory as JSON."""
    import json

    with open(file, "w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=4)


def load_stock(file=STOCK_FILE):
    """Load inventory from JSON."""
    import json

    global medicines

    with open(file, "r", encoding="utf-8") as stock_file:
        loaded_medicines = json.load(stock_file)

    if not isinstance(loaded_medicines, dict):
        raise ValueError("Invalid stock data.")

    medicines = loaded_medicines


def print_label(name):
    """Print a medicine label without invoking a shell."""
    if not isinstance(name, str):
        raise TypeError("Medicine name must be a string.")

    print(f"Dispensing label: {name}")


def expiring_soon(days=30):
    """Return medicines expiring within the specified number of days."""
    if days < 0:
        raise ValueError("Days cannot be negative.")

    result = []

    for medicine_name, medicine in medicines.items():
        expiry = datetime.strptime(
            medicine["expiry"], "%Y-%m-%d"
        ).date()

        remaining_days = (expiry - date.today()).days

        if 0 <= remaining_days < days:
            result.append(medicine_name)

    return result


def pharmacist_login(password):
    """Check a pharmacist password against the configured password."""
    if not DB_PASSWORD or not password:
        return False

    return hmac.compare_digest(password, DB_PASSWORD)


def print_stock():
    """Display the current pharmacy inventory."""
    print("===== Pharmacy Stock Report =====")

    for name, medicine in medicines.items():
        print(
            f"{name} -> {medicine['qty']} units, "
            f"Rs. {medicine['price']}, "
            f"exp {medicine['expiry']}"
        )


def main():
    """Run a demonstration of pharmacy operations."""
    medicines.clear()

    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31")

    dispense_medicine("Paracetamol 500mg", 30)

    print(
        "Paracetamol stock:",
        get_quantity("Paracetamol 500mg"),
    )
    print(
        "Amoxicillin expired?",
        is_expired("Amoxicillin 250mg"),
    )
    print(
        "Bill:",
        bill_amount(
            [
                ("Paracetamol 500mg", 10),
                ("Amoxicillin 250mg", 5),
            ]
        ),
    )
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print("Login:", pharmacist_login(DB_PASSWORD or ""))
    print_label("Paracetamol 500mg")

    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()
