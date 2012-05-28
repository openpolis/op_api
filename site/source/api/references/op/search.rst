.. _api-res-op-search:

===================
Search in Openpolis
===================

Search functionality allows to search through politicians and locations.

Resource URI
************
::

   /1.0/search

HTTP GET
********
Retrieves a list of Locations and Politicians that contains the string in the ``q`` parameter.

List filters
^^^^^^^^^^^^
The following query string parameters allow you to define the search

================= ====================================================================================
Parameter         Description
================= ====================================================================================
q                 the sequence of characters to look for; must be longer than 3 characters
================= ====================================================================================

The results list contains all politicians and locations that have the sequence.
Results are grouped by politicians and locations.

Results are sorted by textual relevance of the sequence in the string. If the sequence is the string,
then the result is shown first. If the sequence is a small part of the string, then it's shown last.

Example 1
^^^^^^^^^
Look for items containing the sequence ``roma``
::

    GET /1.0/politicians/?q=roma

.. code-block:: python

    {
        "politicians": [
            [
                23496, 
                "ROMANO ROMANO, nato a Telese Terme (BN) il 1969-10-02"
            ], 
            [
                308790, 
                "Romano Romani, nato a Orciano Di Pesaro (PS) il 1956-12-29"
            ], 
            [
                37355, 
                "UGO ROMANO, nato a Gioia Sannitica (CE) il 1949-10-14"
            ], 
            [
                29684, 
                "ROMAN MAYR, nato a PLAUS il 1958-10-29"
            ], 
            ...
        ],
        "locations": [
            [
                5132, 
                "Comune di Roma"
            ], 
            [
                80, 
                "Provincia di Roma"
            ], 
            [
                7377, 
                "Comune di Romana"
            ], 
            [
                3143, 
                "Comune di Romallo"
            ], 
            ...
        ]
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
