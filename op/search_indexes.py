import datetime
from haystack.indexes import *
from haystack import site
from op_api.op.models import OpPolitician, OpLocation

class LocationIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name')
    location_id = IntegerField(model_attr='id', indexed=False)
    location_type = CharField(model_attr='location_type__name', null=True)
    inhabitants = IntegerField(model_attr='inhabitants', null=True)
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return OpLocation.objects.db_manager('op').all()
    
class PoliticianIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pol_id = IntegerField(model_attr='content_id', indexed=False)
    last_name = CharField(model_attr='last_name')
    first_name = CharField(model_attr='first_name', null=True)
    birth_date = DateField(model_attr='birth_date', indexed=False, null=True)
    birth_location = CharField(model_attr='birth_location', indexed=False, null=True)
    sex = CharField(model_attr='sex')
    

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return OpPolitician.objects.db_manager('op').all()

site.register(OpPolitician, PoliticianIndex)
site.register(OpLocation, LocationIndex)
