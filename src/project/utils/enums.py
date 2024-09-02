from enum import Enum


class WeekDay(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class TimeType(str, Enum):
    # WEEKS = "Weeks"
    DAYS = "days"
    HOURS = "Hours"
    MINUTES = "Minutes"


class OauthProvider(Enum):
    GOOGLE = "GOOGLE"
    ORDINARY_USER = "ORDINARY_USER"
