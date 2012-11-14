from django.contrib.auth.models import User
from django.db import models
from hvad.models import TranslatableModel, TranslatedFields
from validators import validate_liuid

from booking.common import utc_now


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    postal_number = models.IntegerField()
    phone_number = models.CharField(max_length=40)
    liuid = models.CharField(max_length=8, validators=[validate_liuid])
    registration_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username


class Remark(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    reservation = models.ForeignKey('Reservation', related_name='remarks', blank=True)
    user = models.ForeignKey(User, related_name='remarks')

    def __unicode__(self):
        return self.user


class ResourceType(TranslatableModel):
    image = models.ImageField(upload_to='resource_type_images', blank=True)
    translations = TranslatedFields(
            type_name=models.CharField(max_length=255),
            general_information=models.TextField(blank=True))

    def __unicode__(self):
        return self.safe_translation_getter('type_name', 'ResourceType: %s' % self.pk)


class Resource(TranslatableModel):
    resource_type = models.ForeignKey(ResourceType, related_name='resources')
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    translations = TranslatedFields(
            name=models.CharField(max_length=255),
            specific_information=models.TextField())

    def __unicode__(self):
        return self.safe_translation_getter('name', 'Resource: %s' % self.pk)


class Reservation(models.Model):
    resource = models.ForeignKey(Resource, related_name='reservations')
    user = models.ForeignKey(User, related_name='reservations')
    time_created = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return '%s booking' % [self.user.username]

    def is_solid(self):
        if self.start < utc_now():
            return True

        conflicting_reservations = Reservation.objects.filter(
                user=self.user,
                resource=self.resource,
                start__lt=self.start,
                start__gt=utc_now())
        return conflicting_reservations.count() == 0
