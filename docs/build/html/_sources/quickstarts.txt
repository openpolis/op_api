.. _quickstart:

=================
Quickstart Guides
=================

To query our API you need to authenticate.

You can ask us by writing to ``lab [chiocciola] openpolis [punto] it`` and we'll send your username and password along.

Suppose you've done it and we've sent you the following auth tokens:

================= ====================================================================================
Username          Password
================= ====================================================================================
user              pass
================= ====================================================================================


Then you should really tell us we're dumb weirdos, but wait, take it easy, it's just an example!

---------------
Access examples
---------------

The API is accessed trough python's `request <http://docs.python-requests.org/en/latest/>`_ in the following examples,
but ruby's `rest-client <https://github.com/rest-client/rest-client>`_ or any other equivalent packages in smarter or dumber
languages would fit.

.. code-block:: python

    >>> import requests
    >>> r = requests.get('http://localhost:8001/op/1.0/decisionmakers/?context=sindaci&location_id=21', auth=('user', 'pass'))
    >>> results = r.json()
    >>> results['n_results']
    339



