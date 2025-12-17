from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def role_required(*roles):
    """
    @role_required("Owner") -> only Owner (and superuser)
    @role_required("Owner", "Employee") -> Owner + Employee (and superuser)
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            user = request.user

            # Superuser can do everything
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            # must be staff for management pages
            if not user.is_staff:
                return HttpResponseForbidden("Admins only.")

            user_roles = set(user.groups.values_list("name", flat=True))
            if any(r in user_roles for r in roles):
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("Insufficient role.")
        return _wrapped
    return decorator
