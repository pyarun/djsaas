'''
Created on 24-Jun-2013

@author: arun
'''
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib import auth
from models import User


class UserChangeForm(auth.forms.UserChangeForm):
    
    class Meta:
        model = User
        
class UserCreationForm(auth.forms.UserCreationForm):
    
    class Meta:
        model= User



class SaasAuthenticationForm(AuthenticationForm):
    
#     tenant = forms.CharField(max_length= 25, required=True, widget=forms.HiddenInput)
    
    
#     def __init__(self, request=None, *args, **kwargs):
#         AuthenticationForm.__init__(self, request=request, *args, **kwargs)
#         
#         data = kwargs.get("data", None)
#         if data:
#             data["tenant"] = request.tenant.domain_name
#             kwargs["data"] = data
#         print kwargs


    def clean(self):
        cleaned_data = AuthenticationForm.clean(self)
        if not self.get_user() in self.request.tenant.users:
            raise forms.ValidationError(self.error_messages['invalid_login'] % {'username': self.username_field.verbose_name})
            
        return cleaned_data
