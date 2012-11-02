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


def add_solidity_annotations(reservations):
    """
    Adds a 'solid' parameter to each reservation, specifying whether
    there already were other reservations made by the same user
    when this one was made (and which obviously occurr after the time
    when this booking was made).
    """
    for r in reservations:
        solid_reservations = Reservation.objects.filter(
                user=r.user,
                resource=r.resource,
                start__gt=r.time_created,
                time_created__lt=r.time_created)
        if solid_reservations.count() > 0:
            r.solid = True
        else:
            r.solid = False


def get_reservations(resource_id, start_time, end_time):
    if not resource_id or not start_time or not end_time:
        raise Http404
    start_time = int(start_time)
    end_time = int(end_time)
    resource_id = int(resource_id)
    start_datetime = datetime.fromtimestamp(start_time)
    # We need to add a day to endtime because of djangoisms
    # see https://docs.djangoproject.com/en/dev/ref/models/querysets/#range
    end_datetime = datetime.fromtimestamp(end_time) + timedelta(days=1)
    reservations = Reservation.objects.filter(
            resource=resource_id,
            start__range=(start_datetime, end_datetime))
    add_solidity_annotations(reservations)
    return reservations


def reservations_to_json(reservations):
    return json.dumps([{
        'title': r.user.username,
        'start': calendar.timegm(r.start.timetuple()),
        'end': calendar.timegm(r.end.timetuple())}
        for r in reservations])


def solid_reservations(request, resource_id=None):
    reservations = get_reservations(resource_id, request.GET.get('start'), request.GET.get('end'))
    reservations = filter(lambda x: x.solid, reservations)
    return HttpResponse(reservations_to_json(reservations))


def preliminary_reservations(request, resource_id=None):
    reservations = get_reservations(resource_id, request.GET.get('start'), request.GET.get('end'))
    reservations = filter(lambda x: not x.solid, reservations)
    return HttpResponse(reservations_to_json(reservations))
