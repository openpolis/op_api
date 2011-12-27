from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication, OAuthAuthentication
from op_api.authentication import TwoLeggedOAuthAuthentication
from op_api.op.handlers import *

auth = HttpBasicAuthentication(realm="Openpolis API")
authoauth = TwoLeggedOAuthAuthentication(realm='Openpolis API')
noauth = None

# switch auth type by changing the 'authentication' parameter below
ad = { 'authentication': noauth }


""" piston resources are marked csrf_exempt to ensure the the django
CsrfMiddleware doesn't interfere with POST requests
http://bitbucket.org/jespern/django-piston/issue/82/post-requests-fail-when-using-django-trunk """
class CsrfExemptResource( Resource ):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

historical_resource = Resource(handler=HistoricHandler, **ad)

urlpatterns = patterns('',
    url(r'^locations/$', CsrfExemptResource(handler=LocationHandler, **ad), name='api_location_detail'),
    url(r'^locations/(?P<id>[^/]+)/$', CsrfExemptResource(handler=LocationHandler, **ad), name='api_location_detail'),
    url(r'^professions/$', CsrfExemptResource(handler=ProfessionHandler, **ad)),
    url(r'^education_levels/$', CsrfExemptResource(handler=EducationLevelHandler, **ad)),
    url(r'^statistics/$', Resource(handler=StatisticsHandler, **ad)), 
    url(r'^cityreps/(?P<id_type>[^/]+)/(?P<city_id>[^/]+)$', Resource(handler=CityrepsHandler, **ad)),
    url(r'^politician/(?P<pol_id>[^/]+)$', CsrfExemptResource(handler=PoliticianHandler, **ad)),
    url(r'^historical_city_mayor/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/(?P<year>[^/]+)$', historical_resource),    
    url(r'^historical_location_government/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)/(?P<year>[^/]+)$', historical_resource),    
    url(r'^current_location_government/(?P<id_type>[^/]+)/(?P<location_id>[^/]+)$', historical_resource),    
)
