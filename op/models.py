from django.db import models
from django.db import connections
from django.conf import settings

class OpLocationType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=96)
    class Meta:
        db_table = u'op_location_type'
        managed = False
        
    def __unicode__(self):
      return self.name


class OpLocationManager(models.Manager):
  def getFromTypeId(self, location_type, location_id):
    if (location_type == 'regional'):
      locations = self.filter(location_type__name__iexact='regione', regional_id=location_id)
    elif (location_type == 'provincial'):
      locations = self.filter(location_type__name__iexact='provincia', provincial_id=location_id)
    elif (location_type == 'city'):
      locations = self.filter(location_type__name__iexact='comune', city_id=location_id)
    else:
      raise Exception('wrong location_type parameters %s not in (regional, provincial, city)' % location_type)

    return locations[0]

class OpLocation(models.Model):
    id = models.IntegerField(primary_key=True)
    location_type = models.ForeignKey(OpLocationType)
    name = models.CharField(max_length=255, blank=True)
    macroregional_id = models.IntegerField(null=True, blank=True)
    regional_id = models.IntegerField(null=True, blank=True)
    provincial_id = models.IntegerField(null=True, blank=True)
    city_id = models.IntegerField(null=True, blank=True)
    prov = models.CharField(max_length=2, blank=True)
    inhabitants = models.IntegerField(null=True, blank=True)
    last_charge_update = models.DateTimeField(null=True, blank=True)
    alternative_name = models.CharField(max_length=255, blank=True)
    minint_regional_code = models.IntegerField(null=True, blank=True)
    minint_provincial_code = models.IntegerField(null=True, blank=True)
    minint_city_code = models.IntegerField(null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    new_location_id = models.IntegerField(null=True, blank=True)

    objects = OpLocationManager()

    class Meta:
        db_table = u'op_location'
        managed = False

    def __unicode__(self):
      return self.name
      

        
class OpUser(models.Model):
    id = models.IntegerField(primary_key=True)
    location = models.ForeignKey(OpLocation, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=16, blank=True)
    is_active = models.IntegerField()
    email = models.CharField(max_length=100)
    sha1_password = models.CharField(unique=True, max_length=40, blank=True)
    salt = models.CharField(max_length=32, blank=True)
    want_to_be_moderator = models.IntegerField(null=True, blank=True)
    is_moderator = models.IntegerField(null=True, blank=True)
    is_administrator = models.IntegerField(null=True, blank=True)
    deletions = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    picture = models.TextField(blank=True)
    url_personal_website = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    has_paypal = models.IntegerField(null=True, blank=True)
    remember_key = models.CharField(max_length=64, blank=True)
    wants_newsletter = models.IntegerField()
    public_name = models.IntegerField()
    charges = models.IntegerField(null=True, blank=True)
    resources = models.IntegerField(null=True, blank=True)
    declarations = models.IntegerField(null=True, blank=True)
    themes = models.IntegerField(null=True, blank=True)
    comments = models.IntegerField(null=True, blank=True)
    last_contribution = models.DateTimeField(null=True, blank=True)
    is_premium = models.IntegerField(null=True, blank=True)
    is_adhoc = models.IntegerField(null=True, blank=True)
    is_aggiungitor = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'op_user'
        managed = False

class OpContent(models.Model):
    id = models.IntegerField(primary_key=True)
    reports = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    op_table = models.CharField(max_length=128, blank=True)
    op_class = models.CharField(max_length=128, blank=True)
    hash = models.CharField(max_length=32, blank=True)
    class Meta:
        db_table = u'op_content'
        managed = False

class OpOpenContent(models.Model):
    content = models.ForeignKey(OpContent)
    user = models.ForeignKey(OpUser)
    deleted_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'op_open_content'
        managed = False


class OpProfessionManager(models.Manager):
  def getBasic(self):
    return self.filter(oid__isnull=True)

class OpProfession(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    oid = models.IntegerField(null=True, blank=True)
    odescription = models.CharField(max_length=255, blank=True)
    objects = OpProfessionManager()
    class Meta:
        db_table = u'op_profession'
        managed = False

class OpElectionType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    class Meta:
        db_table = u'op_election_type'
        managed = False

class OpElection(models.Model):
    id = models.IntegerField(primary_key=True)
    election_date = models.DateField(unique=True, null=True, blank=True)
    election_type = models.ForeignKey(OpElectionType)
    location = models.ForeignKey(OpLocation)
    class Meta:
        db_table = u'op_election'
        managed = False

class OpPolitician(models.Model):
    content = models.ForeignKey(OpContent)
    profession = models.ForeignKey(OpProfession, null=True, blank=True)
    user = models.ForeignKey(OpUser, null=True, blank=True, related_name='oppolitician_user_set')
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    sex = models.CharField(max_length=1, blank=True)
    picture = models.TextField(blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    birth_location = models.CharField(max_length=128, blank=True)
    death_date = models.DateTimeField(null=True, blank=True)
    last_charge_update = models.DateTimeField(null=True, blank=True)
    is_indexed = models.IntegerField()
    minint_aka = models.CharField(unique=True, max_length=255, blank=True)
    creator = models.ForeignKey(OpUser, null=True, blank=True, related_name='oppolitician_creator_set')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'op_politician'
        managed = False


class OpEducationLevelManager(models.Manager):
  def getBasic(self):
    return self.filter(oid__isnull=True)

class OpEducationLevel(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    oid = models.IntegerField(null=True, blank=True)
    odescription = models.CharField(max_length=255, blank=True)
    objects = OpEducationLevelManager()
    class Meta:
        db_table = u'op_education_level'
        managed = False

class OpPoliticianHasOpEducationLevel(models.Model):
    politician = models.ForeignKey(OpPolitician)
    education_level = models.ForeignKey(OpEducationLevel)
    description = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'op_politician_has_op_education_level'
        managed = False

class OpInstitution(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    short_name = models.CharField(max_length=45, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'op_institution'
        managed = False

class OpChargeType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    short_name = models.CharField(max_length=45, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=1)
    class Meta:
        db_table = u'op_charge_type'
        managed = False

class OpInstitutionHasChargeType(models.Model):
    institution = models.ForeignKey(OpInstitution)
    charge_type = models.ForeignKey(OpChargeType)
    class Meta:
        db_table = u'op_institution_has_charge_type'
        managed = False


class OpConstituency(models.Model):
    id = models.IntegerField(primary_key=True)
    election_type = models.ForeignKey(OpElectionType)
    name = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=128, blank=True)
    valid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'op_constituency'
        managed = False

class OpConstituencyLocation(models.Model):
    constituency = models.ForeignKey(OpConstituency)
    location = models.ForeignKey(OpLocation)
    class Meta:
        db_table = u'op_constituency_location'
        managed = False

class OpParty(models.Model):
    id = models.IntegerField(primary_key=True)
    istat_code = models.CharField(max_length=15, blank=True)
    name = models.CharField(unique=True, max_length=80)
    acronym = models.CharField(max_length=20, blank=True)
    party = models.IntegerField(null=True, blank=True)
    main = models.IntegerField(null=True, blank=True)
    electoral = models.IntegerField(null=True, blank=True)
    oid = models.IntegerField(null=True, blank=True)
    oname = models.CharField(max_length=80, blank=True)
    logo = models.TextField(blank=True)
    class Meta:
        db_table = u'op_party'
        managed = False

class OpPartyLocation(models.Model):
    party = models.ForeignKey(OpParty)
    location = models.ForeignKey(OpLocation)
    class Meta:
        db_table = u'op_party_location'
        managed = False

class OpGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255, blank=True)
    acronym = models.CharField(max_length=80, blank=True)
    oid = models.IntegerField(null=True, blank=True)
    oname = models.CharField(max_length=80, blank=True)
    class Meta:
        db_table = u'op_group'
        managed = False

class OpGroupLocation(models.Model):
    group = models.ForeignKey(OpGroup)
    location = models.ForeignKey(OpLocation)
    class Meta:
        db_table = u'op_group_location'
        managed = False


class OpInstitutionChargeManager(models.Manager):
    def get_statistics(self, request):
        from django.db import connection
        cursor = connections['op'].cursor()

        base_sql = """
            from op_institution_charge ic, op_institution i, op_open_content oc, op_politician p, 
              op_location l, op_profession pr, op_politician_has_op_education_level pe, op_education_level e 
            where l.id=ic.location_id and ic.institution_id=i.id and 
              ic.politician_id=p.content_id and oc.content_id=ic.content_id and
              p.profession_id=pr.id and p.content_id=pe.politician_id and
              pe.education_level_id=e.id and  
              oc.deleted_at is null and ic.date_end is null 
            """
        filters = {}
        results = {}
        
        clauses_sql = ""
        clauses_params = []


        #
        # building filters
        #
        
        location_types = ('all', 'regional', 'provincial', 'city')
        location_id = 0
        if 'location_id' in request.GET:
          location_id = request.GET['location_id']
        location_type = 0
        if 'location_type' in request.GET:
          location_type = request.GET['location_type']
        if location_id != 0:
          if location_type in location_types:
            location = OpLocation.objects.db_manager('op').getFromTypeId(location_type, location_id)
            clauses_sql += " and l.%s_id=%%s " % location_type
            clauses_params.append(location_id)
            filters['location_context'] = { 'type': location_type, 'id': location_id, 'name': location.name, 'op_location_id': location.id }
          else:
            raise Exception('wrong location type parameter: %s not in (regional, provincial, city)' % location_type)
        elif location_type == 'all':
          clauses_sql += " and l.location_type_id in (4, 5, 6) "
          filters['location_context'] = { 'type': 'all' }
        
        ages = {
          'twenties': 20, 
          'thirties': 30, 
          'forties': 40, 
          'fifties': 50, 
          'sixties': 60, 
          'seventies': 70, 
          'eighties': 80, 
          'nineties': 90, 
          'venerables': 100
        }        
        age = 0
        if 'age' in request.GET:
          age = request.GET['age']
        if age != 0:
          if age in ages.keys():
            tenth = ages[age] / 10
            clauses_sql += " and YEAR(CURDATE())-YEAR(p.birth_date) < %d5 and YEAR(CURDATE())-YEAR(p.birth_date) >= %d5 " % (tenth, tenth-1)
            filters['age'] = age
          else:
            raise Exception('wrong age parameter: %s not in (twenties, thirties, ..., nineties, venerables)' % age)

        sexes = ('M', 'F')
        sex = 0
        if 'sex' in request.GET:
          sex = request.GET['sex']
        if sex != 0:
          if sex in sexes:
            clauses_sql += " and sex = %s"
            clauses_params.append(sex)
            filters['sex'] = sex
          else:
            raise Exception('wrong sex parameter: %s not in (M, F)' % sex)
            
        institutions = ('giunta_regionale', 'consiglio_regionale', 'giunta_provinciale', 'consiglio_provinciale', 'giunta_comunale', 'consiglio_comunale', 'commissariamento')
        institution = 0
        if 'institution' in request.GET:
          institution = request.GET['institution']
        if institution != 0:
          if institution in institutions:
            clauses_sql += " and i.name = %s"
            clauses_params.append(institution.replace('_', ' '))
            filters['institution'] = institution.replace('_', ' ')
          else:
            raise Exception('wrong institution parameter: %s not in (giunta_regionale, consiglio_regionale, ...)' % institution)
         
        professions = {}
        for profession in OpProfession.objects.db_manager('op').getBasic().values('id', 'description', 'odescription'):
          if profession['odescription']:
            professions[profession['id']] = profession['odescription']
          else:
            professions[profession['id']] = profession['description']
        profession_id = 0
        if 'profession_id' in request.GET:
          profession_id = int(request.GET['profession_id'])
        if profession_id != 0:
          if profession_id in professions.keys():
            clauses_sql += " and (pr.id = %s or pr.oid = %s)"
            clauses_params.extend([profession_id, profession_id])
            filters['profession'] = { 'id': profession_id, 'name': professions[profession_id] }
          else:
            raise Exception('wrong institution parameter: %s not in professions_ids' % profession_id)

        educations = {}
        for education in OpEducationLevel.objects.db_manager('op').getBasic().values('id', 'description'):
          educations[education['id']] = education['description']
        education_id = 0
        if 'education_id' in request.GET:
          education_id = int(request.GET['education_id'])
        if education_id != 0:
          if education_id in educations.keys():
            clauses_sql += " and (e.id = %s or e.oid = %s)"
            clauses_params.extend([education_id, education_id])
            filters['education'] = { 'id': education_id, 'name': educations[education_id] }
          else:
            raise Exception('wrong institution parameter: %s not in educations_ids' % education_id)

        #
        # building results
        #
        total_sql = """
            select count(*) as n
            %s %s
            """ % (base_sql, clauses_sql)
        cursor.execute(total_sql, clauses_params)
        row = cursor.fetchone()
        results['total'] = row[0]

        age_numbers = {
          'twenties':   { 'count': 0 },
          'thirties':   { 'count': 0 },
          'fourties':   { 'count': 0 },
          'fifties':    { 'count': 0 },
          'sixties':    { 'count': 0 },
          'seventies':  { 'count': 0 },
          'eighties':   { 'count': 0 },
          'nineties':   { 'count': 0 },
          'venerables': { 'count': 0 }
        }
        if age == 0:
          age_sql = """
              select YEAR(CURDATE())-YEAR(p.birth_date) as age, count(*) as n
              %s %s      
              group by age order by n desc
              """ % (base_sql, clauses_sql)
          cursor.execute(age_sql, clauses_params)

          for row in cursor.fetchall():
              age = row[0]
              if age < 25:
                age_numbers['twenties']['count'] += row[1]
              elif age >= 25 and age < 35:
                age_numbers['thirties']['count'] += row[1]
              elif age >= 35 and age < 45:
                age_numbers['fourties']['count'] += row[1]
              elif age >= 45 and age < 55:
                age_numbers['fifties']['count'] += row[1]
              elif age >= 55 and age < 65:
                age_numbers['sixties']['count'] += row[1]
              elif age >= 65 and age < 75:
                age_numbers['seventies']['count'] += row[1]
              elif age >= 75 and age < 85:
                age_numbers['eighties']['count'] += row[1]
              elif age >= 85 and age < 95:
                age_numbers['nineties']['count'] += row[1]
              elif age >= 9:
                age_numbers['venerables']['count'] += row[1]

          results['age'] = age_numbers
          

        if sex == 0:          
          sex_sql = """
              select p.sex, count(*) as n
              %s %s      
              group by p.sex order by n desc
              """ % (base_sql, clauses_sql)
          cursor.execute(sex_sql, clauses_params)          
          sex_numbers = {}
          for row in cursor.fetchall():
              sex = row[0]
              sex_numbers[sex] = int(row[1])

          if 'M' in sex_numbers.keys():
            sex_numbers_m = sex_numbers['M']
          else:
            sex_numbers_m = 0
            
          if 'F' in sex_numbers.keys():
            sex_numbers_f = sex_numbers['F']
          else:
            sex_numbers_f = 0
            
          results['sex'] = { 'M': { 'count': sex_numbers_m }, 'F': { 'count': sex_numbers_f } }
          
          
        institution_numbers = {}
        for inst in OpInstitution.objects.using('op').all().values('id', 'name'):
          if 'giunta' in inst['name'].lower() or 'consiglio' in inst['name'].lower() or 'commissariamento' in inst['name'].lower():
            institution_numbers[inst['id']] = { 'name': inst['name'], 'count': 0 }
        if institution == 0:
          institution_sql = """
              select i.id, count(*) as n
              %s %s      
              group by i.id order by n desc
            """ % (base_sql, clauses_sql)
          cursor.execute(institution_sql, clauses_params)          
          for row in cursor.fetchall():
              i_id = row[0]
              i_count = int(row[1])
              
              if i_id in institution_numbers:
                institution_numbers[i_id]['count'] += i_count
              else:
                if settings.DEBUG:
                  print "Impossibile trovare institution_id: %s" % (i_id,)

          results['institutions'] = institution_numbers

        
        profession_numbers = {}
        for profession in OpProfession.objects.db_manager('op').getBasic().values('id', 'odescription'):
          profession_numbers[profession['id']] = { 'name': profession['odescription'], 'count': 0 }
        if profession_id == 0:
          profession_sql = """
              select pr.id, pr.oid, count(*) as n
              %s %s
              group by pr.id, pr.oid order by n desc
            """ % (base_sql, clauses_sql)
          cursor.execute(profession_sql, clauses_params)             
          for row in cursor.fetchall():
              if row[1] != None:
                p_id = row[1]
              else:
                p_id = row[0]
              p_count = int(row[2])
              if p_id in profession_numbers:
                profession_numbers[p_id]['count'] += p_count
              else:
                if settings.DEBUG:
                  print "Impossibile trovare profession_id (oid: %s, id: %s)" % (row[1], row[0])

          results['professions'] = profession_numbers


        education_numbers = {}
        for education in OpEducationLevel.objects.db_manager('op').getBasic().values('id', 'description'):
          education_numbers[education['id']] = { 'name': education['description'], 'count': 0 }
        if education_id == 0:
          education_sql = """
              select e.id, e.oid, count(*) as n
              %s %s
              group by e.id, e.oid order by n desc
            """ % (base_sql, clauses_sql)
          cursor.execute(education_sql, clauses_params)             
          for row in cursor.fetchall():
              if row[1] != None:
                e_id = row[1]
              else:
                e_id = row[0]
              e_count = int(row[2])

              if e_id in education_numbers:
                education_numbers[e_id]['count'] += e_count
              else:
                if settings.DEBUG:
                  print "Impossibile trovare education_id (oid: %s, id: %s)" % (row[0], row[1])
                
          results['educations'] = education_numbers
        

        return { 'filters': filters, 'results': results }
        

class OpInstitutionCharge(models.Model):
    content = models.ForeignKey(OpOpenContent)
    politician = models.ForeignKey(OpPolitician)
    institution = models.ForeignKey(OpInstitution)
    charge_type = models.ForeignKey(OpChargeType)
    location = models.ForeignKey(OpLocation, null=True, blank=True)
    constituency = models.ForeignKey(OpConstituency, null=True, blank=True)
    party = models.ForeignKey(OpParty)
    group = models.ForeignKey(OpGroup)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    minint_verified_at = models.DateTimeField(null=True, blank=True)
    
    objects = OpInstitutionChargeManager()
    
    class Meta:
        db_table = u'op_institution_charge'
        managed = False
