'''
.. include:: ../README.rst
'''
__version__ = "1.0.0"
import requests

class JSONREST(object):
    """A class providing access to discoverable REST APIs using JSON payloads. The REST server must respond to GET requests on directories with an array containing the names of the available properties and subdirectories within it.

The directory names in the URIs are converted into a nested tree of JSONREST objects, in which each endpoint URI is available as a class instance attribute. All payloads use JSON, and Python data types are automatically converted back and forth from JSON.

To do a PUT of the value 42 to the URI http://example/foo/bar, then perform a GET on the same URI and print the result, do the following:

.. code-block:: python

    rest = JSONREST('http://example/')
    rest.foo.bar = 42
    print(rest.foo.bar)

In interactive interpreters such as ipython or jupyter notebooks, the available URIs are discoverable via tab-completion.
"""
    def __init__(self, base, members=None, session=None):
        # Type (str, list[str], requests.Session)
        """
:param base: The top-level base URI at which the API is hosted.
:param members: The names of subdirectories and properties available at the base URI. This will be queried from the API if not specified.
:param session: The requests session to perform all HTTP operations with. Reusing the same session for all connections to the same host minimizes overhead.

        """
        self._base = base
        if not self._base.endswith('/'):
            self._base += '/'
        if session is None:
            self._session = requests.Session()
            self._session.headers.update({'Accept': 'application/json'})
        else:
            self._session = session
        if members is None:
            self._dir = self.get('')
        else:
            self._dir = members
        self._dircache = {}

    def put(self, uri, data):
        # Type (str, Any) -> None
        """Perform a PUT.

:param uri: The URI to perform the PUT on, relative to the base path of this object.
:param data: The data to send; it will be converted to JSON then included as the message body.

        """
        resp = self._session.put(self._base + uri, json=data)
        resp.raise_for_status()

    def get(self, uri):
        # Type (str) -> Any
        """Perform a GET.

:param uri: The URI to perform the GET on, relative to the base path of this object.

:return The message body of the response, converted from json to native python data types.
        """
        resp = self._session.get(self._base + uri)
        resp.raise_for_status()
        return resp.json()

    def _child(self, name, members):
        # Type (str, list[str]) -> JSONREST
        """Construct a new `JSONREST` object representing a subdirectory of this one.

:param name: The name of the subdirectory.
:param members: The names of items within the subdirectory.

        """
        return JSONREST(self._base + name + '/', members, self._session)

    def __getattr__(self, name):
        if name in self._dircache:
            return self._dircache[name]
        result = self.get(name)
        asdir = name+'/' if not name.endswith('/') else name
        if asdir in self._dir:
            self._dircache[name] = self._child(name, result)
            return self._dircache[name]
        return result

    def __setattr__(self, name, val):
        if name.startswith('_'):
            return object.__setattr__(self, name, val)
        return self.put(name, val)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'JSONREST({}, {})'.format(repr(self._base), repr(self._dir))

    def __iter__(self):
        for i in dir(self):
            yield getattr(self, i)

    def __dir__(self):
        return [member.strip('/') for member in self._dir]

    def __contains__(self, value):
        return value in self._dir or (value+'/') in self._dir

class VTIInstrumentError(Exception):
    """A base class representing the types of errors raised by VTI Instruments REST APIs."""
    def __init__(self, arg):
        Exception.__init__(self, arg)

class VTIInstrumentErrorMessage(VTIInstrumentError):
    """An error object returned from a VTI Instruments REST API, with a fully populated error message.

:ivar message: The error message.
:ivar error_code: The numerical error code
:ivar resource: The URI that the error was raised by
    """
    def __init__(self, message, error_code, resource):
        # Type (str, int, str)
        VTIInstrumentError.__init__(self, {'message': message, 'error_code': error_code, 'resource': resource})
        self.message = message
        self.error_code = error_code
        self.resource = resource

    def __str__(self):
        code = self.error_code
        if code < 0:
            code += 0x100000000
        return 'Instrument Error 0x{:08x} for {}: {}'.format(code, self.resource, self.message)

class VTIInstrumentErrorArgs(VTIInstrumentError):
    """An error object returned from a VTI Instruments REST API, with arguments that can be used to fill in an error message template.

    In order to construct the full error message, find the message associated with `error_code`, and replace each "%s" in it with the next member of `args`.

:ivar args: The arguments for filling in the error message template
:ivar error_code: The numerical error code
:ivar resource: The URI that the error was raised by

    """
    def __init__(self, args, error_code, resource):
        # Type (list[str], int, str)
        VTIInstrumentError.__init__(self, {'args': args, 'error_code': error_code, 'resource': resource})
        self.args = args
        self.error_code = error_code
        self.resource = resource

    def __str__(self):
        code = self.error_code
        if code < 0:
            code += 0x100000000
        return 'Instrument Error 0x{:08x} for {} with message args {}'.format(code, self.resource, self.args)

class VTIREST(JSONREST):
    """Wraps the :py:class:`JSONREST` class to provide easier access to the JSON-REST APIs of VTI Instruments products.

Constructs the proper base URI for a certain slot name automatically, and properly handles the HTTP 240 status code that VTI Instruments products use to indicate an error, querying the error queue and raising a :py:class:`VTIInstrumentError` exception using the result.

For example, to print the serial number of a card in slot 2 of a controller at hostname "my-inst", do the following:

.. code-block:: python

    slot2 = VTIREST('my-inst', 'slot0_2')
    print(slot2.common.serial)
    """
    def __init__(self, host, slot='inst0', path='', members=None, session=None): # pylint: disable=too-many-arguments
        # Type (str, str, str, list[str], requests.Session)
        """
:param host: The hostname or IP address of the instrument.
:param slot: The slot name of the subinstrument. For non-modular products, the default of "inst0" should be used.
:param path: The subdirectory in the REST API to use.
:param members: The names of subdirectories and properties available at the specified path. This will be queried from the API if not specified.
:param session: The requests session to perform all HTTP operations with. Reusing the same session for all connections to the same host minimizes overhead.

        """
        if not path.endswith('/'):
            path += '/'
        self._host = host
        self._slot = slot
        self._path = path
        JSONREST.__init__(self, 'http://{}/card/{}/{}'.format(host, slot, path), members, session)

    def _child(self, name, members):
        # Type (str, list[str]) -> VTIREST
        """Construct a new `VTIREST` object representing a subdirectory of this one.

:param name: The name of the subdirectory
:param members: The names of items within the subdirectory

        """
        return VTIREST(self._host, self._slot, self._path + name, members, self._session)

    def _check_error(self):
        # Type () -> None
        """Check the error queue for the connected instrument slot. If there is an item in the queue, it will be removed, and a :py:class:`VTIInstrumentError` will be raised containing the details.

:raise jsonrest.VTIInstrumentError: The next item from the error queue, if any.
        """
        queue = VTIREST(self._host, self._slot, 'common/error_queue', session=self._session)
        if 'next_entry_message' in queue:
            err = queue.next_entry_message
            if err:
                raise VTIInstrumentErrorMessage(**err)
        else:
            err = queue.next_entry
            if err:
                raise VTIInstrumentErrorArgs(**err)

    def get(self, uri):
        # Type (str) -> Any
        """Perform a GET, querying the error queue and raising an exception if necessary.

:param uri: The URI to perform the GET on, relative to the base path of this object.

:return The message body of the response, converted from json to native python data types.

:raise jsonrest.VTIInstrumentError: When the HTTP status is 240, the next item in the instrument error queue will be raised as a child class of this type.
        """
        resp = self._session.get(self._base + uri)
        resp.raise_for_status()
        if resp.status_code == 240:
            self._check_error()
        return resp.json()

    def put(self, uri, data):
        # Type (str, Any) -> None
        """Perform a PUT, querying the error queue and raising an exception if necessary.

:param uri: The URI to perform the PUT on, relative to the base path of this object.
:param data: The data to send; it will be converted to JSON then included as the message body.

:raise jsonrest.VTIInstrumentError: When the HTTP status is 240, the next item in the instrument error queue will be raised as a child class of this type.
        """
        resp = self._session.put(self._base + uri, json=data)
        resp.raise_for_status()
        if resp.status_code == 240:
            self._check_error()

    def __repr__(self):
        return 'VTIREST({}, {}, {}, {})'.format(repr(self._host), repr(self._slot), repr(self._path), repr(self._dir))
