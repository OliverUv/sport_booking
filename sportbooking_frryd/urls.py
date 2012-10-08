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

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    url(r'^i18n/', include('django.conf.urls.i18n'))  # Enables internationalization
)
