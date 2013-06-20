'''
Created on 19-Jun-2013

@author: arun
'''
from django.contrib import admin
from django import forms
from models import User, Tenant
from django.contrib.admin.options import TabularInline


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register( User, UserAdmin)


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
    inlines = [
               UserTabularInline,
            ]
#     exclude = ["users"]
    pass


admin.site.register( Tenant, TenantAdmin)