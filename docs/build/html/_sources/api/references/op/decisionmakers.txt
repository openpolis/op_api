.. _api-res-op-decisionmakers:

===============
Decision Makers
===============
Openpolis decisionmakers returns a list of charges, along with their personal identities and contacts.
The list may be filtered through ``context`` and ``location`` and is sorted by charge relevancies.
It is used in the Openpolis Campaign Application.

The resource only returns a read-only list of decisionmakers, there is no single instance API.

Decision makers list
++++++++++++++++++++

Resource URI
************
::

   /1.0/decisionmakers

HTTP GET
********
Retrieves a list of the decisionmakers resources.

List filters
^^^^^^^^^^^^
The following query string parameters allow you to limit the list returned:

================= ====================================================================================
Parameter         Description
================= ====================================================================================
context           Filter by a given context (or charge type). See specifications below for possible values
location_id       Filter by location. ``location_id`` matches the ``location`` API.
offset            Starts the results slice from ``offset``.
limit             Only return ``limit`` results (starting from ``offset``).
================= ====================================================================================

In all examples below, resources are sorted by charge priorities.
Default ``limit`` is set to 20. Default ``offset`` to 0.
Default output is json, add ``?format=xml`` to get xml.

Results have a meta section, with the total number of results, the current offset and limit,
and links to the next page or the previous, when needed.
The paginator links are built by ``offset`` manipulation.

Contexts
^^^^^^^^

These are the possible values for the contexts. Each of the values in a single line identifies a context.
This to allow flexibility in the API usage.

* pres-della-repubblica
* pres-del-consiglio
* ministro, ministri
* euro-commissario
* euro-deputato, euro-deputati
* deputato, deputati
* senatore, senatori
* governatore, governatori
* assessore-reg, assessore-regionale, assessori-regionali
* consigliere-reg, consigliere-regionale, consiglieri-regionali
* pres-prov, presidente-della-provincia, presidenti-della-provincia
* assessore-prov, assessore-provinciale, assessori-provinciali
* consigliere-prov, consigliere-provinciale, consiglieri-provinciali
* sindaco, sindaci
* assessore-com, assessore-comunale, assessori-comunali
* consigliere-com, consigliere-comunale, consiglieri-comunali
* commissario, commissari


Example 1 - Trivial
^^^^^^^^^^^^^^^^^^^
The list of all the decision makers. It is actually limited to the top 20 brasses.
::

    GET /1.0/decisionmakers/

.. code-block:: javascript

    {
        "n_results": 159915,
        "offset": 0,
        "limit": 20,
        "members": [
            {
                "op_charge_id": 688897,
                "politician_uri": "http://localhost:8001/op/1.0/politicians/1657",
                "politician": {
                    "first_name": "Giorgio",
                    "last_name": "NAPOLITANO",
                    "birth_location": "Napoli (NA)",
                    "op_politician_id": 1657,
                    "sex": "M",
                    "birth_date": "1925-06-29T00:00:00",
                    "resources": [
                        {
                            "type": "URL ufficiale",
                            "value": "http://www.senato.it/leg/15/BGT/Schede/Attsen/00001672.htm",
                            "descr": "pagina personale sito Senato"
                        },
                        {
                            "type": "Email ufficiale",
                            "value": "napolitano_g@posta.senato.it",
                            "descr": "mail personale Senato"
                        },
                        {
                            "type": "Twitter",
                            "value": "ITALYPRESIDENT",
                            "descr": ""
                        }
                    ]
                },
                "description": "",
                "textual_rep": "dal 22/04/2013 Pres. della Repubblica",
                "date_end": null,
                "date_start": "2013-04-22",
                "institution": "Presidenza della Repubblica",
                "charge": "Presidente della Repubblica",
                "location": "Italia",
                "party": "Non specificato",
                "location_type": "Italia",
                "op_link": "http://politici.openpolis.it/politico/1657"
            },
            { ... },
            ...
        ],
        "next": "http://localhost:8001/op/1.0/decisionmakers/?offset=20"
    }

Example 2 - Simple
^^^^^^^^^^^^^^^^^^
The list of all the ministers in the government.
::

    GET /1.0/decisionmakers/?context=ministri

.. code-block:: javascript

    {
        "n_results": 21,
        "offset": 0,
        "limit": 20,
        "members": [
            {
                "op_charge_id": 689048,
                "politician_uri": "http://localhost:8001/op/1.0/politicians/167",
                "politician": {
                    "first_name": "Angelino",
                    "last_name": "ALFANO",
                    "birth_location": "Agrigento (AG)",
                    "op_politician_id": 167,
                    "sex": "M",
                    "birth_date": "1970-10-31T00:00:00",
                    "resources": [
                        {
                            "type": "URL ufficiale",
                            "value": "http://www.camera.it/cartellecomuni/leg15/include/contenitore_dati.asp?tipopagina=&deputato=d300431&source=%2Fdeputatism%2F240%2Fdocumentoxml%2Easp&position=DeputatiLa%20Scheda%20Personale&Pagina=Deputati/Composizione/SchedeDeputati/SchedeDeputati.asp%3Fd",
                            "descr": "pagina personale sito Camera"
                        },
                        {
                            "type": "Email ufficiale",
                            "value": "ALFANO_A@CAMERA.IT",
                            "descr": "mail personale Camera Dep."
                        },
                        {
                            "type": "URL ufficiale",
                            "value": "http://www.angelinoalfano.it/",
                            "descr": "Sito personale"
                        },
                        {
                            "type": "Twitter",
                            "value": "angealfa",
                            "descr": ""
                        },
                        {
                            "type": "Facebook",
                            "value": "http://www.facebook.com/angelinoalfano.it",
                            "descr": ""
                        }
                    ]
                },
                "description": "Interno",
                "textual_rep": "dal 28/04/2013 Ministro Interno(Partito: PdL)",
                "date_end": null,
                "date_start": "2013-04-28",
                "institution": "Governo Nazionale",
                "charge": "Ministro",
                "location": "Italia",
                "party": "PdL",
                "location_type": "Italia",
                "op_link": "http://politici.openpolis.it/politico/167"
            },
            { ... },
            ...
        ],
        "next": "http://localhost:8001/op/1.0/decisionmakers/?context=ministri&offset=20"
    }


Example 3 - Advanced
^^^^^^^^^^^^^^^^^^^^
The list of all the sindaci in the region of Sicily.
::

    GET /1.0/decisionmakers/?context=sindaci&

.. code-block:: javascript

    {
        "n_results": 339,
        "offset": 0,
        "limit": 20,
        "members": [
            {
                "op_charge_id": 646728,
                "politician_uri": "http://localhost:8001/op/1.0/politicians/646727",
                "politician": {
                    "first_name": "Maria Teresa",
                    "last_name": "Collica",
                    "birth_location": "Barcellona Pozzo di Gotto(ME)",
                    "op_politician_id": 646727,
                    "sex": "F",
                    "birth_date": "1970-04-30T00:00:00",
                    "resources": []
                },
                "description": "",
                "textual_rep": "dal 24/05/2012 Sindaco Giunta Comunale Barcellona Pozzo di Gotto (Partito: Lista Civica - Cen-Sin)",
                "date_end": null,
                "date_start": "2012-05-24",
                "institution": "Giunta Comunale",
                "charge": "Sindaco",
                "location": "Barcellona Pozzo di Gotto",
                "party": "Lista Civica - Cen-Sin",
                "location_type": "Comune",
                "op_link": "http://politici.openpolis.it/politico/646727"
            },
            { ... },
            ...
        ],
        "next": "http://localhost:8001/op/1.0/decisionmakers/?location_id=21&context=sindaci&offset=20"
    }


HTTP POST
*********
Not supported.

HTTP PUT
********
Not supported.

HTTP DELETE
***********
Not supported.
