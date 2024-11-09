import enum

class OrderDirection(enum.Enum):
    asc: str = "asc"
    desc: str = "desc"

class OrderBy(enum.Enum):
    date_created: str = "date_created"
    date_modified: str = "date_modified"

class DateRangeType(enum.Enum):
    days: str = "days"
    weeks: str = "weeks"
    months: str = "months"