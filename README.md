# Attendance Reporter

A Python tool for processing employee attendance reports and extracting **base working hours and salary information** from Excel reports.

The project was created to turn detailed attendance/payroll reports into a clearer calculation of the hours and salary components that should be considered for purposes such as:

* Pension contribution calculations
* Employment percentage (`אחוז משרה`)
* Monthly base working hours
* Monthly base salary
* Analysis of different salary-percentage components
* Verification of employer-provided attendance/payroll calculations

## What it does

The program reads Excel attendance reports from the `input/` directory, processes the records, and writes a calculated report to the `output/` directory.

The main calculation is the extraction of **base hours** from the attendance report.

Attendance reports can contain different payment percentages for different types of hours. For example, an employee may have:

* Regular/base hours
* Hours paid at 125%
* Hours paid at 150%
* Other percentage-based payment components

The program separates the underlying base hours from these payment components and then applies the relevant salary percentages to the calculated base hours.

This makes it possible to determine both:

1. **How many hours were actually base hours**, and
2. **What salary those hours represent after applying the relevant payment percentages.**

From these results, additional information such as monthly base hours, base salary, and employment percentage can be derived.

## Project structure

```text
.
├── attendance_reporter.py
├── add_sum_row.py
├── calc_base_hours.py
├── calc_base_salary.py
├── calc_sickness.py
├── excel_reader.py
├── record_classifier.py
├── xlsx_writer.py
├── input/
│   └── *.xlsx
└── output/
    └── *.xlsx
```

### Modules

**`attendance_reporter.py`**
Main entry point coordinating the processing pipeline.

**`excel_reader.py`**
Reads and extracts the relevant data from Excel attendance reports.

**`record_classifier.py`**
Classifies attendance/payment records according to their characteristics and payment percentages.

**`calc_base_hours.py`**
Calculates the underlying base working hours from the attendance data.

**`calc_base_salary.py`**
Calculates the salary represented by the calculated base hours and their applicable payment percentages.

**`calc_sickness.py`**
Processes sickness-related records and calculations.

**`add_sum_row.py`**
Adds summary/total rows to the generated report.

**`xlsx_writer.py`**
Writes the processed results back to an Excel workbook.

## Input / Output

Place the source attendance reports in:

```text
input/
```

The generated reports are written to:

```text
output/
```

For example:

```text
input/
└── 01-2026.xlsx

output/
└── 01-2026.xlsx
```

The output workbook contains the processed information and calculated values needed for further analysis.

## Why base hours matter

An attendance report may show the total number of hours paid during a month, but the total paid hours are not necessarily equivalent to the number of **base hours**.

For example, if some hours are paid at 125% or 150%, simply adding the displayed paid-hour components can produce a misleading picture of the employee's underlying working time.

This project therefore works backwards from the payment components to identify the underlying base hours and then calculates the corresponding salary.

Conceptually:

```text
Attendance report
        │
        ▼
Extract attendance/payment records
        │
        ▼
Classify records
        │
        ▼
Calculate base hours
        │
        ├───────────────► Employment percentage
        │
        ├───────────────► Monthly base hours
        │
        ▼
Apply payment percentages
        │
        ▼
Calculate base salary
        │
        ▼
Processed Excel report
```

## Example use case

Suppose a monthly report contains hours paid under different percentage categories.

Rather than treating each displayed payment category as an independent amount of working time, the program identifies the underlying base hours and calculates what those hours represent at the applicable salary rates.

This is useful when auditing attendance and payroll data where the distinction between:

* hours worked,
* base hours,
* overtime/payment percentages, and
* the resulting salary

matters.

## Requirements

* Python 3
* Excel `.xlsx` input files
* The Python packages required by the project

Install the required packages with:

```bash
pip install -r requirements.txt
```

> A `requirements.txt` file can be added to the repository once the project's external dependencies are finalized.

## Running

Place an attendance report in the `input/` directory and run:

```bash
python attendance_reporter.py
```

The processed workbook will be written to `output/`.

## Project background

This project started as a practical need to process real-world attendance reports that were difficult to analyze manually.

It also became an opportunity to learn Python after many years of programming primarily in other languages.

The implementation focuses on straightforward data processing rather than introducing a database or a large framework. Excel files are used as the input and output format because they are the format in which the underlying attendance reports are provided and because the resulting calculations can be inspected directly.

## Status

This is a personal, actively developed project.

The calculations are designed around the structure and semantics of the attendance reports the project was created to process, so the program may require adaptation for reports from different employers or payroll systems.
