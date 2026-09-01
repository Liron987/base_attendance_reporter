from datetime import datetime, timedelta


def calculate_base_hours(records):

    # Process each attendance record
    for record in records:

        # Skip the header row
        if record["date"] == "תאריך":
            continue

        # Vacation day: the employer recognizes 8.4 base hours
        # Paid absence days are attributed 8.4 base hours
        if record["category"] in ("VACATION", "SICKNESS", "HOLIDAY"):
            record["base_duration"] = timedelta(hours=8, minutes=24)
            record["base_hours"] = 8.40
            continue

        # Only calculate base hours for actual work days
        if record["category"] != "WORK_DAY":
            continue

        # Combine the date and entry time into a datetime
        entry_datetime = datetime.combine(
            record["date"],
            record["entry"]
        )

        # Calculate 9 hours and 10 minutes from the entry time
        calculated_exit = entry_datetime + timedelta(
            hours=9,
            minutes=10
        )

        # Combine the date and actual exit time into a datetime
        exit_datetime = datetime.combine(
            record["date"],
            record["exit"]
        )

        # Handle a shift that crosses midnight
        if exit_datetime < entry_datetime:
            exit_datetime += timedelta(days=1)

        # The base-work period ends at the earlier of:
        # 1. 9:10 after entry
        # 2. Actual exit time
        base_exit = min(calculated_exit, exit_datetime)

        # Store the calculated base-work period
        record["base_entry"] = entry_datetime
        record["base_exit"] = base_exit
        record["base_duration"] = base_exit - entry_datetime

        # Convert the duration to decimal hours, rounded to 2 decimal places
        record["base_hours"] = round(
            record["base_duration"].total_seconds() / 3600,
            2
        )
