# Lab 6 – Museum Admission

## Overview

This project focuses on testing a museum admission application using Python. The application handles ticket pricing, group discounts, and gallery entry based on visitor details and gallery capacity.

## Objectives

* Understand code coverage and branch coverage.
* Design test cases for different inputs and conditions.
* Test normal cases, boundary conditions, and invalid inputs.
* Measure the effectiveness of test cases using coverage reports.

## Application Features

* **Ticket Pricing:** Calculates admission fees based on visitor category, age, day of the week, and guided tour selection.
* **Group Discounts:** Applies discounts according to group size and group type.
* **Gallery Entry:** Determines whether visitors can enter, queue, or wait based on gallery occupancy and capacity.

## Testing and Coverage

The application is tested using `pytest`, with `coverage.py` used to measure code and branch coverage.

* **Code Coverage:** Measures the proportion of executable statements covered by the tests.
* **Branch Coverage:** Measures whether the possible outcomes of conditional decisions have been exercised.

## Project Files

| File                                              | Description                  |
| ------------------------------------------------- | ---------------------------- |
| `museum_admission.py`                             | Museum admission application |
| `test_museum_admission.py`                        | Initial test cases           |
| `CodeCoverageTest_PES1UG24CS718_application.py`   | Code coverage test cases     |
| `BranchCoverageTest_PES1UG24CS718_application.py` | Branch coverage test cases   |
| `codecoverage.png`                                | Code coverage report         |
| `branchcoverage.png`                              | Branch coverage report       |

## Coverage Results

* **Code Coverage:** 100%
* **Branch Coverage:** 100%

## Conclusion

Code coverage and branch coverage help evaluate how thoroughly an application has been tested. Testing different inputs, boundary conditions, and decision outcomes helps identify potential issues and improve software reliability.
