.. _api-overview:

=============
API: Overview
=============


Credentials
-----------
Our REST API is served over HTTPS. To convey users' identity and ensure data policies, unencrypted HTTP is not supported.
::

    https://username:password@api.openpolis.it/op/resources/identifier

Base URLs
---------
All URLs referenced in the documentation have the following bases, that depends on the project you target.

The **openpolitici** project's API code is `op`
::

    https://username:password@api.openpolis.it/op/


The **openparlamento** project's API code is `opp`
::

    https://username:password@api.openpolis.it/opp/




Requests and responses
----------------------
.. toctree::
   :maxdepth: 2
   
   overview_requests
   overview_responses

About REST (REpresentational State Transfer)
--------------------------------------------
We designed the openpolis API in a very RESTful way, so that your consumption of it is simple and straightforward.

.. note:: From `Wikipedia <http://en.wikipedia.org/wiki/REST>`_

  REST's proponents argue that the Web's scalability and growth are a direct result of a few key design principles:

  * Application state and functionality are divided into resources
  * Every resource is uniquely addressable using a universal syntax for use in hypermedia links
  * All resources share a uniform interface for the transfer of state between client and resource, consisting of

    * A constrained set of well-defined operations
    * A constrained set of content types, optionally supporting code on demand
    * A protocol which is:
  
      * Client-server
      * Stateless
      * Cacheable
      * Layered
    
  REST's client/server separation of concerns simplifies component implementation, reduces the complexity of connector semantics, improves the effectiveness of performance tuning, and increases the scalability of pure server components. Layered system constraints allow intermediaries-proxies, gateways, and firewalls-to be introduced at various points in the communication without changing the interfaces between components, thus allowing them to assist in communication translation or improve performance via large-scale, shared caching. REST enables intermediate processing by constraining messages to be self-descriptive: interaction is stateless between requests, standard methods and media types are used to indicate semantics and exchange information, and responses explicitly indicate cacheability.

If you're looking for more information about RESTful web services, the `O'Reilly RESTful Web Services <http://www.amazon.com/RESTful-Web-Services-Leonard-Richardson/dp/0596529260>`_ book is an excellent choice.


