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

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'booking.views.general.logout', name='logout'),
    url(r'^$', 'booking.views.general.start', name='start'),
    url(r'^resource/(?P<resource_id>\d+)/$', 'booking.views.calendar.resource', name='resource'),
    url(r'^solid-reservations/(?P<resource_id>\d+)/$', 'booking.views.calendar.solid_reservations', name='solid-reservations'),
    url(r'^preliminary-reservations/(?P<resource_id>\d+)/$', 'booking.views.calendar.preliminary_reservations', name='preliminary-reservations'),

    url(r'^i18n/', include('django.conf.urls.i18n'))  # Enables internationalization
)
