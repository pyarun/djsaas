from django.db import models

# Create your models here.
from django.contrib import auth
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import string, random

ROLES = (
         ( "dev-admin", _("Developer Admin")),
         ( "superadmin", _("Super Admin")),
         ( "tmanager", _("Tenant Manager")),
         ( "tadmin", _("Tenant Admin")),
         ( "user", _("User"))
    )

from django.db.models.signals import class_prepared
@receiver(class_prepared)
def set_default_username(sender, **kwargs):
    """
        This function is a reciever of class_prepared signal.
        It is used to set the default value for username, in User Table.
        Username is a unique and dynamically generated key. Whenever a new user instance is created,
        a unique username is set by default.
    """
    def generate_new_username():
        while True:
            sample = "".join(random.sample(string.letters.lower() + string.digits, 6))
            if not User.objects.filter(username = sample).exists():break
        return sample
    
    if sender.__name__ == "User" and sender.__module__== __name__:
        sender._meta.get_field("username").default = generate_new_username



class SaasUserManager(auth.models.UserManager):
    pass

class User(auth.models.AbstractUser):
    avatar = models.ImageField(upload_to="avatar", blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLES)

    objects = SaasUserManager()
    
    def is_tmanager(self):
        """
            returns True if the given users Role is tmanager
        """
        return self.role == "tmanager"
    
#Classes for Tenant's Account Manager    

class TenantAccountManagers_Manager(SaasUserManager):
    
    def get_query_set(self):
        queryset = SaasUserManager.get_query_set(self)
        return queryset.filter(role="tmanager") 


class TenantAccountManager(User):
    objects = TenantAccountManagers_Manager()
    class Meta:
        proxy=True    

#Classes for Tenant Records

class TenantModelManager(models.Manager):
    
    def create_tenant_manager(self, sender, **kwargs):
        """
            creates a tenant manager user and adds to the tenant
        """
        is_created = kwargs.get("created") 
        instance = kwargs.get("instance")
        if is_created:
            data_set = dict(username="{}-admin".format(instance.name),
                            email="admin@some.com",
                            password="12345")
            
            tadmin = User.objects.create_user(**data_set)
            instance.users.add(tadmin)
        
        
    def create_tenant(self):
        """
            Create/Add a Tenant Manager
            Associate a Manager to Tenant
            Create a Group
            Set Permissions to the Group
        """
     
def generate_unique_slug():
    while True:
        slug = "".join(random.sample(string.letters, 6))
        if not Tenant.objects.filter(slug=slug).exists():
            break
    return slug   
    
        

def logo_storage(obj, filename):
    """
        generates unique path for logo storage
    """
    return "{}/logo/{}".format(obj.slug, filename)

class Tenant(models.Model):
    """
        Holds Basic Information about the Tenant for SaaS application.
        This model should hold very basic information that can be used with any type of SAAS application.
        For Detailed Product(application) specific information about the tenant, its recommended to add 
        a TenantProfile Model, Just like we have User and UserProfile Relation
    
        When a Tenant is created, a Tenant owner account should also be created
    """

    name = models.CharField(max_length=50, help_text="Company's Display Name", db_index=True)
    logo = models.ImageField( upload_to=logo_storage, blank=True, null=True)
    domain_name = models.CharField(max_length=25,unique=True, help_text="Domain Name to be set", db_index=True)
    
    active = models.BooleanField(default=False)
    
    users =  models.ManyToManyField(User, blank=True, null=True)
    
    slug = models.SlugField(max_length=6, default=generate_unique_slug, db_index=True, unique=True )
    
    objects = TenantModelManager()
    
    def __unicode__(self):
        return "{}-{}".format(self.name, self.slug) 
  
