'''
Created on 24-Jun-2013

@author: arun
'''
from django.conf.urls import patterns, include, url
from saas.forms import SaasAuthenticationForm

urlpatterns = patterns("",
    
        url("^login$", "accounts.views.client_login", name="client_login"),
        
        url("^dlogin$", "django.contrib.auth.views.login", {"template_name":"client_login.html", "authentication_form":SaasAuthenticationForm}, name="dlogin")

)