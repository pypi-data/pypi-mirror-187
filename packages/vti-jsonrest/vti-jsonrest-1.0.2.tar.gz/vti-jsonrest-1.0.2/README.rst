JSONREST
========

JSONREST is a client library for discoverable REST APIs using JSON payloads.

.. code-block:: python

    >>> import jsonrest
    >>> j = jsonrest.JSONREST('http://example/')
    >>> dir(j)
    ['foo', 'bar', 'baz']
    >>> j.foo
    JSONREST('http://example/foo/', ['x', 'y', 'z'])
    >>> j.foo.x = 42
    >>> print(j.foo.x)
    42


JSONREST exposes the REST API as an object-oriented interface, with the object hierarchy mirroring the directory structure of the URLs. In order to make this work, it depends on the server responding to GET requests on directories with a JSON array containing all available API endpoints (or other directories) that reside there, with directories identified by a trailing forward-slash (/).

Installing
----------

JSONREST is available on `PyPI <https://pypi.org/project/vti-jsonrest/>`_:

.. code-block:: sh

    $ python -m pip install vti-jsonrest

Documentation
-------------

Full documentation is available at `jsonrest.readthedocs.io <https://jsonrest.readthedocs.io/>`_.

Supported Versions
------------------

JSONREST officially supports Python 2.7 & 3.6+.

Features
--------
* Makes REST APIs behave like a normal python object
* Supports tab-completion in REPLs and Jupyter notebooks
* Keep-Alive & Connection Pooling
