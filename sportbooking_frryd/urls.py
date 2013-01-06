from django.conf import settings
from django.conf.urls import patterns, include, url


# These two lines enable the admin interface
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sportbooking_frryd.views.home', name='home'),
    # url(r'^sportbooking_frryd/', include('sportbooking_frryd.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^accounts/login/$', 'django_cas.views.login', name='login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout', name='logout'),
    url(r'^$', 'booking.views.general.start', name='start'),
    url(r'^resource/(?P<resource_id>\d+)/$', 'booking.views.booking_calendar.resource', name='resource'),
    url(r'^reservations/(?P<resource_id>\d+)/$', 'booking.views.booking_calendar.get_reservations', name='reservations'),
    url(r'^make_reservation/$', 'booking.views.booking_calendar.make_reservation', name='make_reservation'),
    url(r'^delete_reservation/$', 'booking.views.booking_calendar.delete_reservation', name='delete_reservation'),
    url(r'^single_click_reservation/$', 'booking.views.booking_calendar.single_click_reservation', name='single_click_reservation'),

    url(r'^i18n/', include('django.conf.urls.i18n'))  # Enables internationalization
)

if settings.DEBUG:
    # media files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
