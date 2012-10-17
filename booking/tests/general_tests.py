# coding=UTF-8
# Line above required to use swedish characters in file

from django.utils import unittest
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from booking.models import ResourceType, Resource, Reservation

from datetime import datetime, timedelta


def add_test_data():
    user1 = User()
    user1.username = 'user1'
    # user1.password = 'a'
    user1.set_password('a')
    user1.is_staff = True
    user1.is_superuser = True
    user1.save()

    footballfield = ResourceType.objects.create()
    footballfield.translate('en')
    footballfield.type_name = 'Football field'
    footballfield.general_information = 'general information about football fields'
    footballfield.translate('sv')
    footballfield.type_name = 'Fotbollsplan'
    footballfield.general_information = 'Generell information om fotbollsplan.'
    footballfield.save()

    field1 = Resource.objects.create(resource_type=footballfield, longitude=1, latitude=1)
    field1.translate('en')
    field1.name = 'Field one'
    field1.specific_information = 'Specific information about field one'
    field1.translate('sv')
    field1.name = 'Fält ett'
    field1.specific_information = 'Specifik information om fält ett.'
    field1.save()

    now = datetime.now()
    later = now + timedelta(hours=1)

    res1 = Reservation(user=user1, resource=field1, start=now, end=later)
    res1.save()


class GeneralTests(unittest.TestCase):
    def setUp(self):
        add_test_data()

    def test_ensure_user(self):
        self.assertEqual(1, User.objects.all().count())
        self.assertEqual(1, Reservation.objects.all().count())


class ManualTests(LiveServerTestCase):
    def setUp(self):
        add_test_data()

    def test_run_test_server_with_test_data(self):
        try:
            raw_input('\nAccepting tests on http://127.0.0.1:8081 until key pressed...\n')
        except EOFError:
            pass
