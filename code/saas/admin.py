'''
Created on 19-Jun-2013

@author: arun
'''
from django.contrib import admin, auth
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from django.db import models
from saas.models import User, Tenant, TenantAccountManager
from django.contrib.admin.options import TabularInline
from saas import forms as saas_forms
 
class SaasUserAdmin(auth.admin.UserAdmin):
    readonly_fields = ('last_login',)
    
    form = saas_forms.UserChangeForm
    add_form = saas_forms.UserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (('first_name', 'last_name'), 'avatar')}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2')}
        ),
    )
#     form = UserChangeForm
#     add_form = UserCreationForm
#     change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name','role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email', 'role')
    filter_horizontal = ('groups', 'user_permissions',)



#     fieldsets = auth.admin.UserAdmin.fieldsets + (("abc", {'fields': ('role', 'avatar')}),)
#     add_fieldsets = ((None, {'fields':('email', 'role', 'password1', 'password2')}),)

 
admin.site.register( User, SaasUserAdmin)

# class TenantManagerAdmin(SaasUserAdmin):
# #       
# #     fields = (  ( "first_name", "last_name"),
# #                 ( "email", "password"),
# #                 ( "username","groups",),
# #                 ( "avatar", "role",),
# #             )
# #     readonly_fields = ('last_login','date_joined', 'username')
#       
# #     formfield_overrides = {
# #         models.CharField: {'widget': forms.Select(attrs={"disabled":"disabled"})},
# #     }
#       
#     form = saas_forms.UserChangeForm
#     add_form = saas_forms.UserCreationForm
#       
#     def get_form(self, request, obj=None, **kwargs):
#         """
#             Override the base function to set the Role as Tenant Manager
#         """
#         form = SaasUserAdmin.get_form(self, request, obj=obj, **kwargs)
#         try:
#             form.base_fields["role"].initial = "tmanager"
#         except:
#             pass # this is an add form
#         return form
#       
# #     def queryset(self, request):
# #         """
# #             Returns Users Who are account managers
# #         """
# #         qs = super(TenantManagerAdmin, self).queryset(request)
# #         return qs.filter(role="tmanager")
#   
#   
# admin.site.register(TenantAccountManager, TenantManagerAdmin)
# 
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