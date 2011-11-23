from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings
from optparse import make_option
from piston.doc import generate_doc
from op_api.op.handlers import LocationHandler

class Command(NoArgsCommand):
  help = 'Test api doc generation'
  
  option_list = NoArgsCommand.option_list + (
      make_option('--dryrun',
          action='store_true',
          dest='dryrun',
          default=False,
          help='Execute a dry run: non-sense, currently.'),
      )
  
  
  def handle_noargs(self, **options):   
      h_doc = generate_doc(LocationHandler)

      print "handler: ", h_doc.name
      print "model: ", h_doc.handler.model
      print h_doc.resource_uri_template # -> '/api//{id}'
      print "methods --"
      for m in h_doc.get_methods():
          print "  %s(%s)" % (m.name, m.signature)
