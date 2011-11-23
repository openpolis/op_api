from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from op_api.op.handlers import *

historical_resource = Resource(handler=HistoricHandler)

urlpatterns = patterns('',
    url(r'^search/$', Resource(handler=SearchHandler), name='api_search'),
    url(r'^locations/$', Resource(handler=LocationHandler), name='api_locations_list'),
    url(r'^locations/(?P<id>[^/]+)/$', Resource(handler=LocationHandler), name='api_location_detail'),
    url(r'^politician/(?P<pol_id>[^/]+)$', Resource(handler=PoliticianHandler)),
    url(r'^politicians/$', Resource(handler=PoliticianHandler), name='api_politicians_list'),
    url(r'^politicians/(?P<pol_id>[^/]+)/$', Resource(handler=PoliticianHandler), name='api_politician_detail'),
    url(r'^institutions/$', Resource(handler=InstitutionHandler), name='api_institutions_list'),
    url(r'^professions/$', Resource(handler=ProfessionHandler), name='api_professions_list'),
    url(r'^education_levels/$', Resource(handler=EducationLevelHandler), name='api_education_levels_list'),
    url(r'^statistics/$', Resource(handler=StatisticsHandler)), 
    url(r'^cityreps/(?P<id_type>[^/]+)/(?P<city_id>[^/]+)$', Resource(handler=CityrepsHandler)),
    url(r'^historical_city_mayor/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/(?P<year>[^/]+)$', historical_resource),    
    url(r'^historical_location_government/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/(?P<year>[^/]+)$', historical_resource),    
    url(r'^current_location_government/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)$', historical_resource),    
)
