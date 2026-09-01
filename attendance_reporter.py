import os

from datetime import datetime

from excel_reader import read_attendance
from calc_base_hours import calculate_base_hours
from xlsx_writer import export_xlsx
from calc_sickness import SicknessState, assign_sickness_days

# Directory containing the attendance reports

input_directory = "input"


# Make sure the output directory exists

os.makedirs("output", exist_ok=True)

employment_end_date = datetime.strptime(
    "13.04.2026",
    "%d.%m.%Y"
).date()

# prepare to count sickness days in a row
sickness_state = SicknessState()

# Process every Excel file in the input directory
for filename in sorted(os.listdir(input_directory)):

    # Only process XLSX files
    if not filename.lower().endswith(".xlsx"):
        continue

    input_file = os.path.join(
        input_directory,
        filename
    )

    print(f"Processing {input_file}")

    # Read attendance data from Excel

    records = read_attendance(
        input_file,
        employment_end_date
    )

    # Calculate base hours according to entry and exit
    calculate_base_hours(records)

    # remember sickness days
    assign_sickness_days(
        records,
        sickness_state
    )

    # Export the processed records

    output_file = export_xlsx(records, input_file)

    print(f"Created {output_file}")
