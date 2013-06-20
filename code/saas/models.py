from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


ROLES = (
         ( "dev-admin", "Developer Admin"),
         ( "superadmin", "Super Admin"),
         ( "tmanager", "Tenant Manager"),
         ( "tadmin", "Tenant Admin"),
         ( "user", "User")
    )



class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatar", blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLES)
    
    
    def is_tmanager(self):
        """
            returns True if the given users Role is tmanager
        """
        return self.role == "tmanager"
    
    

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    
    
class TenantManager(models.Manager):
    
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
        
        
class Tenant(models.Model):
    """
        Holds Basic Information about the Tenant for SaaS application.
        This model should hold very basic information that can be used with any type of SAAS application.
        For Detailed Product(application) specific information about the tenant, its recommended to add 
        a TenantProfile Model, Just like we have User and UserProfile Relation
    
        When a Tenant is created, a Tenant owner account should also be created
    """
    name = models.CharField(max_length=50, help_text="Company's Display Name")
    logo = models.ImageField(upload_to="logo", blank=True, null=True)
    domain_name = models.CharField(max_length=25, help_text="Domain Name to be set")
    
    active = models.BooleanField(default=False)
    
    users =  models.ManyToManyField(User, blank=True, null=True)
    
    objects = TenantManager()
  
    
# post_save.connect(Tenant.objects.create_tenant_manager, Tenant)

# class TenantUser(models.Model):
#     tenant = models.ForeignKey(Tenant)
#     user = models.ForeignKey(User)
    
    



