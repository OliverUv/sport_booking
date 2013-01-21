# coding=UTF-8
# Line above required to use swedish characters in file

from django.contrib.auth.models import User

from booking.models import ResourceType, Resource, Reservation
from booking.common import utc_now

from datetime import timedelta


def create_user(username):
    username = username
    password = 'pass'
    user = User.objects.create_user(username, '%s@test.com' % username, password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    p = user.profile
    p.postal_number = 58434
    p.phone_number = 0720226044
    p.full_name = 'boop derpatron'
    p.save()

    return user


def create_resource_type(image, name, desc, swe_name, swe_desc):
    resource_type = ResourceType.objects.create()
    resource_type.translate('en')
    resource_type.type_name = name
    resource_type.general_information = desc
    resource_type.image = image
    resource_type.save()
    resource_type.translate('sv')
    resource_type.type_name = swe_name
    resource_type.general_information = swe_desc
    resource_type.save()
    return resource_type


def later(hours_later):
    return utc_now() + timedelta(hours=hours_later)


def create_reservation(user, resource, time):
    start = later(time)
    end = later(time + 1)
    res = Reservation(user=user, resource=resource, start=start, end=end)
    res.save()
    return res


def create_resource(resource_type, longitude, latitude, name, info, swe_name, swe_info):
    resource = Resource(resource_type=resource_type)
    resource.longitude = longitude
    resource.latitude = latitude
    resource.translate('en')
    resource.name = name
    resource.specific_information = info
    resource.save()
    resource.translate('sv')
    resource.name = swe_name
    resource.specific_information = swe_info
    resource.save()
    return resource


def add_initial_data(debug):
    fbf = create_resource_type(
        'resource_type_images/football.png',
        'Football fields',
        'On the football fields you can play as much football as you want. They truly are magical things.',
        'Fotbollsplaner',
        'som man spelar fotboll på :)')
    tns = create_resource_type(
        'resource_type_images/tennis-ball.png',
        'Tennis courts',
        'Where tennis can be played.',
        'Tennisplaner',
        'Där man spelar lite tennis ibland.')
    pol = create_resource_type(
        'resource_type_images/poolball.png',
        'Pool table rooms',
        'Where you can play pool.',
        'Biljardrum',
        'Här kan du spela biljard och ha det trevligt.')
    vol = create_resource_type(
        'resource_type_images/volleyball.png',
        'Volleyball fields',
        'Where you can play volleyball.',
        'Volleybollplaner',
        'Här kan du spela volleyboll!')

    fa = create_resource(fbf, 15.56774, 58.410758, 'Rock', 'a place', 'Sten', 'en plats')
    fb = create_resource(fbf, 15.570261, 58.410134, 'Paper', 'to call', 'Papper', 'att kalla')
    fc = create_resource(fbf, 15.57128, 58.41012, 'Scissors', 'home', 'Sax', 'hem')

    ta = create_resource(tns, 15.559725, 58.412745, 'Leftie', 'take a swing', 'Pumpen', 'svinga')
    tb = create_resource(tns, 15.560272, 58.412891, 'Rightie', 'ding ding dang', 'Pumpen', 'ding dabo dong')

    create_resource(vol, 15.563014, 58.410334, 'BBQ field', 'Just beside [hg] and the central Ryd BBQ grills.', 'Grillplan', 'Ligger precis brevid [hg] och centrala Rydsgrillarna.')

    create_resource(pol, 15.56266, 58.41238, 'Baller room', 'Remember to clean up after yourselves.', 'Balla rummet', 'Glöm inte att städa efter er.')

    if debug:
        a = create_user('baren555')
        b = create_user('helan444')
        c = create_user('booop333')
        d = create_user('sybil829')

        create_reservation(a, fa, 1)
        create_reservation(a, fa, 6)

        create_reservation(a, fb, 3)
        create_reservation(b, fb, 2)

        create_reservation(d, fc, 3)
        create_reservation(c, fc, 4)
        create_reservation(d, fc, 8)
        create_reservation(c, fc, 11)

        create_reservation(c, ta, 5)
        create_reservation(c, ta, 6)
        create_reservation(a, ta, 10)

        create_reservation(c, tb, 1)
        create_reservation(c, tb, 3)
        create_reservation(a, tb, 5)
