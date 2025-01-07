from datetime import datetime


def transform_date_strings(start_date: str, end_date: str) -> (int, str):
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    interval = (end_date_obj - start_date_obj).days
    start_day = start_date_obj.day
    start_month = start_date_obj.strftime("%b")
    end_day = end_date_obj.day
    end_month = end_date_obj.strftime("%b")

    return interval, f"{start_day} {start_month} - {end_day} {end_month}"
