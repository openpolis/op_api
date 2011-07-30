'''
Custom XML emitter for the op_location data
'''

from django.utils.xmlutils import SimplerXMLGenerator
from piston.emitters import Emitter
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.encoding import smart_unicode
from django.core.urlresolvers import reverse, NoReverseMatch

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class OpXMLEmitter(Emitter):
    def _get_item_name(self):
        return 'item'
        
    def _to_xml(self, xml, data, item_name='item'):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement(item_name, {})
                self._to_xml(xml, item)
                xml.endElement(item_name)
        elif isinstance(data, dict):
            for key, value in data.iteritems():
                if not isinstance(key, (long, int, float)):
                  attr = {}
                else:
                  attr = {'id': str(key)}
                  key = 'item'
                xml.startElement(key, attr)
                self._to_xml(xml, value)
                xml.endElement(key)
        else:
            xml.characters(smart_unicode(data))

    def render(self, request):
        stream = StringIO.StringIO()

        xml = SimplerXMLGenerator(stream, "utf-8")
        xml.startDocument()
        xml.startElement("op_content", {})

        self._to_xml(xml, self.construct(), item_name = self._get_item_name())

        xml.endElement("op_content")
        xml.endDocument()

        return stream.getvalue()

class OpLocationXMLEmitter(OpXMLEmitter):
  def _get_item_name(self):
      return 'location'


class OpProfessionXMLEmitter(OpXMLEmitter):
  def _get_item_name(self):
      return 'profession'

class OpEducationLevelXMLEmitter(OpXMLEmitter):
  def _get_item_name(self):
      return 'education_level'
  