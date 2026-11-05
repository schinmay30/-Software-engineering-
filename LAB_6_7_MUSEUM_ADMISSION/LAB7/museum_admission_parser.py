from datetime import date
import re


def format_visitor_name(name):
    """
    Formats a full name as 'Surname, Given names' for the ticket.
    """
    if not isinstance(name, str):
        raise TypeError("Name must be a string")

    parts = name.split()

    if not parts:
        raise ValueError("Name cannot be empty")

    return parts[-1].title() + ', ' + ' '.join(parts[:-1]).title()


def parse_group_ages(text):
    """
    Parses space-separated ages into a list of integers.
    """
    if not isinstance(text, str):
        raise TypeError("Ages must be provided as a string")

    try:
        return [int(age) for age in text.split()]
    except ValueError:
        raise ValueError("All ages must be whole numbers")


def parse_visit_date(text):
    """
    Parses a valid YYYY-MM-DD date into a (year, month, day) tuple.
    """
    if not isinstance(text, str):
        raise TypeError("Date must be a string")

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text.strip()):
        raise ValueError("Date must use YYYY-MM-DD format")

    try:
        parsed = date.fromisoformat(text.strip())
        return parsed.year, parsed.month, parsed.day
    except ValueError:
        raise ValueError("Invalid calendar date")


def main():
    print("==== Running format_visitor_name ====")
    value = input("Enter a visitor's full name (e.g. asha rao): ")
    print("Name on ticket:", format_visitor_name(value))

    print("\n==== Running parse_group_ages ====")
    value = input("Enter the ages in the group separated by spaces (e.g. 34 12 70): ")
    print("Group ages:", parse_group_ages(value))

    print("\n==== Running parse_visit_date ====")
    value = input("Enter the visit date as YYYY-MM-DD (e.g. 2026-11-05): ")
    print("Visit date (year, month, day):", parse_visit_date(value))


if __name__ == "__main__":
    main()
