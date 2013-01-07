from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

import re

liu_id_regex = r'[a-z]{4,5}\d{3}'


def is_valid_liuid(value):
    if value is None:
        return False
    if not isinstance(value, basestring):
        return False
    if not re.search(liu_id_regex, value):
        return False
    return True


def validate_liuid(value):
    if not is_valid_liuid(value):
        raise ValidationError(_("You did not input a valid liu-id."))
