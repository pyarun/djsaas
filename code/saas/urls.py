'''
Created on 24-Jun-2013

@author: arun
'''
from django.conf.urls import patterns, include, url

urlpatterns = patterns("",
    
        url("^login$", "saas.views.login", name="tenant_login")

)