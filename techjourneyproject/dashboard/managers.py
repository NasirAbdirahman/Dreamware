from multiprocessing.sharedctypes import Value
from django.contrib.auth.base_user import BaseUserManager
#from django.utils.translation import ugettext_lazy as _ #Allows me to mark as a translation string

"""
    Custom user model manager:
        Email is the unique identifiers for authentication (NO usernames)
        Extra fields added
"""

class CustomUserManager(BaseUserManager):
   
    
    #Create and save a User with the given email and password.
    def create_user(self, email,first_name,last_name,password, **extra_fields):
    
        #if not email:
        #   raise ValueError("Email must be set")
        email = self.normalize_email(email)
        #Extra fields added to model
        user = self.model(email=email,first_name=first_name,last_name=last_name, **extra_fields)
        user.set_password(password)

        #user saved
        user.save(using=self._db)

        return user


  
    #Create and save a SuperUser with the given email,name and password.
    def create_superuser(self, email, first_name,last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(email=email,first_name=first_name,last_name=last_name,password=password,**extra_fields)
        user.set_password(password)
        user.is_admin = True
        
        #super_user saved
        user.save(using=self._db)

        return user