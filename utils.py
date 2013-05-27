from piston.decorator import decorator
from piston.utils import rc

from urlparse import parse_qs, urlsplit, urlunsplit
from urllib import urlencode


def require_permission(permission):
    """permission may be: add, change, delete
    this decorator checks that the currently logged user has the right permissions
    """
    @decorator
    def wrap(f, self, request, *a, **kwa):
        # get module name (op_mailer)
        app = self.model.__module__.split(".")[0]
        
        # get model name (lowered class name)
        model = self.model().__class__.__name__.lower()
        
        # build permission string (es: 'op_mailer.add_application')
        permission_complete_name = "%s.%s_%s" % (app, permission, model)
        
        # verify permission, or return a piston built-in response
        if request.user.has_perm(permission_complete_name):
            return f(self, request, *a, **kwa)
        else:
            resp = rc.FORBIDDEN
            msg = ": The logged user cannot %s a(n) %s" % (permission, model)
            resp.write(msg)
            return resp
    return wrap

def set_query_parameter(url, param_name, param_value):
    """Given a URL, set or replace a query parameter and return the
    modified URL.

    >>> set_query_parameter('http://example.com?foo=bar&biz=baz', 'foo', 'stuff')
    'http://example.com?foo=stuff&biz=baz'

    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))