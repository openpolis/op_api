from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from op_api.op.handlers import LocationHandler, EducationLevelHandler, ProfessionHandler, StatisticsHandler

location_resource = Resource(handler=LocationHandler)
education_level_resource = Resource(handler=EducationLevelHandler)
profession_resource = Resource(handler=ProfessionHandler)
statistics_resource = Resource(handler=StatisticsHandler)

urlpatterns = patterns('',
    url(r'^locations/$', location_resource),
    url(r'^locations/(?P<id>[^/]+)/$', location_resource), 
    url(r'^regions/$', location_resource),
    url(r'^regions/(?P<regional_id>[^/]+)$', location_resource),
    url(r'^provinces/$', location_resource),
    url(r'^provinces/(?P<provincial_id>[^/]+)$', location_resource),
    url(r'^region_provinces/(?P<regional_id>[^/]+)/$', location_resource),
    url(r'^cities/$', location_resource),
    url(r'^cities/(?P<city_id>[^/]+)$', location_resource),
    url(r'^province_cities/(?P<provincial_id>[^/]+)/$', location_resource),
    url(r'^region_cities/(?P<regional_id>[^/]+)/$', location_resource),
    url(r'^professions/$', profession_resource),
    url(r'^education_levels/$', education_level_resource),
    url(r'^statistics/$', statistics_resource), 
)
