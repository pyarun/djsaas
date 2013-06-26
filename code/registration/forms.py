'''
Created on 26-Jun-2013

@author: arun
'''

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from saas.models import Tenant, User
from django.core.exceptions import ValidationError
from .models import RegistrationProfile
from django.conf import settings

def unique_domain_name_validator(value):
    if Tenant.objects.filter(domain_name=value).exists():
        raise ValidationError("{} is already used. Please choose different Domain Name".format(value))

def unique_email_validator(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError("User already registered with email {}. Please use different email".format(value))



class RegistrationForm(forms.Form):
    """
        To be Used for tenant Registrations
    """
    _manager_role = "tmanager"
    
    name = forms.CharField(label=_("Company Name"), max_length=25, required=True, help_text=_("Name of the Company"))
    email = forms.EmailField(label=_("Email"), required =True, validators=[unique_email_validator])
    domain_name = forms.CharField(_('Subdomain'), required=True, validators=[unique_domain_name_validator],
                        help_text=_("Subdomain name to be used for setting up customized access url."))
    address = forms.CharField(max_length=150, )
    phone = forms.CharField(max_length=15)
    
    
    def _generate_password(self):
        """
        Returns a randome string of six characters as password
        """
        import random, string
        return "".join( random.sample(string.letters+string.digits, 6))
    
    def register_tenant(self):
        """
        Create a Tenant Record and send a verification mail to Manager
        """
        if hasattr(self, "cleaned_data"):
            data = self.cleaned_data
            tenant = Tenant()
            for k,v in data.items():
                if hasattr(tenant, k): setattr(tenant, k, v)
            tenant.save()
            manager = User.objects.create_user(data["email"], self._manager_role, self._generate_password())
            tenant.users.add(manager)
            tenant.save()
            
            #create profile
            profile = RegistrationProfile.objects.create_profile(manager)
            
            self.send_activation_mail(profile)
            return profile
            
            
        else:
            raise  RuntimeError( "Its required to call form's is_valid method before a call to register_tenant")

    def send_activation_mail(self, profile):
        """
        Send a mail to tenant manager with a link to activate the account
        """
        if "dbmail" in settings.INSTALLED_APPS:
            from dbmail.mail import DbSendMail
            mailer = DbSendMail("TAAM")
            context = dict(name=profile.user.get_full_name(), 
                           activation_key=profile.activation_key)
            
            mailer.sendmail([profile.user.email], context)
            
        else:
            from django.core.exceptions import ImproperlyConfigured
            ImproperlyConfigured("to Use mail service, its required to install dbmail app. Download from {}".format("https://bitbucket.org/pyarun/dbmail", ))
#             profile.user.email_user(subject, message)
        
        