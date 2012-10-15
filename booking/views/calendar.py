from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from booking.models import Resource

import json


def resource(request, resource_id=None):
    """
    Shows today's bookings for the specified resource.
    """
    if resource_id is None:
        raise Http404
    resource = get_object_or_404(Resource, pk=resource_id)
    context = RequestContext(request, {
        'resource': json.encode(resource)
        })
    return render_to_response('resource.html', context)
