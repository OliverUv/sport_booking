from django.db import models
from hvad.models import TranslatableModel, TranslatedFields
from validators import validate_liuid

# Create your models here.
class User(TranslatableModel):
    name = models.CharField(max_lenght=255, validators=[validate_liuid])
    liuid = models.CharField()
