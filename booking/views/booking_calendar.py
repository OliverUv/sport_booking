from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from datetime import timedelta

from booking.common import get_object_or_404
from booking.models import Reservation
from booking.models import Resource
from booking.common import to_timestamp, from_timestamp, utc_now
from booking.common import http_forbidden, http_badrequest, http_json_response


def resource(request, resource_id=None):
    """
    Shows today's bookings for the specified resource.
    """
    if resource_id is None:
        return http_badrequest(_('No resource id given.'))
    resource = get_object_or_404(Resource, resource_id)
    context = RequestContext(request, {
        'resource': {'id': resource.id,
                    'name': resource.name}})

    return render_to_response('resource.html', context)


def add_reservation_annotations(user, reservations):
    """
    Adds colors to reservations so that they are represented correctly
    to the user.
    """
    background_colors = settings.CALENDAR_COLORS['background']
    text_colors = settings.CALENDAR_COLORS['text']

    for r in reservations:
        display_as = 'other'
        r.is_own = False
        if user.is_authenticated() and user == r.user:
            display_as = 'own'
            r.is_own = True

        r_status = 'solid' if r.is_solid() else 'preliminary'

        r.bg_color = background_colors[display_as][r_status]
        r.text_color = text_colors[display_as][r_status]


def get_reservations(request, resource_id):
    start_time = int(request.GET.get('start'))
    end_time = int(request.GET.get('end'))
    resource_id = int(resource_id)
    if not resource_id or not start_time or not end_time:
        return http_badrequest('')

    start_datetime = from_timestamp(start_time)
    # We need to add a day to endtime because of djangoisms
    # see https://docs.djangoproject.com/en/dev/ref/models/querysets/#range
    end_datetime = from_timestamp(end_time) + timedelta(days=1)
    reservations = Reservation.objects.filter(
            deleted=False,
            resource=resource_id,
            start__range=(start_datetime, end_datetime))
    add_reservation_annotations(request.user, reservations)

    return http_json_response(reservations_to_json_struct(reservations))


def reservations_to_json_struct(reservations):
    return [{
        'title': r.user.username,
        'is_own': r.is_own,
        'id': r.id,
        'start': to_timestamp(r.start),
        'end': to_timestamp(r.end),
        'color': r.bg_color,
        'textColor': r.text_color}
        for r in reservations]


def do_make_reservation(start, end, resource_id, user):
    interval = end - start
    max_interval = timedelta(hours=settings.MAX_RESERVATION_LENGTH)
    if (interval > max_interval):
        return http_forbidden(_('You may not reserve the resource for such a long time.'))

    now = utc_now()
    if (now > start) or (now > end):
        return http_forbidden(_('Start and end times must be in the future.'))

    if not (start < end):
        return http_forbidden(_('Start time must be before end time.'))

    outstanding_reservations = Reservation.objects.filter(
            deleted=False,
            user=user,
            end__gt=now,
            resource=resource_id).count()

    if outstanding_reservations > 1:
        return http_forbidden(_('You may only make two reservations per resource.'))

    possibly_concurrent_reservations = Reservation.objects.filter(
            deleted=False,
            user=user,
            end__gt=now)
    concurrent_reservations = filter(lambda r: r.would_overlap(start, end), possibly_concurrent_reservations)
    if len(concurrent_reservations) > 0:
        return http_forbidden(_('You may not reserve two resources at the same time.'))

    possibly_overlapping_reservations = Reservation.objects.filter(
            deleted=False,
            end__gt=now,
            resource=resource_id)

    # Check if solid reservations prevent this one to be made
    # Or if preliminary reservations prevent a preliminary reservation
    # from being made.
    for r in possibly_overlapping_reservations:
        if r.would_overlap(start, end):
            if outstanding_reservations > 0:
                return http_forbidden(_("You can't override a reservation with a preliminary reservation."))
            elif r.is_solid():
                return http_forbidden(_('Somebody has already made a reservation here!'))

    # Mark overriden preliminary bookings as deleted.
    for r in possibly_overlapping_reservations:
        if r.would_overlap(start, end):
            r.delete_and_report()

    r = Reservation(user=user, start=start, end=end)
    r.resource_id = resource_id
    r.save()

    return http_json_response({'status': 'success', 'id': r.id})


@login_required
def single_click_reservation(request):
    ts = request.POST.get('timestamp', None)
    resource_id = request.POST.get('resource_id', None)
    if None in [ts, resource_id]:
        return http_badrequest('')

    start = from_timestamp(int(ts))
    start = start.replace(minute=0)
    end = start + timedelta(hours=1)

    return do_make_reservation(start, end, resource_id, request.user)


@login_required
def delete_reservation(request):
    r_id = request.POST.get('id', None)
    if r_id is None:
        return http_badrequest(_('No request id provided.'))
    r = list(Reservation.objects.filter(id=int(r_id)))
    for reservation in r:
        if request.user.id != reservation.user_id:
            return http_forbidden(_('You may only delete your own events.'))
    for reservation in r:
            reservation.delete_and_report()

    return http_json_response({'status': 'success', 'deleted': len(r)})


@login_required
def make_reservation(request):
    start = request.POST.get('start', None)
    end = request.POST.get('end', None)
    resource_id = request.POST.get('resource_id', None)

    if None in [start, end, resource_id]:
        return http_badrequest('')

    start = from_timestamp(int(start))
    end = from_timestamp(int(end))
    resource_id = int(resource_id)

    return do_make_reservation(start, end, resource_id, request.user)
