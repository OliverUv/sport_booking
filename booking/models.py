from django.db import models
from hvad.models import TranslatableModel, TranslatedFields
from validators import validate_liuid


# Create your models here.
class User(TranslatableModel):
    name = models.CharField(max_lenght=255)
    postal_number = models.IntegerField()
    phone_number = models.CharField(max_length=40)
    liuid = models.CharField(max_lenght=8, validators=[validate_liuid])

    def __unicode__(self):
        return self.name
