from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from datetime import datetime, timedelta
from booking.common import get_object_or_404
from booking.models import Reservation

from booking.models import Resource
import json
import calendar


def resource(request, resource_id=None):
    """
    Shows today's bookings for the specified resource.
    """
    if resource_id is None:
        raise Http404
    resource = get_object_or_404(Resource, resource_id)
    context = RequestContext(request, {
        'resource': {'id': resource.id,
                    'name': resource.name}})

    return render_to_response('resource.html', context)


def add_color_annotations(user, reservations):
    """
    Adds colors to reservations so that they are represented correctly
    to the user.
    """
    background_colors = {
            'own': {'solid': '#1e90ff', 'preliminary': '#afeeee'},
            'other': {'solid': '#b22222', 'preliminary': '#f4a460'},
            }

    text_colors = {
            'own': {'solid': '#ffffff', 'preliminary': '#000000'},
            'other': {'solid': '#ffffff', 'preliminary': '#000000'},
            }

    for r in reservations:
        display_as = 'other'
        if user.is_authenticated() and user == r.user:
            display_as = 'own'

        r_status = 'solid' if r.is_solid() else 'preliminary'

        r.bg_color = background_colors[display_as][r_status]
        r.text_color = text_colors[display_as][r_status]


def get_reservations(request, resource_id):
    start_time = int(request.GET.get('start'))
    end_time = int(request.GET.get('end'))
    resource_id = int(resource_id)
    if not resource_id or not start_time or not end_time:
        raise Http404

    start_datetime = datetime.fromtimestamp(start_time)
    # We need to add a day to endtime because of djangoisms
    # see https://docs.djangoproject.com/en/dev/ref/models/querysets/#range
    end_datetime = datetime.fromtimestamp(end_time) + timedelta(days=1)
    reservations = Reservation.objects.filter(
            resource=resource_id,
            start__range=(start_datetime, end_datetime))
    add_color_annotations(request.user, reservations)

    return HttpResponse(reservations_to_json(reservations))


def reservations_to_json(reservations):
    return json.dumps([{
        'title': r.user.username,
        'start': calendar.timegm(r.start.timetuple()),
        'end': calendar.timegm(r.end.timetuple()),
        'color': r.bg_color,
        'textColor': r.text_color}
        for r in reservations])
