from datetime import date, time

def get_hourly_rate(record_date):
    """
    Return the applicable hourly salary rate for a given date.
    """

    if record_date < date(2025, 1, 1):
        return 38

    return 42

def time_to_decimal_hours(value):
    """
    Convert an Excel time value to decimal hours.

    Supported formats:
    - datetime.time
    - Excel numeric time fraction
    - HH:MM string
    """

    if value is None:
        return None

    # Native Python time object
    if isinstance(value, time):
        return (
            value.hour
            + value.minute / 60
            + value.second / 3600
        )

    # Excel stores time numerically as a fraction of a day
    if isinstance(value, (int, float)):
        return value * 24

    # String representation such as "07:16"
    if isinstance(value, str):
        value = value.strip()

        hours, minutes = value.split(":")

        return int(hours) + int(minutes) / 60

    raise TypeError(
        f"Unsupported time value type: {type(value).__name__}"
    )

def calculate_night_premium(record, hourly_rate):
    """
    Calculate the additional 25% night-shift premium.

    A shift beginning after 22:00 receives an additional
    25% for up to the first 7 base hours.
    """

    base_hours = record.get("base_hours")
    night_125 = record["percentages"].get("לילה 125%")

    if base_hours is None or night_125 is None:
        return 0

    night_hours = time_to_decimal_hours(night_125)

    if night_hours is None or night_hours <= 0:
        return 0

    # The premium applies to at most the first 7 base hours
    premium_hours = min(base_hours, 7)

    return round(
        premium_hours * 0.25 * hourly_rate,
        2
    )


def calculate_base_salary(record, hourly_rate):
    """
    Calculate the base salary from the available salary components.

    The calculated base hours are filled sequentially according
    to the salary-component order. Each component is multiplied
    by its applicable salary multiplier.

    לילה 125% is intentionally excluded for now.
    """

    base_hours = record.get("base_hours")

    if base_hours is None:
        return {
            "base_salary": None,
            "night_premium": 0
        }

    # reference category
    category = record.get("category")

    # Determine whether the attendance report contains
    # any actual percentage-based hours.
    has_percentage_data = any(
        time_to_decimal_hours(value) not in (None, 0)
        for value in record["percentages"].values()
    )

    # Unworked vacation or holiday:
    # pay the calculated base hours at the normal hourly rate.
    if category in ("VACATION", "HOLIDAY") and not has_percentage_data:
        return {
            "base_salary": round(
                base_hours * hourly_rate,
                2
            ),
            "night_premium": 0
        }

    if category == "SICKNESS":
        sickness_day = record.get("sickness_day")

        if sickness_day == 1:
            multiplier = 0.00
        elif sickness_day in (2, 3):
            multiplier = 0.50
        else:
            multiplier = 1.00

        return {
            "base_salary": round(
                base_hours * hourly_rate * multiplier,
                2
            ),
            "night_premium": 0
        }

    salary_components = [
        ("100%", 1.00),
        ("125%", 1.25),
        ("150%", 1.50),
        ("לילה 125%", 1.25),
        ("לילה 150%", 1.50),
        ("שעות שבת/חג 150%", 1.50),
        ("שעות שבת/חג 175%", 1.75),
        ("שעות שבת/חג 200%", 2.00),
    ]

    remaining_hours = base_hours
    salary = 0

    for column_name, multiplier in salary_components:

        # Stop once all base hours have been accounted for
        if remaining_hours <= 0:
            break

        value = record["percentages"].get(column_name)

        # Missing/empty percentage column
        if value is None:
            continue

        available_hours = time_to_decimal_hours(value)

        if available_hours is None:
            continue

        # Use only the portion still required to reach
        # the calculated base hours.
        usable_hours = min(
            available_hours,
            remaining_hours
        )

        salary += (
            usable_hours
            * multiplier
            * hourly_rate
        )

        remaining_hours -= usable_hours

    night_premium = calculate_night_premium(
        record,
        hourly_rate
    )

    return {
        "base_salary": round(salary + night_premium, 2),
        "night_premium": night_premium if night_premium != 0 else None
    }
