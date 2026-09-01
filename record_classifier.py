def classify_record(record):

    # Weekend
    if record["type"] == 'סופ"ש':
        return "WEEKEND"

    # Holiday
    if record["type"] == "חג":
        if record["weekday_he"] == "ש":
            return "WEEKEND"
        return "HOLIDAY"

    # Sick day
    if record["event"] == "מחלה":
        return "SICKNESS"

    # Vacation day
    if record["event"] == "חופש":
        return "VACATION"

    # Work day
    if record["entry"] is not None and record["exit"] is not None:
        return "WORK_DAY"

    # Anything we haven't classified yet
    return "OTHER"
