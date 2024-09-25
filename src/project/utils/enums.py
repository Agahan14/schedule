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


default_work_schedule = [
    {"day_of_week": "Monday", "time_from": "09:00", "time_to": "17:00"},
    {"day_of_week": "Tuesday", "time_from": "09:00", "time_to": "17:00"},
    {"day_of_week": "Wednesday", "time_from": "09:00", "time_to": "17:00"},
    {"day_of_week": "Thursday", "time_from": "09:00", "time_to": "17:00"},
    {"day_of_week": "Friday", "time_from": "09:00", "time_to": "17:00"},
    {"day_of_week": "Saturday", "time_from": "09:00", "time_to": "17:00"},
    {"day_of_week": "Sunday", "time_from": "09:00", "time_to": "17:00"}
]
