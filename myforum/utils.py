from django.contrib.auth.views import login
from django.utils.translation import ugettext as _
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME


def login_view(request):
    '''non-redirect version login view function'''
    defaults = {
        'template_name': 'admin/login.html',
        'authentication_form': AdminAuthenticationForm,
        'extra_context': {
            'title': _('Log in'),
            'app_path': request.get_full_path(),
            REDIRECT_FIELD_NAME: request.get_full_path(),
        },
    }
    return login(request, **defaults)

def login_required(view_func):
    '''non-redirect version login_required decorator'''
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        return login_view(request)
    return _wrapped_view
