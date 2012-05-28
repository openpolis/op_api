.. _api-res-op-politicians:

===========
Politicians
===========

Openpolis politicians are the main subject of the openpolis archive. A politician may have different charges, in the past and at present time.

Politician instance
+++++++++++++++++++
A Politician instance resource represents a **single openpolis politician**.

Resource URI
************
::

   /1.0/politicians/{id}



Resource Properties
*******************
A Politician resource is identified by the following properties:

=============================  =======================================
property                       explanation
=============================  =======================================
:const:`content_id`            openpolis content identifier
:const:`first_name`            first name
:const:`last_name`             last name
:const:`birth_date`            birth date
:const:`birth_location`        birth location
:const:`profession`            profession
:const:`education_levels`      array of :ref:`education-levels`
:const:`institution_charges`   array of :ref:`institution-charges`
:const:`political_charges`     array of :ref:`political-charges`
:const:`organization_charges`  array of :ref:`organization-charges`
=============================  =======================================


.. _education-levels:

Education levels
^^^^^^^^^^^^^^^^
Represents the education levels of the politician. It may be more than one (although very rarely). A single level has the following properties:

=============================  =======================================
property                       explanation
=============================  =======================================
:const:`name`                  the name (Laurea, Licenza media, ...)
:const:`description`           some more detail about the level (Faculty, School, ...)
=============================  =======================================

.. _institution-charges:

Institution charges
^^^^^^^^^^^^^^^^^^^
Represents the institutional charges of the politician.  Charges are grouped by `current` (open) and `past` (closed). 
Current charges are sorted by the start date (most recent on top), past charges are sorted by end date (most recently closed on top).

A single charge has the following properties:

=============================  =======================================
property                       explanation
=============================  =======================================
:const:`date_start`            charge start date (yyyy-mm-dd)
:const:`date_end`              charge end date (yyyy-mm-dd)
:const:`description`           charge description
:const:`institution`           institution (Senato, Camera, ...)
:const:`charge_type`           charge type (Presidente, Deputato, ...)
:const:`location`              location name
:const:`location_id`           location id
:const:`group`                 group (if parliament, regional)
:const:`party`                 party of election
:const:`textual_rep`           a longer textual description
=============================  =======================================

.. _political-charges:

Political charges
^^^^^^^^^^^^^^^^^^^
Represents current or past political charges of the politician (in parties).
Sorting criteria match those explained above for institutional charges.

A single charge has the following properties:

=============================  =======================================
property                       explanation
=============================  =======================================
:const:`date_start`            charge start date (yyyy-mm-dd)
:const:`date_end`              charge end date (yyyy-mm-dd)
:const:`description`           charge description
:const:`charge_type`           charge type (carica, iscritto)
:const:`location`              location name
:const:`location_id`           location id
:const:`party`                 party of election
:const:`textual_rep`           a longer textual description
=============================  =======================================

.. _organization-charges:

Organization charges
^^^^^^^^^^^^^^^^^^^^
Represents the charges that the politician has or has had in organizations (non-institutional, non-political).
Sorting criteria match those explained above for institutional charges.

A single charge has the following properties:

=============================  =======================================
property                       explanation
=============================  =======================================
:const:`date_start`            charge start date (yyyy-mm-dd)
:const:`date_end`              charge end date (yyyy-mm-dd)
:const:`charge_name`           name of the charge
:const:`organization`          name of the organization
:const:`textual_rep`           a longer textual description
=============================  =======================================


HTTP GET
********
Returns a representation of a single politician, including the properties above. Associated arrays are exploded. 


JSON Example
^^^^^^^^^^^^
::

    GET op/1.0/politicians/204

.. code-block:: python

    {
        "first_name": "Silvio", 
        "last_name": "BERLUSCONI", 
        "organization_charges": {
            "current": [], 
            "past": [
                {
                    "organization": "fininvest", 
                    "date_end": "1995-01-01", 
                    "date_start": "1989-01-01", 
                    "charge_name": "presidente", 
                    "textual_rep": "dal 1989 al 1995 è stato presidente fininvest (http://www.fininvest.it/)"
                }
            ]
        }, 
        "birth_location": "Milano (MI)", 
        "education_levels": [
            {
                "name": "Laurea", 
                "descr": "Giurisprudenza"
            }
        ], 
        "profession": "Imprenditore", 
        "political_charges": {
            "current": [
                {
                    "charge_type": "carica", 
                    "description": "Presidente", 
                    "textual_rep": "dal 2009 è Presidente - Popolo della Libertà", 
                    "date_end": null, 
                    "date_start": "2009-01-01", 
                    "location": "Italia", 
                    "party": "Popolo della Libertà", 
                    "location_id": 2
                }
            ], 
            "past": [
                {
                    "charge_type": "carica", 
                    "description": "Presidente", 
                    "textual_rep": "dal 1994 al 2009 è stato Presidente - Forza Italia", 
                    "date_end": "2009-01-01", 
                    "date_start": "1994-01-01", 
                    "location": "Italia", 
                    "party": "FORZA ITALIA", 
                    "location_id": 2
                }
            ]
        }, 
        "institution_charges": {
            "current": [
                {
                    "charge_type": "Deputato", 
                    "group": "Popolo della Libertà", 
                    "description": "", 
                    "textual_rep": "dal 29/04/2008 Deputato(Gruppo: PdL) ", 
                    "date_end": null, 
                    "date_start": "2008-04-29", 
                    "location": "Italia", 
                    "party": "NON SPECIFICATO", 
                    "location_id": 2, 
                    "institution": "Camera dei Deputati"
                }, 
                {
                    "charge_type": "Presidente del Consiglio", 
                    "group": "Non specificato", 
                    "description": "", 
                    "textual_rep": "dal 08/05/2008 Pres. del Consiglio (Partito: PdL)", 
                    "date_end": null, 
                    "date_start": "2008-05-08", 
                    "location": "Italia", 
                    "party": "Popolo della Libertà", 
                    "location_id": 2, 
                    "institution": "Governo Nazionale"
                }
            ], 
            "past": [
                {
                    "charge_type": "Deputato", 
                    "group": "Forza Italia", 
                    "description": null, 
                    "textual_rep": "dal 28/04/2006 al 28/04/2008 Deputato(Gruppo: FI) ", 
                    "date_end": "2008-04-28", 
                    "date_start": "2006-04-28", 
                    "location": "Italia", 
                    "party": "FORZA ITALIA", 
                    "location_id": 2, 
                    "institution": "Camera dei Deputati"
                }, 
                {
                    "charge_type": "Presidente del Consiglio", 
                    "group": "Non specificato", 
                    "description": "", 
                    "textual_rep": "dal 11/06/2001 al 11/02/2006 Pres. del Consiglio (Partito: FI)", 
                    "date_end": "2006-02-11", 
                    "date_start": "2001-06-11", 
                    "location": "Italia", 
                    "party": "FORZA ITALIA", 
                    "location_id": 2, 
                    "institution": "Governo Nazionale"
                }, 
                {
                    "charge_type": "Ministro", 
                    "group": "Non specificato", 
                    "description": "Min. Affari esteri (ad interim)", 
                    "textual_rep": "dal 07/01/2002 al 13/11/2002 Ministro Min. Affari esteri (ad interim)(Partito: FI)", 
                    "date_end": "2002-11-13", 
                    "date_start": "2002-01-07", 
                    "location": "Italia", 
                    "party": "FORZA ITALIA", 
                    "location_id": 2, 
                    "institution": "Governo Nazionale"
                }, 
                {
                    "charge_type": "Ministro", 
                    "group": "Non specificato", 
                    "description": "Min. Economia e Finanze (ad interim)", 
                    "textual_rep": "dal 04/07/2004 al 16/07/2004 Ministro Min. Economia e Finanze (ad interim)(Partito: FI)", 
                    "date_end": "2004-07-16", 
                    "date_start": "2004-07-04", 
                    "location": "Italia", 
                    "party": "FORZA ITALIA", 
                    "location_id": 2, 
                    "institution": "Governo Nazionale"
                }, 
                {
                    "charge_type": "Presidente del Consiglio", 
                    "group": "Non specificato", 
                    "description": "", 
                    "textual_rep": "dal 11/05/1994 al 17/01/1995 Pres. del Consiglio (Partito: FI)", 
                    "date_end": "1995-01-17", 
                    "date_start": "1994-05-11", 
                    "location": "Italia", 
                    "party": "FORZA ITALIA", 
                    "location_id": 2, 
                    "institution": "Governo Nazionale"
                }, 
                {
                    "charge_type": "Consigliere", 
                    "group": "Non specificato", 
                    "description": "", 
                    "textual_rep": "dal 09/06/2006 al 21/05/2008 Consigliere Consiglio Comunale Milano (Lista elettorale: FI) ", 
                    "date_end": "2008-05-21", 
                    "date_start": "2006-06-09", 
                    "location": "Milano", 
                    "party": "FORZA ITALIA", 
                    "location_id": 1974, 
                    "institution": "Consiglio Comunale"
                }, 
                {
                    "charge_type": "Deputato", 
                    "group": "Non specificato", 
                    "description": null, 
                    "textual_rep": "dal 30/05/2001 al 27/04/2006 Deputato", 
                    "date_end": "2006-04-27", 
                    "date_start": "2001-05-30", 
                    "location": "Italia", 
                    "party": "NON SPECIFICATO", 
                    "location_id": 2, 
                    "institution": "Camera dei Deputati"
                }, 
                {
                    "charge_type": "Deputato", 
                    "group": "Non specificato", 
                    "description": null, 
                    "textual_rep": "dal 09/05/1996 al 29/05/2001 Deputato", 
                    "date_end": "2001-05-29", 
                    "date_start": "1996-05-09", 
                    "location": "Italia", 
                    "party": "NON SPECIFICATO", 
                    "location_id": 2, 
                    "institution": "Camera dei Deputati"
                }, 
                {
                    "charge_type": "Deputato", 
                    "group": "Non specificato", 
                    "description": null, 
                    "textual_rep": "dal 15/04/1994 al 08/05/1996 Deputato", 
                    "date_end": "1996-05-08", 
                    "date_start": "1994-04-15", 
                    "location": "Italia", 
                    "party": "NON SPECIFICATO", 
                    "location_id": 2, 
                    "institution": "Camera dei Deputati"
                }
            ]
        }, 
        "birth_date": "1936-09-29 00:00:00", 
        "content_id": "204", 
        "resources": [
            {
                "type": "Email ufficiale", 
                "value": "BERLUSCONI_S@camera.it", 
                "descr": "mail personale Camera Dep."
            }, 
            {
                "type": "Altra Email", 
                "value": "s.berlusconi@forzaitalia.it", 
                "descr": ""
            }
        ]
    }


HTTP POST
*********
Not yet supported. To be done in the future.

HTTP PUT
********
Not supported.

HTTP DELETE
***********
Not supported.



Politicians list
++++++++++++++++

Resource URI
************
::

   /1.0/politicians

HTTP GET
********
Retrieves a list of the Locations resources.

List filters
^^^^^^^^^^^^
The following query string parameters allow you to limit the list returned:

================= ====================================================================================
Parameter         Description
================= ====================================================================================
institution       Only return Politicians of the given institution. If local institution, location must be specified, too
institution_id    Only return Politicians of the institution having the given institution_id (see table below)
location_id       Specifies the location for a local institution
================= ====================================================================================

Institutions
^^^^^^^^^^^^
===== ============================
id    name                        
===== ============================
1     Commissione Europea         
2     Parlamento Europeo          
3     Governo Nazionale           
4     Camera dei Deputati         
5     Senato della Repubblica     
6     Giunta Regionale            
7     Consiglio Regionale         
8     Giunta Provinciale          
9     Consiglio Provinciale       
10    Giunta Comunale             
11    Consiglio Comunale          
12    Commissariamento            
13    Presidenza della Repubblica 
===== ============================

Example 1
^^^^^^^^^
National institution: the national government
::

    GET /1.0/politicians/?institution=Governo%20Nazionale

.. code-block:: python

    [
        {
            "first_name": "Silvio", 
            "last_name": "BERLUSCONI", 
            "birt_location": "Milano (MI)", 
            "textual_rep": "dal 08/05/2008 Pres. del Consiglio (Partito: PdL)", 
            "date_end": null, 
            "date_start": "2008-05-08", 
            "charge": "Presidente del Consiglio", 
            "op_id": 204, 
            "birth_date": "1936-09-29 00:00:00", 
            "party": "PdL", 
            "op_link": "http://www.openpolis.it/politico/204"
        }, 
        {
            "first_name": "Raffaele", 
            "last_name": "FITTO", 
            "birt_location": "Maglie (LE)", 
            "textual_rep": "dal 08/05/2008 Ministro Rapporti con le regioni(Partito: PdL)", 
            "date_end": null, 
            "date_start": "2008-05-08", 
            "charge": "Ministro", 
            "op_id": 411, 
            "birth_date": "1969-08-28 00:00:00", 
            "party": "PdL", 
            "op_link": "http://www.openpolis.it/politico/411"
        }, 
        {
            "first_name": "Angelino", 
            "last_name": "ALFANO", 
            "birt_location": "Agrigento (AG)", 
            "textual_rep": "dal 08/05/2008 Ministro Giustizia(Partito: PdL)", 
            "date_end": null, 
            "date_start": "2008-05-08", 
            "charge": "Ministro", 
            "op_id": 167, 
            "birth_date": "1970-10-31 00:00:00", 
            "party": "PdL", 
            "op_link": "http://www.openpolis.it/politico/167"
        }, 
        ...
    ]


Example 2
^^^^^^^^^
Local institution: the Rome city government
::

    GET /1.0/politicians/?institution=Giunta%20Comunale&location_id=5132

.. code-block:: python

    [
        {
            "first_name": "Giovanni", 
            "last_name": "ALEMANNO", 
            "birt_location": "Bari (BA)", 
            "textual_rep": "dal 29/04/2008 Sindaco Giunta Comunale Roma (Partito: PdL)", 
            "date_end": null, 
            "date_start": "2008-04-29", 
            "charge": "Sindaco", 
            "op_id": 165, 
            "birth_date": "1958-03-03 00:00:00", 
            "party": "PdL", 
            "op_link": "http://www.openpolis.it/politico/165"
        }, 
        {
            "first_name": "Mauro", 
            "last_name": "CUTRUFO", 
            "birt_location": "Roma (RM)", 
            "textual_rep": "dal 14/01/2011 Vicesindaco Giunta Comunale Roma (Partito: PdL)", 
            "date_end": null, 
            "date_start": "2011-01-14", 
            "charge": "Vicesindaco", 
            "op_id": 1536, 
            "birth_date": "1956-09-09 00:00:00", 
            "party": "PdL", 
            "op_link": "http://www.openpolis.it/politico/1536"
        }, 
        {
            "first_name": "FABRIZIO", 
            "last_name": "GHERA", 
            "birt_location": "Roma (RM)", 
            "textual_rep": "dal 14/01/2011 Assessore Giunta Comunale Roma (Partito: PdL)", 
            "date_end": null, 
            "date_start": "2011-01-14", 
            "charge": "Assessore", 
            "op_id": 125702, 
            "birth_date": "1971-12-06 00:00:00", 
            "party": "PdL", 
            "op_link": "http://www.openpolis.it/politico/125702"
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
