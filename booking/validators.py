from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

import re

liu_id_regex = r'[a-z]{4,5}\d{3}'


def validate_liuid(value):
    if not isinstance(value, basestring):
        raise ValidationError(_("You did not input a valid liu-id."))
    if not re.search(liu_id_regex, value):
        raise ValidationError(_("You did not input a valid liu-id."))
