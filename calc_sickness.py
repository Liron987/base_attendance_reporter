from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class SicknessState:
    day_number: int = 0
    last_sickness_date: date | None = None

def assign_sickness_days(records, state):
    """
    Assign a sickness day number to each sickness record.

    The state persists between monthly files, allowing a sickness
    period to continue across a month boundary.
    """

    for record in records:

        if record["date"] == "תאריך":
            continue

        if record["category"] != "SICKNESS":
            continue

        current_date = record["date"]

        # Continue an existing sickness period if the previous
        # sickness date is immediately before this one.
        if (
            state.last_sickness_date is not None
            and current_date == state.last_sickness_date + timedelta(days=1)
        ):
            state.day_number += 1

        else:
            # Start a new sickness period
            state.day_number = 1

        record["sickness_day"] = state.day_number
        state.last_sickness_date = current_date
