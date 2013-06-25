'''
Created on 24-Jun-2013

@author: arun
'''
from django.conf.urls import patterns, include, url

urlpatterns = patterns("",
        
        url("^home$", "accounts.views.user_home", name="user_home_page"),
    
#         url("^login$", "accounts.views.client_login", name="client_login"),
#         
#         url("^dlogin$", "saas.views.login", {"template_name":"client_login.html", "authentication_form":SaasAuthenticationForm}, name="dlogin")

)