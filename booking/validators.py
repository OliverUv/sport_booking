from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

import re


def validate_liuid(value):
    if not isinstance(value, basestring):
        raise ValidationError(_("You did not input a valid liu-id."))
    # TODO fix liu-id. Can have 4-5 letters then 3 numbers. \w matches 0-9 so
    # fix it.
    if not re.search(r'\w\w\w\w\w\d\d\d', value) or re.search(r'\w\w\w\w\w', value):
        raise ValidationError(_("You did not input a valid liu-id."))
