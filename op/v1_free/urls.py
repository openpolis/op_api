from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from op_api.op.handlers import *

historical_resource = Resource(handler=HistoricHandler)

urlpatterns = patterns('',
    url(r'^locations/$', Resource(handler=LocationHandler), name='api_location_detail'),
    url(r'^locations/(?P<id>[^/]+)/$', Resource(handler=LocationHandler), name='api_location_detail'),
    url(r'^professions/$', Resource(handler=ProfessionHandler)),
    url(r'^education_levels/$', Resource(handler=EducationLevelHandler)),
    url(r'^statistics/$', Resource(handler=StatisticsHandler)), 
    url(r'^cityreps/(?P<id_type>[^/]+)/(?P<city_id>[^/]+)$', Resource(handler=CityrepsHandler)),
    url(r'^politician/(?P<pol_id>[^/]+)$', Resource(handler=PoliticianHandler)),
    url(r'^historical_city_mayor/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/(?P<year>[^/]+)$', historical_resource),    
    url(r'^historical_location_government/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/(?P<year>[^/]+)$', historical_resource),    
    url(r'^current_location_government/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)$', historical_resource),    
)
