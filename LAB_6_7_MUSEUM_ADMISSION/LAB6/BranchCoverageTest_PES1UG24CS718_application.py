import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# Ticket price tests
def test_adult_weekday():
    assert ticket_price("adult", 30, "tuesday", False) == 300

def test_student_monday():
    assert ticket_price("student", 20, "monday", False) == 75

def test_child_below_five():
    assert ticket_price("child", 4, "tuesday", False) == 0

def test_senior_weekend():
    assert ticket_price("senior", 65, "saturday", False) == 250

def test_sunday_ticket():
    assert ticket_price("adult", 30, "sunday", False) == 350

def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200

def test_adult_guided_tour():
    assert ticket_price("adult", 30, "tuesday", True) == 400

def test_weekend_guided_tour():
    assert ticket_price("adult", 30, "saturday", True) == 450

def test_invalid_category():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("vip", 30, "tuesday", False)

def test_negative_age():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)

def test_age_exactly_five():
    assert ticket_price("child", 5, "tuesday", False) == 100


# Group discount tests
def test_small_group():
    assert group_discount(4, False) == 0

def test_invalid_group_size():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)

def test_school_group_at_twenty():
    assert group_discount(20, True) == 40

def test_school_group_below_twenty():
    assert group_discount(19, True) == 25

def test_non_school_group_at_fifteen():
    assert group_discount(15, False) == 20

def test_non_school_group_at_eight():
    assert group_discount(8, False) == 10

def test_non_school_group_below_eight():
    assert group_discount(7, False) == 0


# Gallery entry tests
def test_gallery_at_capacity():
    assert gallery_entry(100, 100, False) == "wait"

def test_gallery_above_capacity():
    assert gallery_entry(110, 100, False) == "wait"

def test_gallery_ninety_percent_without_timed_slot():
    assert gallery_entry(90, 100, False) == "queue"

def test_gallery_ninety_percent_with_timed_slot():
    assert gallery_entry(90, 100, True) == "enter"

def test_gallery_below_ninety_percent():
    assert gallery_entry(89, 100, False) == "enter"

def test_gallery_with_zero_capacity():
    assert gallery_entry(0, 0, False) == "wait"
