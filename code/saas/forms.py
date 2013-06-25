'''
Created on 25-Jun-2013

@author: arun
'''
from django.contrib import auth
from saas.models import User
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        
    password = auth.forms.ReadOnlyPasswordHashField(label=_("Password"),
    help_text=_("Raw passwords are not stored, so there is no way to see "
                "this user's password, but you can change the password "
                "using <a href=\"password/\">this form</a>."))

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]    
    
class UserCreationForm(forms.ModelForm):
#     username = forms.CharField(required=False, widget=forms.HiddenInput)
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))


    class Meta:
        model = User
        fields = ('email', 'role')


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SaasAuthenticationForm(auth.forms.AuthenticationForm):
    

    def clean(self):
        cleaned_data = auth.forms.AuthenticationForm.clean(self)
        
        if not getattr(self.request, "tenant")  or not self.get_user() in self.request.tenant.users.all():
            raise forms.ValidationError(self.error_messages['invalid_login'] % {'username': self.username_field.verbose_name})
            
        return cleaned_data
