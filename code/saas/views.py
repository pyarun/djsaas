# Create your views here.

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from django.contrib.auth import REDIRECT_FIELD_NAME , login as auth_login
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url
from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.sites.models import get_current_site
from saas.forms import SaasAuthenticationForm


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='client_login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=SaasAuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
