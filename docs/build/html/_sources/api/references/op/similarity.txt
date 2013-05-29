.. _api-res-op-similarity:

==========
Similarity
==========

Openpolis politicians may be looked for by first_name, last_name and birth_date.
This is useful to integrate with other, external applications.

The criteria used to fetch similar politicians is:

 * same first_name and last_name, any birth_date
 * same first_name and birth_date, any last_name (if birth_date given)
 * same last_name and birth_date, any first_name (if birth_date given)

The criteria are alternative (OR).


Similarity list
+++++++++++++++
A Politicians list is returned, containing all the politicians that verify the similarity criteria.
The number of such results is returned if the `count=true` parameter is set.


Resource URI
************
::

   /1.0/similar_politicians

HTTP GET
********
Retrieves a list of the politicians verifying the similarity criteria, starting from the parameters.

List parameters
^^^^^^^^^^^^^^^
The following query string parameters alow to define the search and transfomr the results:

================= ====================================================================================
Parameter         Description
================= ====================================================================================
first_name        Politician's first name (needed)
last_name         Politician's last name (needed)
birth_date        Politician's birth date (not needed)
limit             limit to the number of results
count             returns only the number of results if set to 'true'
================= ====================================================================================

Default output is json, add ``?format=xml`` to get xml.



Example
^^^^^^^
Look for Mario Rossi, born on 1946-10-19
::

    GET /1.0/similar_politicians/?first_name=mario&last_name=rossi&birth_date=1946-10-19

.. code-block:: python

    [
        {
            first_name: "MARIO",
            last_name: "ARESCA",
            birt_location: "Mombercelli (AT)",
            charges: [
                "dal 06/07/2004 al 07/04/2008 Assessore Giunta Provinciale Asti (Partito: FI)",
                "dal 03/11/2010 al 06/05/2012 Consigliere Consiglio Comunale Asti (Lista elettorale: LISTA CIVICA) "
            ],
            op_id: 6202,
            api_link: "http://api.openpolis.it/op/1.0/politicians/6202",
            birth_date: "1946-10-19 00:00:00",
            op_link: "http://www.openpolis.it/politico/6202"
        },
        {
            first_name: "MARIO",
            last_name: "ROSSI",
            birt_location: "Arona (NO)",
            charges: [
                "dal 13/06/2004 al 06/06/2009 Consigliere Consiglio Comunale Massino Visconti (Lista elettorale: LISTA CIVICA) ",
                "dal 13/06/2004 al 06/06/2009 Assessore Giunta Comunale Massino Visconti (Partito: LISTA CIVICA)"
            ],
            op_id: 80378,
            api_link: "http://api.openpolis.it/op/1.0/politicians/80378",
            birth_date: "1946-10-19 00:00:00",
            op_link: "http://www.openpolis.it/politico/80378"
        },
        ...
    ]


Example 2
^^^^^^^^^
Count the number of results of example 1
::

    GET /1.0/similar_politicians/?first_name=mario&last_name=rossi&birth_date=1946-10-19&count=true

.. code-block:: python

    10

HTTP POST
*********
Not supported.

HTTP PUT
********
Not supported.

HTTP DELETE
***********
Not supported.
