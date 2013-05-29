# -*- coding: utf-8 -*-

import time
import logging

from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from django.core.urlresolvers import reverse

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.emitters import Emitter

from op_api.op.models import *
from op_api.emitters import OpXMLEmitter, OpLocationXMLEmitter, OpProfessionXMLEmitter, OpEducationLevelXMLEmitter
from op_api.utils import set_query_parameter


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


class LocationHandler(BaseHandler):
    model = OpLocation
    fields = ['id', 'name', 'prov', 'slug', 'macroregional_id', 'regional_id', 'provincial_id', 'city_id',
              'minint_regional_code', 'minint_provincial_code', 'minint_city_code',
              'gps_lat', 'gps_lon', 'inhabitants', ('location_type', ('name',)), 'date_start', 'date_end', 'new_location_id']
    exclude = ()
    allowed_methods = ('GET')
    base = OpLocation.objects.using('op')
    request_s = ''
    
    @classmethod
    def resource_uri(cls, loc=None):
        loc_id = "id"
        if loc:
            loc_id = loc.id
        return ('api_op_location_detail', [loc_id, ])
    
    
    def read(self, request, id=None):
        Emitter.register('xml', OpLocationXMLEmitter, 'text/xml; charset=utf-8')

        # store request as a string, as cache key
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
                      locs = locs.filter((Q(name__istartswith=request.GET['namestartswith']) |
                                          Q(alternative_name__istartswith=request.GET['namestartswith']))).order_by('location_type__id', '-inhabitants')
                    if 'name' in request.GET:
                      locs = locs.filter((Q(name=request.GET['name']) | Q(alternative_name=request.GET['name']))).order_by('location_type__id')
                    if 'location_type' in request.GET:
                        location_type = request.GET['location_type']
                        # self.fields.remove(('location_type', ('name', )))
                        if location_type in ('comune', 'provincia', 'regione'):
                            locs = locs.filter(location_type__name__iexact=location_type)
                        else:
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
    

class ChargeTypeHandler(BaseHandler):
  model = OpChargeType
  fields = ('id', 'name', 'short_name', 'priority', 'category')
  allowed_methods = ('GET')

  def read(self, request):
    Emitter.register('xml', OpXMLEmitter, 'text/xml; charset=utf-8')
    return OpChargeType.objects.using('op').all()


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
    
    
class SimilarityHandler(BaseHandler):
    model = OpPolitician
    exclude = ('picture',)
    allowed_methods = ('GET')
    base = model.objects.using('op')
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
            members = None

            if 'first_name' not in request.GET or 'last_name' not in request.GET:
                return {'error': 'must specify first_name, last_name and, optionally, birth_date'}


            if 'first_name' in request.GET and 'last_name' in request.GET:
                members = self.base.select_related().filter(
                    Q(first_name=request.GET['first_name'], last_name=request.GET['last_name']),
                )
            if 'first_name' in request.GET and 'last_name' in request.GET and 'birth_date' in request.GET:
                members = self.base.select_related().filter(
                    Q(first_name=request.GET['first_name'], last_name=request.GET['last_name']) |
                    Q(first_name=request.GET['first_name'], birth_date=request.GET['birth_date']) |
                    Q(last_name=request.GET['last_name'], birth_date=request.GET['birth_date'])
                )

            if members:
                if 'count' in request.GET and request.GET['count'] == 'true':
                    return len(members)

                if 'limit' in request.GET:
                    members = members[:request.GET['limit']]

                pols = []
                for member in members:
                    api_url = reverse('api_op_politician_detail', args=[member.content_id])
                    member_charges = [c['textual_rep'] for c in member.getInstitutionCharges()]
                    member= {
                        'op_id': member.content_id,
                        'first_name': member.first_name,
                        'last_name': member.last_name,
                        'birth_date': member.birth_date,
                        'birth_location': member.birth_location,
                        'charges': member_charges,
                        'op_link': 'http://www.openpolis.it/politico/%s' % member.content_id,
                        'api_link': '%s%s' % (settings.SITE_URL, api_url)
                    }
                    pols.append(member)
                return pols
            else:
                if 'count' in request.GET:
                    return 0
                else:
                    return []

        except self.model.DoesNotExist:
            return None


class PoliticianHandler(BaseHandler):
    """docstring for PoliticianHandler"""
    model = OpPolitician
    exclude = ('picture',)
    allowed_methods = ('GET')
    base = model.objects.using('op')
    request_s = ''
    

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
                members = None

                if 'first_name' in request.GET or\
                    'namestartswith' in request.GET:

                    if 'first_name' in request.GET and 'last_name' in request.GET and 'birth_date' in request.GET:
                        members = self.base.select_related().filter(
                            Q(first_name=request.GET['first_name'],
                              last_name=request.GET['last_name'],
                              birth_date=request.GET['birth_date'])
                        )
                    elif 'first_name' in request.GET and 'last_name' in request.GET:
                        members = self.base.select_related().filter(
                            Q(first_name=request.GET['first_name'], last_name=request.GET['last_name']),
                            )
                    elif 'namestartswith' in request.GET:
                        members = self.base.select_related().filter(
                            Q(last_name__istartswith=request.GET['namestartswith'])
                        )

                    pols = []
                    if members:
                        if 'limit' in request.GET:
                            members = members[:request.GET['limit']]

                        for member in members:
                            api_url = reverse('api_op_politician_detail', args=[member.content_id])
                            member_charges = [c['textual_rep'] for c in member.getInstitutionCharges()]
                            member= {
                                'op_id': member.content_id,
                                'first_name': member.first_name,
                                'last_name': member.last_name,
                                'birth_date': member.birth_date,
                                'birth_location': member.birth_location,
                                'charges': member_charges,
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
                    api_url = reverse('api_op_politician_detail', args=[member.content_id])
                    member= {
                        'op_id': member.content_id,
                        'charge': member.charge_type.name,
                        'date_start': member.date_start,
                        'date_end': member.date_end,
                        'party': member.party.getNormalizedAcronymOrName(),
                        'first_name': member.first_name,
                        'last_name': member.last_name,
                        'birth_date': member.birth_date,
                        'birth_location': member.birth_location,
                        'op_link': 'http://www.openpolis.it/politico/%s' % member.content_id,
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
                'birth_location': ic_mayor.politician.birth_location,
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
    

class InstitutionChargeHandler(BaseHandler):
    """
    Handler to extract institution charges, used in open_action.
    Extracts a list of complex objects, containing some institution charge details,
    and politician and resources details, too, used while selecting the recipients of a campaign.
    Limit is set by default to 10.
    """
    model = OpInstitutionCharge
    allowed_methods = ('GET')
    base = model.objects.using('op').filter(date_end__isnull=True)
    fields = ('content_id', 'politician')

    @classmethod
    def resource_uri(cls, charge=None):
        charge_id = "content_id"
        if charge:
            charge_id = charge.id
        return ('api_op_institutioncharge_detail', [charge_id, ])

    def filterByConstituencies(self, members, election_type, location):
        """
        Filter members through constituency, given an election type and a location
        @return: members queryset
        """
        locations = ()
        members = members.filter(constituency__election_type__name=election_type)
        if location.is_city() or location.is_province():
            locations = (location.provincial_id,)
        elif location.is_region():
            locations = location.getProvincesInRegion().values('id')

        constituencies = OpConstituencyLocation.objects.db_manager('op').filter(
            constituency__election_type__name=election_type,
            location__provincial_id__in=locations).values('constituency').distinct()
        members = members.filter(
            constituency__in=constituencies,
        )

        return members



    def read(self, request, charge_id=None):
        Emitter.register('xml', OpXMLEmitter, 'text/xml; charset=utf-8')
        try:
            if charge_id is not None:
                return {'error': 'Not implemented'}
            else:
                members = self.base
                context = None
                is_parliament = False

                if 'context' in request.GET:
                    context = request.GET['context']

                location = None
                if 'location_id' in request.GET:
                    location = OpLocation.objects.db_manager('op').get(pk=request.GET['location_id'])

                #
                # filters building
                #

                # no context, pre-set filters for location types
                # returning all members of a given location
                if context is None:
                    if location is None:
                        # whole (limits are on by default)
                        pass
                    elif location.is_region():
                        # governatore, assessori and consiglieri
                        members = members.filter(
                            location__location_type__name='Regione', location__regional_id=location.regional_id)
                    elif location.is_province():
                        # president of la provincia, assessori and consiglieri
                        members = members.filter(
                            location__location_type__name='Provincia', location__provincial_id=location.provincial_id)
                    elif location.is_city():
                        # sindaco, assessori and consiglieri
                        members = members.filter(
                            location__location_type__name='Comune', location__city_id=location.city_id)

                # location-independent contexts
                elif context == 'euro-commissario':
                    members = members.filter(institution__id=1)
                elif context == 'pres-della-repubblica':
                    members = members.filter(charge_type__id=19)
                elif context == 'pres-del-consiglio':
                    members = members.filter(institution__id=3, charge_type__id=7)
                elif context == 'ministro' or context == 'ministri':
                    members = members.filter(institution__id=3, charge_type__id=9)

                # italian and european parliaments
                elif context == 'euro-deputato' or context == 'euro-deputati':
                    members = members.filter(institution__id=2)
                    # constituency filtering, from location, in case of euro parliament
                    if location:
                        members = self.filterByConstituencies(members, election_type='EU', location=location)

                elif context == 'deputato' or context == 'deputati':
                    members = members.filter(charge_type__id=5)

                    # constituency filtering, from location, in case of camera
                    if location:
                        members = self.filterByConstituencies(members, election_type='Camera', location=location)


                elif context == 'senatore' or context == 'senatori':
                    from django.db import Q
                    members = members.filter(Q(charge_type__id=6) | Q(charge_type__id=20))
                    # constituency filtering, from location, in case of senato
                    if location:
                        members = self.filterByConstituencies(members, election_type='Senato', location=location)


                # governatori
                elif context == 'governatore' or context == 'governatori':
                    members = members.filter(institution__id=6, charge_type__id=1)
                    if location is None:
                        pass
                    else:
                        members = members.filter(location__regional_id=location.regional_id)

                # assessori regionali
                elif context == 'assessore-reg' or context == 'assessore-regionale' or context == 'assessori-regionali':
                    members = members.filter(institution__id=6, charge_type__id=12)
                    if location is None:
                        return {'error': 'Location ID of a region at least must be specified for this context.'}
                    else:
                        members = members.filter(location__regional_id=location.regional_id)

                # consiglieri regionali
                elif context == 'consigliere-reg' or context == 'consigliere-regionale' or context == 'consiglieri-regionali':
                    members = members.filter(institution__id=7, charge_type__id=13)
                    if location is None:
                        return {'error': 'Location ID of a region at least, must be specified for this context.'}
                    else:
                        members = members.filter(location__regional_id=location.regional_id)


                # presidenti di provincia
                elif context == 'pres-prov' or context == 'presidente-provincia' or context == 'presidenti-provincia':
                    members = members.filter(institution__id=8, charge_type__id=1)
                    if location is None:
                        pass
                    elif location.is_region():
                        members = members.filter(location__regional_id=location.regional_id)
                    else:
                        members = members.filter(location__provincial_id=location.provincial_id)

                # assessori provinciali
                elif context == 'assessore-prov' or context == 'assessore-provinciale' or context == 'assessori-provinciali':
                    members = members.filter(institution__id=8, charge_type__id=12)
                    if location is None or location.is_region():
                        return {'error': 'Location ID of a province at least must be specified for this context.'}
                    else:
                        members = members.filter(location__provincial_id=location.provincial_id)

                # consiglieri provinciali
                elif context == 'consigliere-prov' or context == 'consigliere-provinciale' or context == 'consiglieri-provinciali':
                    members = members.filter(institution__id=9, charge_type__id=13)
                    if location is None or location.is_region():
                        return {'error': 'Location ID of a province at least must be specified for this context.'}
                    else:
                        members = members.filter(location__provincial_id=location.provincial_id)


                # sindaci
                elif context == 'sindaco' or context == 'sindaci':
                    members = members.filter(charge_type__id=14)
                    if location is None:
                        return {'error': 'Location ID of a province at least must be specified for this context.'}
                    elif location.is_region():
                        members = members.filter(location__regional_id=location.regional_id)
                    elif location.is_province():
                        members = members.filter(location__provincial_id=location.provincial_id)
                    else:
                        members = members.filter(location__city_id=location.city_id)

                # assessori comunali
                elif context == 'assessore-com' or context == 'assessore-comunale' or context == 'assessori-comunali':
                    members = members.filter(institution__id=10, charge_type__id=12)
                    if not location or not location.is_city():
                        return {'error': 'Location ID of a city must be specified for this context.'}
                    else:
                        members = members.filter(location__provincial_id=location.provincial_id)

                # consiglieri comunali
                elif context == 'consigliere-com' or context == 'consigliere-comunale' or context == 'consiglieri-comunali':
                    members = members.filter(institution__id=11, charge_type__id=13)
                    if not location or not location.is_city():
                        return {'error': 'Location ID of a city must be specified for this context.'}
                    else:
                        members = members.filter(location__provincial_id=location.provincial_id)


                # commissariamenti
                elif context == 'commissario' or context == 'commissari':
                    members = members.filter(institution__id=12)
                    if location is None:
                        pass
                    elif location.is_region():
                        members = members.filter(location__regional_id=location.regional_id)
                    elif location.is_province():
                        members = members.filter(location__provincial_id=location.provincial_id)
                    else:
                        members = members.filter(location__city_id=location.city_id)



                # add sorting criteria
                members = members.order_by('charge_type__priority', '-date_start')


                if 'limit' in request.GET:
                    limit = int(request.GET['limit'])
                else:
                    limit = 20

                if 'offset' in request.GET:
                    offset = int(request.GET['offset'])
                else:
                    offset = 0

                members = members.distinct()
                sliced_members = members[offset:limit+offset]

                n_results = members.count()

                # build results array
                results = {
                    'n_results': n_results,
                    'offset': offset,
                    'limit': limit,
                    'members': [],
                }


                # add next and previous links, to navigate through pages
                current_url = '%s%s' % (settings.SITE_URL, request.get_full_path())
                if limit + offset < n_results:
                    results['next'] = set_query_parameter(current_url, 'offset', limit + offset)
                if offset >= limit:
                    results['previous'] = set_query_parameter(current_url, 'offset', limit - offset)


                for m in sliced_members:
                    p = m.politician
                    api_politician_url = reverse('api_op_politician_detail', args=(p.content_id,))
                    member= {
                        'op_charge_id': m.content_id,
                        'charge': m.charge_type.name,
                        'description': m.description,
                        'institution': m.institution.name,
                        'location': m.location.name,
                        'location_type': m.location.location_type.name,
                        'date_start': m.date_start,
                        'date_end': m.date_end,
                        'party': m.party.getNormalizedAcronymOrName(),
                        'politician': {
                            'op_politician_id': p.content_id,
                            'first_name': p.first_name,
                            'last_name': p.last_name,
                            'sex': p.sex,
                            'birth_date': p.birth_date,
                            'birth_location': p.birth_location,
                            'resources': p.getResources(),
                        },
                        'op_link': 'http://politici.openpolis.it/politico/%s' % m.politician.content_id,
                        'politician_uri': '%s%s' % (settings.SITE_URL, api_politician_url),
                        'textual_rep': m.getTextualRepresentation()
                    }
                    if m.constituency:
                        member['constituency'] = m.constituency.name
                    results['members'].append(member)

                return results

        except self.model.DoesNotExist:
          return None



