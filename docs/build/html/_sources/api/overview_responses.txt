.. _api-overview-responses:

================
Response Formats
================

Openpolis provides different representations format for the resource you request: JSON, XML, Yaml.

JSON
****
openpolis REST API returns resource representations as JSON, by default. Here is the default representation for a location resource::

   GET /1.0/locations/1248


.. code-block:: ruby

   {
       "macroregional_id": 1, 
       "name": "Verrayes", 
       "gps_lat": 45.764200000000002, 
       "city_id": 7072, 
       "minint_regional_code": 2, 
       "regional_id": 2, 
       "id": 1248, 
       "provincial_id": 7, 
       "inhabitants": 1327, 
       "minint_city_code": 710, 
       "gps_lon": 7.5357000000000003, 
       "resource_uri": "/op/1.0/locations/1248/", 
       "location_type": {
           "name": "Comune"
       }, 
       "minint_provincial_code": 4
   }

XML
***
an XML representation can be obtained by adding the format specification in the query string parameters::

     GET /1.0/locations/1248?format=xml

.. code-block:: xml

    <op_content>
      <macroregional_id>1</macroregional_id>
      <name>Verrayes</name>
      <gps_lat>45.7642</gps_lat>
      <city_id>7072</city_id>
      <minint_regional_code>2</minint_regional_code>
      <regional_id>2</regional_id>
      <id>1248</id>
      <provincial_id>7</provincial_id>
      <inhabitants>1327</inhabitants>
      <minint_city_code>710</minint_city_code>
      <gps_lon>7.5357</gps_lon>
      <resource_uri>/op/1.0/locations/1248/</resource_uri>
      <location_type>
        <name>Comune</name>
      </location_type>
      <minint_provincial_code>4</minint_provincial_code>
    </op_content>
    
Yaml
****
a Yaml representation is obtained by adding the ``format=yaml`` format specification in the request query string, in this case the file is downloaded and not visualized on screen::

    GET /1.0/locations/1248?format=yaml

.. code-block:: ruby

  city_id: 7072
  gps_lat: 45.764200000000002
  gps_lon: 7.5357000000000003
  id: 1248
  inhabitants: 1327
  location_type: {name: Comune}
  macroregional_id: 1
  minint_city_code: 710
  minint_provincial_code: 4
  minint_regional_code: 2
  name: Verrayes
  provincial_id: 7
  regional_id: 2
  resource_uri: /op/1.0/locations/1248/


