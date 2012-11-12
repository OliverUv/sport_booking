# coding=UTF-8
# Line above required to use swedish characters in file

from django.test import TestCase
from django.test import LiveServerTestCase
from django.test.client import Client
from django.utils import timezone
from django.contrib.auth.models import User
from booking.models import ResourceType, Resource, Reservation

from datetime import timedelta


def create_user():
    user_id = User.objects.all().count() + 1
    username = 'user %s' % user_id
    password = 'pass'
    user = User.objects.create_user(username, '%s@test.com' % user_id, password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user


def create_resource_type():
    resource_type_id = ResourceType.objects.all().count() + 1
    resource_type = ResourceType.objects.create()
    resource_type.translate('en')
    resource_type.type_name = 'english resource type name %s' % resource_type_id
    resource_type.general_information = 'english general info for rt %s' % resource_type_id
    resource_type.translate('sv')
    resource_type.type_name = 'swedish resource type name %s' % resource_type_id
    resource_type.general_information = 'swedish general info for rt %s' % resource_type_id
    resource_type.save()
    return resource_type


def create_resource(resource_type):
    resource_id = Resource.objects.filter(resource_type=resource_type).count() + 1
    resource = Resource(resource_type=resource_type)
    resource.longitude = resource_id + 100
    resource.latitude = resource_id + 100
    resource.translate('en')
    resource.name = 'english resource name %s' % resource_id
    resource.specific_information = 'english resource info %s' % resource_id
    resource.translate('sv')
    resource.name = 'swedish resource name %s' % resource_id
    resource.specific_information = 'swedish resource info %s' % resource_id
    resource.save()
    return resource


def create_reservation(user, resource, start, end):
    res = Reservation(user=user, resource=resource, start=start, end=end)
    res.save()
    return res


def later(hours_later):
    return timezone.now() + timedelta(hours=hours_later)


def earlier(hours_earlier):
    return timezone.now() - timedelta(hours=hours_earlier)


def add_test_data():
    user1 = create_user()
    user2 = create_user()
    user3 = create_user()
    user4 = create_user()
    user5 = create_user()

    rest1 = create_resource_type()
    res1 = create_resource(rest1)
    res2 = create_resource(rest1)

    r1 = create_reservation(user1, res1, earlier(2), earlier(1))
    r2 = create_reservation(user1, res1, later(1), later(2))
    r3 = create_reservation(user1, res1, later(3), later(4))

    r4 = create_reservation(user2, res1, earlier(5), earlier(4))
    r5 = create_reservation(user2, res1, later(6), later(7))
    r6 = create_reservation(user2, res1, later(8), later(9))

    r7 = create_reservation(user3, res2, later(1), later(2))
    r8 = create_reservation(user3, res2, later(3), later(4))
    r9 = create_reservation(user3, res2, later(5), later(6))

    r10 = create_reservation(user4, res2, later(7), later(8))

    test_data = {
            'users': [user1, user2, user3, user4, user5],
            'resource_types': [rest1],
            'resources': [res1, res2],
            'reservations': [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]}

    return test_data


class GeneralTests(TestCase):
    def setUp(self):
        self.test_data = add_test_data()
        self.client = Client()
        self.user = self.test_data['users'][4]
        logged_in = self.client.login(username=self.user.username, password='pass')
        self.assertTrue(logged_in)

    def test_ensure_solidness(self):
        r = self.test_data['reservations']
        self.assertTrue(r[0].is_solid())
        self.assertTrue(r[1].is_solid())
        self.assertFalse(r[2].is_solid())

        self.assertTrue(r[3].is_solid())
        self.assertTrue(r[4].is_solid())
        self.assertFalse(r[5].is_solid())

        self.assertTrue(r[6].is_solid())
        self.assertFalse(r[7].is_solid())
        self.assertFalse(r[8].is_solid())

        self.assertTrue(r[9].is_solid())

    def test_fail_new_reservation_in_past(self):
        resource = self.test_data['resources'][1]

        response = self.client.post('/make_reservation/', {
            'start': earlier(2).timetuple(),
            'end': earlier(1).timetuple(),
            'resource_id': resource.id})
        self.assertEqual(response.status_code, 403)


class ManualTests(LiveServerTestCase):
    def setUp(self):
        self.test_data = add_test_data()

    def test_run_test_server_with_test_data(self):
        try:
            raw_input('\nAccepting tests on http://127.0.0.1:8081 until Enter is pressed...\n')
        except EOFError:
            pass
