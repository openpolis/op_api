.. _api-res-op-locations:

=========
Locations
=========
Openpolis locations are used throughout the projects in order to identify the geo-context. It may be the constituency where a politician was elected in, or a geo-tag in an openparlamento's act, identifying the place the act is talking about, it can be many other things.

Location instance
+++++++++++++++++
A Location instance resource represents a **single openpolis location**.

Resource URI
************
::

   /1.0/locations/{id}



Resource Properties
*******************
A Location resource is identified by the following properties:

============================= =======================================
property                      explanation
============================= =======================================
:const:`id`                   openpolis identifier
:const:`name`                 location name
:const:`macroregional_id`     macro-region identifier (istat)
:const:`regional_id`          region identifier (istat)
:const:`provincial_id`        province identifier (istat)
:const:`city_id`              city identifier (istat)
:const:`minint_regional_id`   region identifier (min. int.)
:const:`minint_provincial_id` province identifier (min. int.)
:const:`minint_city_id`       province identifier (min. int.)
:const:`gps_lat`              latitude (gps coords)
:const:`gps_lon`              longitude (gps coords)
:const:`inhabitants`          inhabitants (as of 2001)
:const:`location_type.name`   location type
============================= =======================================

.. note::

  :const:`location_type.name` indicates the :const:`name` field of the location_type class, which has a one-to-many relation to the main location resource.

HTTP GET
********
Returns a representation of a single location, including the properties above.


JSON Example
^^^^^^^^^^^^
::

    GET /1.0/locations/1745/

.. code-block:: ruby

    {
        "macroregional_id": 1, 
        "name": "Pellio Intelvi", 
        "gps_lat": 45.980800000000002, 
        "city_id": 13179, 
        "minint_regional_code": 3, 
        "regional_id": 3, 
        "id": 1745, 
        "provincial_id": 13, 
        "inhabitants": 940, 
        "minint_city_code": 1710, 
        "gps_lon": 9.0596999999999994, 
        "resource_uri": "/op/1.0/locations/1745/", 
        "location_type": {
            "name": "Comune"
        }, 
        "minint_provincial_code": 24
    }


XML Example
^^^^^^^^^^^^
::

    GET /1.0/locations/1745/?format=xml

.. code-block:: xml

  <op_content>
    <macroregional_id>1</macroregional_id>
    <name>Pellio Intelvi</name>
    <gps_lat>45.9808</gps_lat>
    <city_id>13179</city_id>
    <minint_regional_code>3</minint_regional_code>
    <regional_id>3</regional_id>
    <id>1745</id>
    <provincial_id>13</provincial_id>
    <inhabitants>940</inhabitants>
    <minint_city_code>1710</minint_city_code>
    <gps_lon>9.0597</gps_lon>
    <resource_uri>/op/1.0/locations/1745/</resource_uri>
    <location_type>
      <name>Comune</name>
    </location_type>
    <minint_provincial_code>24</minint_provincial_code>
  </op_content>


HTTP POST
*********
Not yet supported. To be done in the future.

HTTP PUT
********
Not supported.

HTTP DELETE
***********
Not supported.



Locations list
++++++++++++++

Resource URI
************
::

   /1.0/locations

HTTP GET
********
Retrieves a list of the Locations resources.

List filters
^^^^^^^^^^^^
The following query string parameters allow you to limit the list returned:

================= ====================================================================================
Parameter         Description
================= ====================================================================================
namestartswith    Only return Locations starting with the given string (case insensitive)
name              Only return Locations whose name matches exactly the string given (case insensitive)
location_type     Only return Locations of the given type. May be `regione`, `provincia`, `comune`
regional_id       Only return Locations of the given region. ``location_type`` must be `provincia` or `comune`
provincial_id     Only return Locations of the given province. ``location_type`` must be `comune`
================= ====================================================================================

In all examples below, locations are sorted by inhabitants, first the more populous.
Default output is json, add ``?format=xml`` to get xml.


Example 1
^^^^^^^^^
The list of all the locations. It is very long and it takes very long to send, even if cached.
::

    GET /1.0/locations/

.. code-block:: python

    [
        {
            "macroregional_id": null, 
            "name": "Europa", 
            "gps_lat": null, 
            "city_id": null, 
            "minint_regional_code": null, 
            "regional_id": null, 
            "id": 1, 
            "provincial_id": null, 
            "inhabitants": null, 
            "minint_city_code": null, 
            "gps_lon": null, 
            "resource_uri": "/op/1.0/locations/1/", 
            "location_type": {
                "name": "Europa"
            }, 
            "minint_provincial_code": null
        }, 
        {
            "macroregional_id": null, 
            "name": "Italia", 
            "gps_lat": null, 
            "city_id": null, 
            "minint_regional_code": null, 
            "regional_id": null, 
            "id": 2, 
            "provincial_id": null, 
            "inhabitants": 58751711, 
            "minint_city_code": null, 
            "gps_lon": null, 
            "resource_uri": "/op/1.0/locations/2/", 
            "location_type": {
                "name": "Italia"
            }, 
            "minint_provincial_code": null
        }, 
        ...
    ]
    
Example 2
^^^^^^^^^
Locations can be filtered by type, using the ``location_type`` filter. The example below extracts the list of all the regions.
Provinces and cities can be extracted the same way (the list of all cities is practically as long as the complete list in example 1)
::

    GET /1.0/locations/?location_type=regione

.. code-block:: python

    [
        {
            "macroregional_id": 1, 
            "name": "Piemonte", 
            "gps_lat": null, 
            "city_id": null, 
            "minint_regional_code": 1, 
            "regional_id": 1, 
            "id": 3, 
            "provincial_id": null, 
            "inhabitants": 4341733, 
            "minint_city_code": null, 
            "gps_lon": null, 
            "resource_uri": "/op/1.0/locations/3/", 
            "location_type": {
                "name": "Regione"
            }, 
            "minint_provincial_code": null
        }, 
        {
            "macroregional_id": 1, 
            "name": "Valle D'Aosta", 
            "gps_lat": null, 
            "city_id": null, 
            "minint_regional_code": 2, 
            "regional_id": 2, 
            "id": 4, 
            "provincial_id": null, 
            "inhabitants": 123978, 
            "minint_city_code": null, 
            "gps_lon": null, 
            "resource_uri": "/op/1.0/locations/4/", 
            "location_type": {
                "name": "Regione"
            }, 
            "minint_provincial_code": 4
        }, 


Example 3
^^^^^^^^^
Filters can be mixed. See  filters table above to check which filter can be used, when. Example below lists the five provinces in the Lazio region. 
::

    GET /1.0/locations/?location_type=provincia&regional_id=12

.. code-block:: python

    [
        {
            "macroregional_id": 3, 
            "name": "Viterbo", 
            "gps_lat": null, 
            "city_id": null, 
            "minint_regional_code": 12, 
            "regional_id": 12, 
            "id": 78, 
            "provincial_id": 56, 
            "inhabitants": 302547, 
            "minint_city_code": null, 
            "gps_lon": null, 
            "resource_uri": "/op/1.0/locations/78/", 
            "location_type": {
                "name": "Provincia"
            }, 
            "minint_provincial_code": 91
        }, 
        {
            "macroregional_id": 3, 
            "name": "Rieti", 
            "gps_lat": null, 
            "city_id": null, 
            "minint_regional_code": 12, 
            "regional_id": 12, 
            "id": 79, 
            "provincial_id": 57, 
            "inhabitants": 154406, 
            "minint_city_code": null, 
            "gps_lon": null, 
            "resource_uri": "/op/1.0/locations/79/", 
            "location_type": {
                "name": "Provincia"
            }, 
            "minint_provincial_code": 69
        }, 
        {
            "macroregional_id": 3, 
            "name": "Roma", 
            "gps_lat": null, 
            "city_id": null, 
            "minint_regional_code": 12, 
            "regional_id": 12, 
            "id": 80, 
            "provincial_id": 58, 
            "inhabitants": 3831959, 
            "minint_city_code": null, 
            "gps_lon": null, 
            "resource_uri": "/op/1.0/locations/80/", 
            "location_type": {
                "name": "Provincia"
            }, 
            "minint_provincial_code": 70
        }, 
        {
            "macroregional_id": 3, 
            "name": "Latina", 
            "gps_lat": null, 
            "city_id": null, 
            "minint_regional_code": 12, 
            "regional_id": 12, 
            "id": 81, 
            "provincial_id": 59, 
            "inhabitants": 524533, 
            "minint_city_code": null, 
            "gps_lon": null, 
            "resource_uri": "/op/1.0/locations/81/", 
            "location_type": {
                "name": "Provincia"
            }, 
            "minint_provincial_code": 40
        }, 
        {
            "macroregional_id": 3, 
            "name": "Frosinone", 
            "gps_lat": null, 
            "city_id": null, 
            "minint_regional_code": 12, 
            "regional_id": 12, 
            "id": 82, 
            "provincial_id": 60, 
            "inhabitants": 491333, 
            "minint_city_code": null, 
            "gps_lon": null, 
            "resource_uri": "/op/1.0/locations/82/", 
            "location_type": {
                "name": "Provincia"
            }, 
            "minint_provincial_code": 33
        }
    ]
    
    
Example 4
^^^^^^^^^
``namestartswith`` and ``name`` can be used to look for locations starting with or exactly matching a sequence of letters (case insensitive).
These filters can be used alone, working on the complete list, or together with other filters.
::

    GET /1.0/locations/?location_type=comune&regional_id=12namestartswith=san

.. code-block:: python

    [
        {
            "macroregional_id": 3, 
            "name": "Sant'Oreste", 
            "gps_lat": 42.235700000000001, 
            "city_id": 58099, 
            "minint_regional_code": 12, 
            "regional_id": 12, 
            "id": 5142, 
            "provincial_id": 58, 
            "inhabitants": 16727, 
            "minint_city_code": 980, 
            "gps_lon": 12.520300000000001, 
            "resource_uri": "/op/1.0/locations/5142/", 
            "location_type": {
                "name": "Comune"
            }, 
            "minint_provincial_code": 70
        }, 
        {
            "macroregional_id": 3, 
            "name": "San Cesareo", 
            "gps_lat": 41.821899999999999, 
            "city_id": 58119, 
            "minint_regional_code": 12, 
            "regional_id": 12, 
            "id": 5136, 
            "provincial_id": 58, 
            "inhabitants": 11707, 
            "minint_city_code": 931, 
            "gps_lon": 12.8165, 
            "resource_uri": "/op/1.0/locations/5136/", 
            "location_type": {
                "name": "Comune"
            }, 
            "minint_provincial_code": 70
        }, 
        ...
    ]

HTTP POST
*********
Not supported.

HTTP PUT
********
Not supported.

HTTP DELETE
***********
Not supported.
