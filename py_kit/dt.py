import datetime

STANDARD_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def now():
    return datetime.datetime.now().strftime(STANDARD_TIME_FORMAT)


def dt2str(dt: datetime.datetime):
    return dt.strftime(STANDARD_TIME_FORMAT)
