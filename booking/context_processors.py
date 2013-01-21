from django.utils.translation import get_language
from booking.models import ResourceType


def default_values(request):
    '''Add resources that base.html depends on.'''
    language = get_language()
    resource_types = ResourceType.objects.language(language).all()

    return {'base': {
        'in_profile_page': request.path_info.startswith('/profile/'),
        'resource_types': resource_types,
        'language': language}}
