from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
import hashlib, random

User = get_user_model()

class RegistrationProfileManager(models.Manager):
    def create_profile(self, user):
        """
        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(user.email+salt).hexdigest()
        profile = self.create(user=user, activation_key=activation_key)
        
        return profile


class RegistrationProfile(models.Model):
    """
    Profile to store activation key for use during account registrations
    """
    activation_key = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    
    objects = RegistrationProfileManager()