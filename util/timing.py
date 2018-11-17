from datetime import date, datetime

import copy
import math

# Calculates the current week, based on term start and end
def get_week(term_start, term_end):
    # Split dates, convert each of day / month / year to int
    start_tokens = list(map(int, term_start.split('/')))[::-1]
    end_tokens = list(map(int, term_end.split('/')))[::-1]

    if len(start_tokens) != 3:
        raise Error('Term start date incorrectly formatted')

    if len(end_tokens) != 3:
        raise Error('Term end date incorrectly formatted')

    # Convert to date objects
    start = date(*start_tokens)
    end = date(*end_tokens)

    # Get today's date, check if it's outside the term
    today = date.today()

    if (end - today).total_seconds() < 0:
        return -1
    if (today - start).total_seconds() < 0:
        return -1

    # Use a timedelta to figure out how many weeks are elapsed, and
    # return that
    return int(math.floor((today - start).days/7))

# Gets the current day and time
def get_day_time():
    now = datetime.now()
    return (now.weekday(), now.hour)

# Extracts a class from a timetable, given week, day and time. Also
# injects additional information
def extract_class(timetable, week, day, time):
    for cls in timetable["classes"]:
        if week in convert_range(cls["weeks"]):
            rg = convert_range(cls["time"])
            if day == int(cls["day"]) and time in rg:
                ret = copy.deepcopy(cls)
                start = rg[0]
                if len(rg) == 1:
                    end = rg[0]
                else:
                    end = rg[1]
                ret["is_start"] = start == time
                ret["duration"] = (end - start) + 1
                return ret
    return None


# Converts a range string into a list of values
def convert_range(range_str):
    ret = []
    ranges = range_str.split(',')
    for r in ranges:
        if '-' in r:
            s = r.split('-')
            ret += list(range(int(s[0]), int(s[1])+1))
        else:
            ret.append(int(r))
    return ret
