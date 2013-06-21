'''
Created on 19-Jun-2013

@author: arun
'''
from django.contrib import admin
from django import forms
from django.db import models
from models import User, Tenant, TenantManager
from django.contrib.admin.options import TabularInline


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('last_login', 'username')
    pass


admin.site.register( User, UserAdmin)


class TenantManagerAdmin(UserAdmin):
    
    fields = (  ( "first_name", "last_name"),
                ( "email", "password"),
                ( "username","groups",),
                ( "avatar", "role",),
            )
    readonly_fields = ('last_login','date_joined', 'username')
    
#     formfield_overrides = {
#         models.CharField: {'widget': forms.Select(attrs={"disabled":"disabled"})},
#     }
    
    
    def get_form(self, request, obj=None, **kwargs):
        """
            Override the base function to set the Role as Tenant Manager
        """
        form = UserAdmin.get_form(self, request, obj=obj, **kwargs)
        form.base_fields["role"].initial = "tmanager"
        return form
    
    def queryset(self, request):
        """
            Returns Users Who are account managers
        """
        qs = super(TenantManagerAdmin, self).queryset(request)
        return qs.filter(role="tmanager")


admin.site.register(TenantManager, TenantManagerAdmin)

class TenantManagerInlineForm(forms.ModelForm):
    fields = ("username", "email", "password")
    
    
class UserTabularInline(admin.TabularInline):
    model = Tenant.users.through
    extra = 1
    max_num = 1
    
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "users":
            kwargs["queryset"] = User.objects.filter(role="tmanager")
        
        return admin.TabularInline.formfield_for_manytomany(self, db_field, request=request, **kwargs)
        
    
class TenantAdmin(admin.ModelAdmin):
    pass
#     inlines = [
#                UserTabularInline,
#             ]
    


admin.site.register( Tenant, TenantAdmin)