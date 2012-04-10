# -*- coding: utf-8 -*-

import sys
import time
import datetime
import logging

from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from django.core.urlresolvers import reverse

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.emitters import Emitter
from haystack.query import SearchQuerySet

from op_api.op.models import *
from op_api.utils import require_permission
from op_api.emitters import OpXMLEmitter, OpLocationXMLEmitter, OpProfessionXMLEmitter, OpEducationLevelXMLEmitter


class LoggingHandler(BaseHandler):
    
    def getlogger(self):
        logger = logging.getLogger()
        hdlr = logging.FileHandler(settings.LOG_FILE)
        formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S') 
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG)
        
        return logger
    
    def debug(self, msg):
        logger = self.getlogger()
        logger.debug(msg)


class SearchHandler(BaseHandler):
    """da rivedere"""
    request_s = ''
    
    def read(self, request, q=None):
        Emitter.register('xml', OpXMLEmitter, 'text/xml; charset=utf-8')
        
        if q:
            if len(q) < 3:
                return { 'warning': 'search key must be longer than 3 characters' }
        
            results = {}
            if ('filter' not in request.GET or
                'filter' in request.GET and request.GET['filter'] == 'politicians'):
            
                politicians = []
                for res in SearchQuerySet().filter(content=q, django_ct='op.oppolitician'):
                    if (res.sex == 'M'):
                        born = 'nato'
                    else:
                        born = 'nata'
                    politicians.append(("%s/op/1.0/politicians/%s" % (settings.SITE_URL, res.pol_id,), "%s, %s a %s il %s" % (res.text, born, res.birth_location, res.birth_date)))
                results['politicians'] = politicians
            
            if ('filter' not in request.GET or
                'filter' in request.GET and request.GET['filter'] == 'locations'):
            
                locations = []
                for res in SearchQuerySet().filter(content=q, django_ct='op.oplocation').models(OpLocation):
                    if  res.location_type != 'Regione':
                        locations.append(("%s/op/1.0/locations/%s" % (settings.SITE_URL, res.location_id,), "%s di %s" % (res.location_type, res.text)))
                    else:
                        locations.append(("%s/op/1.0/locations/%s" % (settings.SITE_URL, res.location_id,), "Regione %s" % (res.text)))
                results['locations'] = locations
                    
            return results
        else:
            return { 'warning': 'empty query will yeld no results' }
    


class LocationHandler(BaseHandler):
    model = OpLocation
    fields = ['id', 'name', 'macroregional_id', 'regional_id', 'provincial_id', 'city_id', 
              'minint_regional_code', 'minint_provincial_code', 'minint_city_code',
              'gps_lat', 'gps_lon', 'inhabitants', ('location_type', ('name',))]
    exclude = ()
    allowed_methods = ('GET')
    base = OpLocation.objects.using('op')
    request_s = ''
    
    @classmethod
    def resource_uri(cls, loc=None):
        loc_id = "id"
        if loc:
            loc_id = loc.id
        return ('api_op_location_detail', [loc_id,])
    
    
    def read(self, request, id=None):
        Emitter.register('xml', OpLocationXMLEmitter, 'text/xml; charset=utf-8')
        
        self.request_s = request.get_full_path().replace('&', '+')
        
        msg = "%s, %s %s, %s, %s" % \
            (time.strftime("%d/%b/%Y %H:%M:%S",time.localtime(time.time())), 
            request.method, self.request_s, request.user.username, request.META['REMOTE_ADDR'])
        
        try:    
            if id:
                return self.base.get(pk=id)
            else:
                locs = cache.get('op_api_' + self.request_s)
                if locs is None:
                    locs = self.base.all()
                    if 'namestartswith' in request.GET:
                      locs = locs.filter((Q(name__istartswith=request.GET['namestartswith']) |                                               Q(alternative_name__istartswith=request.GET['namestartswith']))).order_by('location_type__id', '-inhabitants')
                    if 'name' in request.GET:
                      locs = locs.filter((Q(name=request.GET['name']) | Q(alternative_name=request.GET['name']))).order_by('location_type__id')
                    if 'location_type' in request.GET:
                        location_type = request.GET['location_type']
                        # self.fields.remove(('location_type', ('name', )))
                        if location_type in ('comune', 'provincia', 'regione'):
                            locs = locs.filter(location_type__name__iexact=location_type)
                        else:
                            logger.warning('Wrong location_type: %s. Comune, provincia or regione expected.' % location_type)
                            return None
                        if location_type in ('comune', 'provincia') and 'regional_id' in request.GET:
                            locs = locs.filter(regional_id=request.GET['regional_id'])
                        if location_type == 'comune' and 'provincial_id' in request.GET:
                            locs = locs.filter(provincial_id=request.GET['provincial_id'])
                    if 'limit' in request.GET:
                        locs = locs[:request.GET['limit']]
                    cache.set('op_api_'+self.request_s, locs, 3600)
                    
                return locs
        except self.model.DoesNotExist:
            return None
    


class InstitutionHandler(BaseHandler):
  model = OpInstitution
  fields = ('id', 'name', 'short_name', 'priority')
  allowed_methods = ('GET')
  
  def read(self, request):
    Emitter.register('xml', OpXMLEmitter, 'text/xml; charset=utf-8')
    return OpInstitution.objects.using('op').all()


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
    allowed_methods = ('GET',)
    
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
    
    def read(self, request, id_type, city_id):
        Emitter.register('xml', OpXMLEmitter, 'text/xml; charset=utf-8')
        request_s = request.GET.urlencode().replace('&', '+')
        reps = cache.get('op_api_' + request_s)
        # if reps is None:
        if True:
            reps = self.get_cityreps(id_type, city_id)
            cache.set('op_api_'+request_s, reps, 3600)
        return reps
    
    
    def get_cityreps(self, id_type, city_id):
        """docstring for get_cityreps"""
        reps = {}
        try:
            location = OpLocation.objects.db_manager('op').retrieveFromId(id_type, city_id)
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
    
    


class PoliticianHandler(BaseHandler):
    """docstring for PoliticianHandler"""
    model = OpPolitician
    exclude = ('picture',)
    allowed_methods = ('GET')
    base = OpPolitician.objects.using('op')
    request_s = ''
    
    @classmethod
    def resource_uri(cls, pol=None):
        pol_id = "id"
        if pol:
            pol_id = pol.content_id
        return ('api_op_politician_detail', [pol_id,])
    
    
    def read(self, request, pol_id=None):
        Emitter.register('xml', OpXMLEmitter, 'text/xml; charset=utf-8')
        self.request_s = request.get_full_path().replace('&', '+')        
        try:    
            if pol_id is not None:
                pol = self.base.get(pk=pol_id)
                pol_detail = {
                    'content_id': pol_id,
                    'first_name': pol.first_name,
                    'last_name': pol.last_name,
                    'birth_date': pol.birth_date,
                    'birth_location': pol.birth_location,
                    'profession': pol.profession and pol.profession.getNormalizedDescription(),
                    'resources': pol.getResources(),
                    'education_levels': pol.getEducationLevels(),
                    'institution_charges': {
                        'current': pol.getInstitutionCharges('current'),
                        'past': pol.getInstitutionCharges('past'),
                    },
                    'political_charges': {
                        'current': pol.getPoliticalCharges('current'),
                        'past': pol.getPoliticalCharges('past'),                
                    },
                    'organization_charges': {
                        'current': pol.getOrganizationCharges('current'),
                        'past': pol.getOrganizationCharges('past'),                
                    }
                }
                
                return pol_detail
            else:
                
                if 'namestartswith' in request.GET:
                    members = self.base.filter(
                        Q(last_name__istartswith=request.GET['namestartswith'])
                    )
                    
                    if 'limit' in request.GET:
                        members = members[:request.GET['limit']]
                    
                    pols = []
                    for member in members:
                        api_url = reverse('api_op_politician_detail', args=[member.content_id])
                        member= {
                            'op_id': member.content_id,
                            'first_name': member.first_name,
                            'last_name': member.last_name,
                            'birth_date': member.birth_date,
                            'birt_location': member.birth_location,
                            'op_link': 'http://www.openpolis.it/politico/%s' % member.content_id,
                            'api_link': '%s%s' % (settings.SITE_URL, api_url)
                        }
                        pols.append(member)
                    return pols
                    
                    
                # if no institution, return empty
                if 'institution' in request.GET:
                    institution_name = request.GET['institution']
                elif 'institution_id' in request.GET:
                    institution_id = request.GET['institution_id']
                    institution = OpInstitution.objects.db_manager('op').get(pk=institution_id)
                    institution_name = institution.name
                else:
                    return {'error': 'must specify an institution'}
                
                
                if 'giunta' in institution_name.lower() or 'consiglio' in institution_name.lower():
                    if 'location_id' not in request.GET:
                        return {'error': 'location_id must be specified for this institution'}
                    else:
                        location_id = request.GET['location_id']
                        members = OpInstitutionCharge.objects.db_manager('op').filter(
                            Q(location__id=location_id),
                            Q(institution__name__iexact=institution_name.lower),
                            Q(date_end__isnull=True)
                        ).order_by('charge_type__priority', '-date_end')
                else:
                    members = OpInstitutionCharge.objects.db_manager('op').filter(
                        Q(institution__name__iexact=institution_name.lower),
                        Q(date_end__isnull=True)
                    ).order_by('charge_type__priority', '-date_end')
                
                        
                pols = []
                for member in members:
                    api_url = reverse('api_op_politician_detail', args=[member.politician.content_id])
                    member= {
                        'op_id': member.politician.content_id,
                        'charge': member.charge_type.name,
                        'date_start': member.date_start,
                        'date_end': member.date_end,
                        'party': member.party.getNormalizedAcronymOrName(),
                        'first_name': member.politician.first_name,
                        'last_name': member.politician.last_name,
                        'birth_date': member.politician.birth_date,
                        'birt_location': member.politician.birth_location,
                        'op_link': 'http://www.openpolis.it/politico/%s' % member.politician.content_id,
                        'api_link': '%s%s' % (settings.SITE_URL, api_url),
                        'textual_rep': member.getTextualRepresentation()
                    }
                    pols.append(member)
                return pols
                    
        except self.model.DoesNotExist:
          return None
    


class HistoricHandler(BaseHandler):
    allowed_methods = ('GET')
    
    def read(self, request, id_type, location_id, year=None):
        Emitter.register('xml', OpLocationXMLEmitter, 'text/xml; charset=utf-8')
        try:    
            if 'city_mayor' in request.path:
                return self.get_city_mayor_data(id_type, location_id, year)
            else:
                return self.get_location_government_data(id_type, location_id, year)
            
        except Exception, e:
            return { 'error': e }
    
    
    def get_city_mayor_data(self, id_type, city_id, year=None):
        """docstring for get_city_mayor_data"""
        from django.db import connection
        cursor = connections['op'].cursor()
        data = { 'year': year }
        try:
            location = OpLocation.objects.db_manager('op').retrieveFromId(id_type, city_id)
            if location.location_type.name != 'Comune':
                return { 'exception': 'location is not a city. only cities are accepted' }
            location_prov = location.getProvince()
            location_reg = location.getRegion()
            data['location'] = "%s (%s)" % (location.name, location.prov)
        except Exception, detail:
            return { 'exception': 'location %s, id_type %s could not be found. %s' % (city_id, id_type, detail) }
        
        if year is None:
            ic_mayors = OpInstitutionCharge.objects.db_manager('op').filter(
                location__id=location.id, 
                charge_type__name='Sindaco', 
                date_end__isnull=True
            )
        else:
            ic_mayors = OpInstitutionCharge.objects.db_manager('op').filter(
                Q(location__id=location.id),
                Q(charge_type__name='Sindaco'),
                Q(date_end__gte='%s-01-01'%year) | Q(date_end__isnull=True),
                Q(date_start__lte='%s-12-31'%year)
            )
        
        data['sindaci'] = []
        for ic_mayor in ic_mayors:
            charge_id = ic_mayor.content_id
            sindaco = {
                'date_start': ic_mayor.date_start,
                'date_end': ic_mayor.date_end,
                'party': ic_mayor.party.getNormalizedAcronymOrName(),
                'first_name': ic_mayor.politician.first_name,
                'last_name': ic_mayor.politician.last_name,
                'birth_date': ic_mayor.politician.birth_date,
                'birt_location': ic_mayor.politician.birth_location,
                'op_link': 'http://www.openpolis.it/politico/%s' % ic_mayor.politician.content_id
            }
            data['sindaci'].append(sindaco)
        
        return data
    
    
    def get_location_government_data(self, id_type, location_id, year=None):
        """docstring for get_location_government_data"""
        from django.db import connection
        cursor = connections['op'].cursor()
        data = { 'year': year }
        try:
            location = OpLocation.objects.db_manager('op').retrieveFromId(id_type, location_id)
            if location.location_type.name not in ('Comune', 'Provincia', 'Regione'):
                return { 'exception': 'location is neither a city, province nor a region.' }
            data['location'] = {
                'type': location.location_type.name,
                'name': location.name,
            }
            if location.location_type.name in ('Comune', 'Provincia'):
                data['location']['region'] = location.getRegion().name
            if location.location_type.name == 'Comune':
                data['location']['province'] = location.getProvince().name
                
        except Exception, detail:
            return { 'exception': 'location %s, id_type %s could not be found. %s' % (location_id, id_type, detail) }
        
        if year is None:
            g_members = OpInstitutionCharge.objects.db_manager('op').filter(
                location__id=location.id,
                institution__name__istartswith='giunta',
                date_end__isnull=True
            ).order_by('charge_type__priority', 'politician__last_name')
        else:
            g_members = OpInstitutionCharge.objects.db_manager('op').filter(
                Q(location__id=location.id),
                Q(institution__name__istartswith='giunta'),
                Q(date_end__gte='%s-01-01'%year) | Q(date_end__isnull=True),
                Q(date_start__lte='%s-12-31'%year)
            ).order_by('charge_type__priority', 'politician__last_name')
        
        data['giunta'] = []
        for g_member in g_members:
            member= {
                'charge': g_member.charge_type.name,
                'charge_descr': g_member.description,
                'date_start': g_member.date_start,
                'date_end': g_member.date_end,
                'party': g_member.party.getNormalizedAcronymOrName(),
                'first_name': g_member.politician.first_name,
                'last_name': g_member.politician.last_name,
                'birth_date': g_member.politician.birth_date,
                'birth_location': g_member.politician.birth_location,
                'sex': g_member.politician.sex,
                'op_id': g_member.politician.content_id,
                'op_link': 'http://www.openpolis.it/politico/%s' % g_member.politician.content_id,
                'textual_rep': g_member.getTextualRepresentation()
            }
            data['giunta'].append(member)
        
        if year is None:
            c_members = OpInstitutionCharge.objects.db_manager('op').filter(
                location__id=location.id,
                institution__name__istartswith='consiglio',
                date_end__isnull=True
            ).order_by('charge_type__priority', 'politician__last_name')            
        else:
            c_members = OpInstitutionCharge.objects.db_manager('op').filter(
                Q(location__id=location.id),
                Q(institution__name__istartswith='consiglio'),
                Q(date_end__gte='%s-01-01'%year) | Q(date_end__isnull=True),
                Q(date_start__lte='%s-12-31'%year)
            ).order_by('charge_type__priority', 'politician__last_name')
        
        data['consiglio'] = []
        for c_member in c_members:
            member= {
                'charge': c_member.charge_type.name,
                'date_start': c_member.date_start,
                'date_end': c_member.date_end,
                'party': c_member.party.getNormalizedAcronymOrName(),
                'group': c_member.group.getNormalizedAcronymOrName(),
                'first_name': c_member.politician.first_name,
                'last_name': c_member.politician.last_name,
                'birth_date': c_member.politician.birth_date,
                'birth_location': c_member.politician.birth_location,
                'sex': c_member.politician.sex,
                'op_id': c_member.politician.content_id,
                'op_link': 'http://www.openpolis.it/politico/%s' % c_member.politician.content_id,
                'textual_rep': c_member.getTextualRepresentation()
            }
            data['consiglio'].append(member)
        
        return data
    

