from django.http import Http404
from django.utils.translation import get_language
from pytz import timezone
from datetime import datetime

import calendar
import pytz

SV = timezone('Europe/Stockholm')
UTC = pytz.utc


def get_object_or_404(object_type, key):
    language = get_language()
    if language not in ['en', 'sv']:
        language = 'en'

    obj = object_type.objects.language(language).get(pk=key)
    if obj is None:
        raise Http404
    return obj


def to_timestamp(datetime):
    calendar.timegm(datetime.timetuple())


def from_timestamp(timestamp):
    UTC.localize(datetime.utcfromtimestamp(timestamp))


def as_local_time(time):
    return SV.normalize(time.astimezone(SV))


def as_utc_time(time):
    return UTC.normalize(time.astimezone(UTC))
