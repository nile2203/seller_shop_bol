import uuid
from datetime import datetime

from pytz import timezone


def get_24_char_uuid():
    uid = uuid.uuid4().hex
    for i in range(0, 8):
        uid = uid[:i] + uid[i + 1:]
    return uid.upper()


def get_date_in_ist(date_time):
    ist_tz = timezone('Asia/Calcutta')
    return date_time.astimezone(ist_tz)


def format_datetime_user_friendly(date):
    if not date:
        return ''

    date_object = get_date_in_ist(date)
    return datetime.strftime(date_object, '%d %b,%Y %I:%S %p')
