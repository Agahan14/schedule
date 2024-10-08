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
    DAYS = "days"
    HOURS = "Hours"
    MINUTES = "Minutes"


class BookingStatus(str, Enum):
    CONFIRMED = "confirmed"
    UNCONFIRMED = "unconfirmed"
    CANCELED = "canceled"
    PAST = "past"


class OauthProvider(Enum):
    GOOGLE = "GOOGLE"
    ORDINARY_USER = "ORDINARY_USER"
