# Create your views here.

from django.views.generic import FormView, TemplateView
from .forms import RegistrationForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationView(FormView):
    template_name = "registration_form.html"
    
    def get_form_class(self):
        return RegistrationForm
    
    def form_valid(self, form):
        self._profile = form.register_tenant()
        return FormView.form_valid(self, form)
        
    def get_success_url(self):
        return reverse_lazy("registration_thankyou", args=(self._profile.user.pk))
        
        
        
class RegistrationThankyouTemplateView(TemplateView):
    template_name = "registration_thankyoupage.html"
    
    def get_context_data(self, **kwargs):
        kwargs =  TemplateView.get_context_data(self, **kwargs)
        userpk = kwargs["userpk"]
        kwargs["user_obj"] = User.objects.get(pk=userpk)
        
        return kwargs