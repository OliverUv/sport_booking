from booking.models import UserProfile, Remark, ResourceType, Resource, Reservation
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Used instead of admin.ModelAdmin for translated models.
# Does not support inline/list etc stuff.
from hvad.admin import TranslatableAdmin


class ResourceTypeAdmin(TranslatableAdmin):
    pass


class ResourceAdmin(TranslatableAdmin):
    pass


# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):  # Define a new User admin
    inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Remark)
admin.site.register(ResourceType, ResourceTypeAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Reservation)
