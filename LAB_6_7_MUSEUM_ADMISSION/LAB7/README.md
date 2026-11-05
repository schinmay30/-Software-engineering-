# Lab 7 - Fuzz Testing

This lab continues the Museum Admission application work from Lab 6.

## Deliverables
- processor.py - Fixed application
- test_processor.py - Hypothesis-based fuzz tests
- screenshots/ - Initial, failing, fixed and passing test evidence
- Lab7_Report.pdf - Report containing screenshots and observations

## Workflow
1. Run the original buggy application.
2. Write Hypothesis tests for all three functions.
3. Identify bugs using failing tests.
4. Fix the application.
5. Run the fixed application.
6. Verify that all tests pass.
7. Prepare the PDF report.

## Dependencies
Install dependencies:

python -m pip install -r requirements.txt

## Run
python processor.py
python -m pytest -v test_processor.py
