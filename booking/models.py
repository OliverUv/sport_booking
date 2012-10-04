from django.db import models
from hvad.models import TranslatableModel, TranslatedFields
from validators import validate_liuid


class User(models.Model):
    name = models.CharField(max_length=255)
    postal_number = models.IntegerField()
    phone_number = models.CharField(max_length=40)
    liuid = models.CharField(max_length=8, validators=[validate_liuid])
    registration_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Remark(models.Model):
    time = models.DateField(auto_now_add=True)
    text = models.TextField()
    reservation = models.ForeignKey('Reservation', related_name='remarks', blank=True)
    user = models.ForeignKey(User, related_name='remarks')


class ResourceType(TranslatableModel):
    image = models.ImageField(upload_to='resource_type_images')
    translations = TranslatedFields(
            type_name=models.CharField(max_length=255),
            general_information=models.TextField(blank=True))


class Resource(TranslatableModel):
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    translations = TranslatedFields(
            name=models.CharField(max_length=255),
            specific_information=models.TextField())


class Reservation(models.Model):
    resource = models.ForeignKey(Resource, related_name='reservations')
    user = models.ForeignKey(User, related_name='reservations')
    start = models.DateTimeField()
    end = models.DateTimeField()
