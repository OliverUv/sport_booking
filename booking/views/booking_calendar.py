from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from datetime import timedelta

from booking.common import get_object_or_404
from booking.models import Reservation, ResourceType, Resource, OverwriteLog
from booking.common import to_timestamp, from_timestamp, utc_now
from booking.common import http_forbidden, http_badrequest, http_json_response


def resource(request, resource_id=None):
    """
    Shows bookings for the specified resource.
    """
    if resource_id is None:
        return http_badrequest(_('No resource id given.'))
    mobile_requested = request.path_info.startswith('/m/')
    language = get_language()
    resources = Resource.objects.language(language).all()
    resource = get_object_or_404(Resource, resource_id)
    context = RequestContext(request, {
        'mobile_requested': mobile_requested,
        'resource': resource,
        'resources': resources})

    return render_to_response('resource.html', context)


def resource_type(request, resource_t_id=None):
    """
    Shows bookings for the specified resource type.
    """
    if resource_t_id is None:
        return http_badrequest(_('No resource type id given.'))

    resource_type = get_object_or_404(ResourceType, resource_t_id)
    resources = list(resource_type.resources.all())
    # Sort resources by longitude so that calendar columns correspond to
    # the map shown above them.
    resources = sorted(resources, key=lambda r: r.longitude)
    min_lat = min(resources, key=lambda r: r.latitude)
    max_lat = max(resources, key=lambda r: r.latitude)
    min_long = min(resources, key=lambda r: r.longitude)
    max_long = max(resources, key=lambda r: r.longitude)

    # Calculate margins and calendar widths
    resource_count = len(resources)
    total_width = 100
    width_sans_margins = 58.2
    margin_width = total_width - width_sans_margins

    cal_width = width_sans_margins / resource_count
    cal_margin = margin_width / (resource_count - 1)

    context = RequestContext(request, {
        'longitude': (max_long.longitude + min_long.longitude) / 2,
        'latitude': (max_lat.latitude + min_lat.latitude) / 2,
        'cal_width': cal_width,
        'cal_margin': cal_margin,
        'resource_type': resource_type,
        'resources': resources})

    return render_to_response('resource_type.html', context)


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

        r.solidity = 'solid' if r.is_solid() else 'preliminary'

        r.bg_color = background_colors[display_as][r.solidity]
        r.text_color = text_colors[display_as][r.solidity]


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
    reservations = filter(lambda r: r.valid_user(), reservations)
    add_reservation_annotations(request.user, reservations)

    return http_json_response(reservations_to_json_struct(reservations))


def reservations_to_json_struct(reservations):
    return [{
        'title': r.user.username,
        'is_own': r.is_own,
        'id': r.id,
        'start': to_timestamp(r.start),
        'end': to_timestamp(r.end),
        'solidity': r.solidity,
        'color': r.bg_color,
        'textColor': r.text_color}
        for r in reservations]


def do_make_reservation(start, end, resource_id, user):
    if not user.profile.completed():
        return http_forbidden(_('You must complete your profile before making reservations.'))
    if user.profile.is_banned:
        return http_forbidden(_('You are banned. Stated reason: ') + user.profile.ban_reason + _(' Contact FRRyd for further information.'))

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
    possibly_concurrent_reservations = filter(lambda r: r.valid_user(), possibly_concurrent_reservations)
    concurrent_reservations = filter(lambda r: r.would_overlap(start, end), possibly_concurrent_reservations)
    if len(concurrent_reservations) > 0:
        return http_forbidden(_('You may not reserve two resources at the same time.'))

    possibly_overlapping_reservations = Reservation.objects.filter(
        deleted=False,
        end__gt=now,
        resource=resource_id)
    possibly_overlapping_reservations = filter(lambda r: r.valid_user(), possibly_overlapping_reservations)

    # Check if solid reservations prevent this one to be made
    # Or if preliminary reservations prevent a preliminary reservation
    # from being made.
    for r in possibly_overlapping_reservations:
        if r.would_overlap(start, end):
            if outstanding_reservations > 0:
                return http_forbidden(_("You can't overwrite a reservation with a preliminary reservation."))
            elif r.is_solid():
                return http_forbidden(_('Somebody has already made a reservation here!'))

    # Mark overwriten preliminary bookings as deleted.
    overwritten_reservations = []
    for r in possibly_overlapping_reservations:
        if r.would_overlap(start, end):
            r.delete_and_report()
            overwritten_reservations.append(r)

    new_reservation = Reservation(user=user, start=start, end=end)
    new_reservation.resource_id = resource_id
    new_reservation.save()

    # Document overwritten reservations
    for r in overwritten_reservations:
        doc_object = OverwriteLog(
            deleted_reservation=r,
            replacing_reservation=new_reservation)
        doc_object.save()

    return http_json_response({'status': 'success', 'id': new_reservation.id})


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
def overwrite_reservation(request):
    r_id = request.POST.get('id', None)
    if r_id is None:
        return http_badrequest(_('No request id provided.'))
    r = list(Reservation.objects.filter(id=int(r_id)))
    if len(r) < 1:
        return http_badrequest(_('No reservation with that id.'))
    reservation = r[0]

    if request.user.id == reservation.user_id:
        return http_forbidden(_('You may not overwrite your own reservations.'))
    elif reservation.is_solid():
        return http_forbidden(_('You may not overwrite solid reservations.'))

    # Dispatch to do_make_reservation which does all necessary testing for
    # overwrites anyway.
    return do_make_reservation(reservation.start, reservation.end, reservation.resource_id, request.user)


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
