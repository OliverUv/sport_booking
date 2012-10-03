from django.conf.urls import patterns, include, url


# These two lines enable the admin interface
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sportbooking_frryd.views.home', name='home'),
    # url(r'^sportbooking_frryd/', include('sportbooking_frryd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n'))  # Enables internationalization
)
