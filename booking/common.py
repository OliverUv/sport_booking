from django.http import Http404
from django.utils.translation import get_language


def get_object_or_404(object_type, key):
    language = get_language()
    if language not in ['en', 'sv']:
        language = 'en'

    obj = object_type.objects.language(language).get(pk=key)
    if obj is None:
        raise Http404
    return obj
