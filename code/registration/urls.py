'''
Created on 24-Jun-2013

@author: arun
'''
from django.conf.urls import patterns, include, url
from .views import RegistrationView, RegistrationThankyouTemplateView

urlpatterns = patterns("",
    
        url('^register$', RegistrationView.as_view(), name="tenant_registration_form"),
        url('^register/thanks/(?P<userpk>\d*)$', RegistrationThankyouTemplateView.as_view(), name="registration_thankyou"),

)