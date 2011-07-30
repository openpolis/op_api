from piston.handler import BaseHandler
from op_api.op.models import OpLocation, OpProfession, OpInstitutionCharge, OpEducationLevel
from piston.emitters import Emitter
from op_api.emitters import OpXMLEmitter, OpLocationXMLEmitter, OpProfessionXMLEmitter, OpEducationLevelXMLEmitter
from django.core.cache import cache

class LocationHandler(BaseHandler):
  model = OpLocation
  fields = ('id', 'name', 'macroregional_id', 'regional_id', 'provincial_id', 'city_id', 'inhabitants', ('location_type', ('name',)))
  allowed_methods = ('GET')

  def read(self, request, id=None, regional_id=None, provincial_id=None, city_id=None):
    Emitter.register('xml', OpLocationXMLEmitter, 'text/xml; charset=utf-8')

    base = OpLocation.objects.using('op')
    if id:
      return base.get(pk=id)
    else:
      if 'region_cities' in request.path:
        return base.filter(location_type__name__iexact='comune', regional_id=regional_id)
      if 'province_cities' in request.path:
        return base.filter(location_type__name__iexact='comune', provincial_id=provincial_id)
        
      if '/cities' in request.path:
        if city_id:
          return base.filter(location_type__name__iexact='comune', city_id=city_id)
        else:
          return base.filter(location_type__name__iexact='comune')

      if 'region_provinces' in request.path:
        return base.filter(location_type__name__iexact='provincia', regional_id=regional_id)
        
      if '/provinces' in request.path:
        if provincial_id:
          return base.filter(location_type__name__iexact='provincia', provincial_id=provincial_id)
        else:
          return base.filter(location_type__name__iexact='provincia')
          
      if '/regions' in request.path:
        if  regional_id:
          return base.filter(location_type__name__iexact='regione', regional_id=regional_id)
        else:
          return base.filter(location_type__name__iexact='regione')
      else:
        return base.all()



class EducationLevelHandler(BaseHandler):
  model = OpEducationLevel
  fields = ('id', 'description', 'oid', 'odescription')
  allowed_methods = ('GET')

  def read(self, request):
    Emitter.register('xml', OpEducationLevelXMLEmitter, 'text/xml; charset=utf-8')

    if 'type' in request.GET and request.GET['type'] == 'basic':
      return OpEducationLevel.objects.db_manager('op').getBasic().values('id', 'description')
    else:
      return OpProfession.objects.using('op').all()

class ProfessionHandler(BaseHandler):
  model = OpProfession
  fields = ('id', 'description', 'oid', 'odescription')
  allowed_methods = ('GET')

  def read(self, request):
    Emitter.register('xml', OpProfessionXMLEmitter, 'text/xml; charset=utf-8')
    
    if 'type' in request.GET and request.GET['type'] == 'basic':
      return OpProfession.objects.db_manager('op').getBasic().values('id', 'odescription')
    else:
      return OpProfession.objects.using('op').all()
  
class StatisticsHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        Emitter.register('xml', OpXMLEmitter, 'text/xml; charset=utf-8')
        request_s = request.GET.urlencode().replace('&', '+')
        statistics = cache.get('op_api_' + request_s)
        if  statistics==None:
          statistics = OpInstitutionCharge.objects.db_manager('op').get_statistics(request)
          cache.set('op_api_'+request_s, statistics, 3600)

        return { 'statistics': statistics }
