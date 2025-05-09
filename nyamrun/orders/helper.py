from datetime import datetime
from datetime import time as dt_time
from datetime import timedelta


def get_time_choices(place=None):
    now = datetime.now()
    min_time = now + timedelta(minutes=15)
    minute_over = (5 - min_time.minute % 5) % 5
    min_time = min_time + timedelta(minutes=minute_over)
    min_time = min_time.replace(second=0, microsecond=0)

    if place and place.working_hours:
        start_t, end_t, is_overnight = parse_working_hours(place.working_hours)
    else:
        start_t, end_t, is_overnight = dt_time(8, 0), dt_time(22, 0), False

    day = min_time.date()

    if not is_overnight:
        open_from = datetime.combine(day, start_t)
        open_to = datetime.combine(day, end_t)
        if min_time < open_from:
            min_time = open_from
        if min_time > open_to:
            return []
        slots = []
        cur = min_time
        while cur <= open_to:
            slots.append((cur.strftime("%H:%M"), cur.strftime("%H:%M")))
            cur += timedelta(minutes=5)
        return slots
    else:
        open_from = datetime.combine(day, start_t)
        open_to = datetime.combine(day + timedelta(days=1), end_t)  # следующий день!
        if min_time < open_from:
            min_time = open_from
        if min_time > open_to:
            return []
        slots = []
        cur = min_time
        while cur <= open_to:
            slots.append((cur.strftime("%H:%M"), cur.strftime("%H:%M")))
            cur += timedelta(minutes=5)
        return slots


def parse_working_hours(working_hours):
    try:
        start_str, end_str = working_hours.split("-")
        from datetime import time

        start_h, start_m = map(int, start_str.strip().split(":"))
        end_h, end_m = map(int, end_str.strip().split(":"))
        start_time = time(start_h, start_m)
        end_time = time(end_h, end_m)
        is_overnight = end_time <= start_time
        return start_time, end_time, is_overnight
    except Exception:
        from datetime import time

        return time(8, 0), time(22, 0), False
