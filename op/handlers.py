from piston.handler import BaseHandler
from op_api.op.models import OpLocation, OpProfession, OpInstitutionCharge, OpEducationLevel
from django.db.models import Q
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
    
    try:    
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

        if 'namestartswith' in request.GET:
          return base.filter((Q(name__istartswith=request.GET['namestartswith']) |
                              Q(alternative_name__istartswith=request.GET['namestartswith'])) &
                             Q(location_type__name='comune')).order_by('-inhabitants')
                          
        if 'name' in request.GET:
          return base.get((Q(name=request.GET['name']) | 
                           Q(alternative_name=request.GET['name'])) &
                          Q(location_type__name='comune'))

          
        return base.all()
    except self.model.DoesNotExist:
      return None



class EducationLevelHandler(BaseHandler):
  model = OpEducationLevel
  fields = ('id', 'description', 'oid', 'odescription')
  allowed_methods = ('GET')

  def read(self, request):
    '''
    documentazione per la api education_levels
    '''
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
      return OpProfession.objects.db_manager('op').getBasic().values('id', 'description', 'odescription')
    else:
      return OpProfession.objects.using('op').all()
  
class StatisticsHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        Emitter.register('xml', OpXMLEmitter, 'text/xml; charset=utf-8')
        request_s = request.GET.urlencode().replace('&', '+')
        statistics = cache.get('op_api_' + request_s)
        if  statistics is None:
          statistics = OpInstitutionCharge.objects.db_manager('op').get_statistics(request)
          cache.set('op_api_'+request_s, statistics, 3600)

        return { 'statistics': statistics }

class CityrepsHandler(BaseHandler):
    """docstring for CityrepsHandler"""
    methods_allowed = ('GET',)
    def read(self, request):
        Emitter.register('xml', OpXMLEmitter, 'text/xml; charset=utf-8')
        mutable_qs = request.GET.copy()
        if 'format' in mutable_qs:
            del mutable_qs['format']
        request_s = mutable_qs.urlencode().replace('&', '+')
        reps = cache.get('op_api_' + request_s)
        # if reps is None:
        if True:
            reps = self.get_cityreps(mutable_qs)
            cache.set('op_api_'+request_s, reps, 3600)
        return reps
    
    def get_cityreps(self, qs):
        """docstring for get_cityreps"""
        reps = {}
        try:
            location = OpLocation.objects.db_manager('op').retrieveFromId(qs)
            location_prov = location.getProvince()
            location_reg = location.getRegion()
            reps['location'] = "%s (%s)" % (location.name, location.prov)
        except Exception, detail:
            return { 'exception': 'location could not be found. %s' % detail }
        try:
            reps['europarl'] = location.getNationalReps('eu', location_prov.id)
        except Exception, detail:
            return { 'exception': 'could not extract euro parliament reps. %s' % detail }
        try:
            reps['camera'] = location.getNationalReps('camera', location_prov.id)
        except Exception, detail:
            return { 'exception': 'could not extract camera reps. %s' % detail }

        try:
            reps['senato'] = location.getNationalReps('senato', location_prov.id)
        except Exception, detail:
            return { 'exception': 'could not extract senato reps. %s' % detail }

        reps['regione'] = {}
        try:
            reps['regione']['giunta'] = location_reg.getLocalReps('Giunta Regionale')
            reps['regione']['consiglio'] = location_reg.getLocalReps('Consiglio Regionale')
        except Exception, detail:
            return { 'exception': 'could not extract regional reps. %s' % detail }

        reps['provincia'] = {}
        try:
            reps['provincia']['giunta'] = location_prov.getLocalReps('Giunta Provinciale')
            reps['provincia']['consiglio'] = location_prov.getLocalReps('Consiglio Provinciale')
        except Exception, detail:
            return { 'exception': 'could not extract provincial reps. %s' % detail }

        reps['comune'] = {}
        try:
            reps['comune']['giunta'] = location.getLocalReps('Giunta Comunale')
            reps['comune']['consiglio'] = location.getLocalReps('Consiglio Comunale')
        except Exception, detail:
            return { 'exception': 'could not extract giunta municipal reps. %s' % detail }


        return { 'city_representatives': reps }
    

   