from django.db import models

# Create your models here.
from django.contrib import auth
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import string, random
from django.utils import timezone
from django.core.mail import send_mail

ROLES = (
         ( "dev-admin", _("Developer Admin")),
         ( "superadmin", _("Super Admin")),
         ( "tmanager", _("Tenant Manager")),
         ( "tadmin", _("Tenant Admin")),
         ( "user", _("User"))
    )

# from django.db.models.signals import class_prepared
# @receiver(class_prepared)
# def set_default_username(sender, **kwargs):
#     """
#         This function is a reciever of class_prepared signal.
#         It is used to set the default value for username, in User Table.
#         Username is a unique and dynamically generated key. Whenever a new user instance is created,
#         a unique username is set by default.
#     """
#     def generate_new_username():
#         while True:
#             sample = "".join(random.sample(string.letters.lower() + string.digits, 6))
#             if not User.objects.filter(username = sample).exists():break
#         return sample
#     
#     if sender.__name__ == "User" and sender.__module__== __name__:
#         sender._meta.get_field("username").default = generate_new_username



class SaasUserManager(auth.models.BaseUserManager):
    
    def create_user(self, email, role, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = SaasUserManager.normalize_email(email)
        user = self.model(email=email, role=role,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        role = extra_fields.pop("role", 'user') if extra_fields.has_key("role") else "user"
        u = self.create_user( email, role, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

<<<<<<< HEAD

class User(auth.models.AbstractBaseUser, auth.models.PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
=======
class SaasUserManager(auth.models.UserManager):
    pass

class User(auth.models.AbstractUser):
>>>>>>> master
    avatar = models.ImageField(upload_to="avatar", blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLES)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = SaasUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'role']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    objects = SaasUserManager()
    
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    
    def is_tmanager(self):
        """
            returns True if the given users Role is tmanager
        """
        return self.role == "tmanager"
    
<<<<<<< HEAD
#Classes for Tenant's Account Manager    
 
class TenantAccountManagers_Manager(SaasUserManager):
     
    def get_query_set(self):
        queryset = SaasUserManager.get_query_set(self)
        return queryset.filter(role="tmanager") 
 
 
class TenantAccountManager(User):
    objects = TenantAccountManagers_Manager()
=======
    

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    
    
class TenantManager(User):
    """
        Subset of Users, Who are acting as Account Managers for Tenant's
    """
>>>>>>> master
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
  
