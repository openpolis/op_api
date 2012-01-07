from piston.decorator import decorator
from piston.utils import rc

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
