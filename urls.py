from django.conf.urls.defaults import patterns, include, url
# from restfulop.views import LocationTypes, LocationTypeInstance, Locations, LocationInstance


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^op/v1/', include('op_api.op.v1.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

