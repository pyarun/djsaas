# Create your views here.
from django.shortcuts import render

from django.contrib.sites.models import RequestSite


def client_login(request):
    """
        Renders the login page for tenant Users
    """
    print request.tenant
    context = dict()
    req= RequestSite(request)
    
    return render(request, "client_login.html", context)