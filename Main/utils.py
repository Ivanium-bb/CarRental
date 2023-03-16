from Main.consts import *


def validate_date(session_start, session_finish):
    if session_finish <= session_start:
        return False, finish_before
    count_days = (session_finish - session_start).days
    if count_days >= 30:
        return False, long_period
    if session_finish.weekday() > 4:
        return False, finish_we
    elif session_start.weekday() > 4:
        return False, start_we
    return True, "success"
