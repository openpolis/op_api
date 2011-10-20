from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from op_api.op.handlers import *

location_resource = Resource(handler=LocationHandler)
historical_resource = Resource(handler=HistoricHandler)

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
    url(r'^professions/$', Resource(handler=ProfessionHandler)),
    url(r'^education_levels/$', Resource(handler=EducationLevelHandler)),
    url(r'^statistics/$', Resource(handler=StatisticsHandler)), 
    url(r'^cityreps/(?P<id_type>[^/]+)/(?P<city_id>[^/]+)$', Resource(handler=CityrepsHandler)),
    url(r'^politician/(?P<pol_id>[^/]+)$', Resource(handler=PoliticianHandler)),
    url(r'^historical_city_mayor/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/(?P<year>[^/]+)$', historical_resource),    
    url(r'^historical_location_government/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/(?P<year>[^/]+)$', historical_resource),    
)
