from django.conf.urls import patterns, url
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication, OAuthAuthentication
from op_api.authentication import TwoLeggedOAuthAuthentication
from op_api.op.handlers import *

auth = HttpBasicAuthentication(realm="Openpolis API")
authoauth = TwoLeggedOAuthAuthentication(realm='Openpolis API')
noauth = None

# switch auth type by changing the 'authentication' parameter below
ad = { 'authentication': auth }


""" piston resources are marked csrf_exempt to ensure the the django
CsrfMiddleware doesn't interfere with POST requests
http://bitbucket.org/jespern/django-piston/issue/82/post-requests-fail-when-using-django-trunk """
class CsrfExemptResource( Resource ):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

historical_resource = Resource(handler=HistoricHandler, **ad)
# politician_shortcuts_resource = Resource(handler=PoliticianShortcutsHandler, **ad)

urlpatterns = patterns('',
    # locations
    url(r'^locations/$', CsrfExemptResource(handler=LocationHandler, **ad), name='api_op_locations_list'),
    url(r'^locations/(?P<id>[^/]+)/$', CsrfExemptResource(handler=LocationHandler, **ad), name='api_op_location_detail'),

    # politicians
    url(r'^politicians/$', CsrfExemptResource(handler=PoliticianHandler, **ad), name='api_op_politicians_list'),
    url(r'^politicians/(?P<pol_id>[^/]+)$', CsrfExemptResource(handler=PoliticianHandler, **ad), name='api_op_politician_detail'),

    # useful to resolve similarities
    # extracts similar politicians, given names and date
    url(r'^similar_politicians/$', CsrfExemptResource(handler=SimilarityHandler, **ad), name='api_op_similar_politicians'),

    # professions
    url(r'^professions/$', CsrfExemptResource(handler=ProfessionHandler, **ad), name='professions_list'),

    # education levels
    url(r'^education_levels/$', CsrfExemptResource(handler=EducationLevelHandler, **ad), name='education_levels_list'),

    # institutions
    url(r'^institutions/$', CsrfExemptResource(handler=InstitutionHandler, **ad), name='institutions_list'),

    # charge types
    url(r'^chargetypes/$', CsrfExemptResource(handler=ChargeTypeHandler, **ad), name='chargetypes_list'),

    # age, gender, profession, education level statistics (takes much time)
    url(r'^statistics/$', Resource(handler=StatisticsHandler, **ad)),

    # api calls used in open_bilanci, to extracts city representatives, mayor or city government, in a given period of time
    url(r'^cityreps/(?P<id_type>[^/]+)/(?P<city_id>[^/]+)/$', Resource(handler=CityrepsHandler, **ad)),

    url(r'^historical_city_mayors/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/$', historical_resource),
    url(r'^historical_city_mayor/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/(?P<year>[^/]+)/$', historical_resource),
    url(r'^historical_location_government/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/(?P<year>[^/]+)/$', historical_resource),    
    url(r'^current_city_mayor/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/$', historical_resource),    
    url(r'^current_location_government/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/$', historical_resource),

    # institution charges with politician links (to op and api)
    # used in open_action to extract decision_makers
    url(r'^decisionmakers/$',
        CsrfExemptResource(handler=InstitutionChargeHandler, **ad), name='api_op_decisionmakers_list'),


)
