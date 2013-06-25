# Create your views here.
from django.shortcuts import render

from django.contrib.sites.models import RequestSite


def user_home(request):
    """
        Renders Users home page. Content will be based on the permissions users have on the tenant data
    """
    context = dict()
    return render(request, 'user_home.html', context)
