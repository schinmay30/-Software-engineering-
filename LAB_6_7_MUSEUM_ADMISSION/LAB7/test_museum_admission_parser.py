import pytest
from datetime import date
from hypothesis import given, strategies as st

from museum_admission_parser import (
    format_visitor_name,
    parse_group_ages,
    parse_visit_date
)


# TEST 1: Visitor name formatting
@given(
    st.lists(
        st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1),
        min_size=2,
        max_size=5
    )
)
def test_format_visitor_name_valid(words):
    name = " ".join(words)
    expected = words[-1].title() + ", " + " ".join(words[:-1]).title()
    assert format_visitor_name(name) == expected


@pytest.mark.parametrize("value", ["", "   ", None])
def test_format_visitor_name_invalid(value):
    with pytest.raises((ValueError, TypeError)):
        format_visitor_name(value)


# TEST 2: Group age parsing
@given(st.lists(st.integers(), min_size=1, max_size=10))
def test_parse_group_ages_valid(ages):
    text = " ".join(map(str, ages))
    assert parse_group_ages(text) == ages


@pytest.mark.parametrize("value", ["12 abc", "12 5x", None])
def test_parse_group_ages_invalid(value):
    with pytest.raises((ValueError, TypeError)):
        parse_group_ages(value)


# TEST 3: Visit date parsing
@given(st.dates())
def test_parse_visit_date_valid(d):
    assert parse_visit_date(d.isoformat()) == (
        d.year, d.month, d.day
    )


@pytest.mark.parametrize(
    "value",
    ["2026-99-99", "2026-02-30", "abc", "", None]
)
def test_parse_visit_date_invalid(value):
    with pytest.raises((ValueError, TypeError)):
        parse_visit_date(value)
