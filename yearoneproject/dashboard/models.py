from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
#from django.utils.translation import ugettext_lazy as _ #Allows me to mark as a translation string
from multiselectfield import MultiSelectField

#import the Custom Manager we created
from .managers import CustomUserManager

# Create your models here.
# Model is an object representing my table's data


#CustomUser class that subclasses AbstractBaseUser with Extra fields
class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = None # Disable a field from AbstractBaseUser

    email = models.EmailField(
        'Email address',
        unique = True,
        error_messages = {'unique': 'This email already exists.'}
    )

    #extra fields declared here
    first_name = models.CharField(blank = False,max_length=50)
    last_name = models.CharField(blank = False,max_length=50)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    #email is the unique identifier
    USERNAME_FIELD = 'email' 

    # required--can't create superuser
    REQUIRED_FIELDS = ['first_name','last_name'] 

    #Specifies that all objects for the class come from CUstomUserManager
    objects = CustomUserManager() 
    
    def __str__(self):
        return self.email 



#Member Model
class Member(models.Model):

    #Members Tech Interests
    INTERESTS = (
        ('FE', 'Front-End'),
        ('BE', 'Back-End'),
        ('FS', 'Full-Stack'),
        ('MD', 'Mobile Dev'),
        ('DO', 'Dev Ops'),
        ('SI', 'Security & Infrastructure')
    )

    #Members Current Work Status
    WORK_STATUS = (
        ('AL', 'Actively Looking'),
        ('AC', 'Just Curious'),
        ('HE', 'Happily Employed')
    )

    #Members Current Availability
    WORK_AVAILABILITY = (
        ('IA', 'Immediately Available'),
        ('AW', 'About 2 Weeks'),
        ('MT', 'Moving Target')
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    #password = models.CharField(max_length=20) #delete potentially
    #picture = models.ImageField(upload_to="images/") #upload to images folder in database
    location = models.CharField(max_length=100)
    #skills = models.ForeignKey('TechSkills', on_delete=models.CASCADE)
    linkedin = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    portfolio = models.CharField(max_length=100)
    interests = MultiSelectField(choices=INTERESTS)
    previousoccupation = models.CharField(max_length=100)
    availability = models.CharField(max_length=2, choices=WORK_AVAILABILITY)
    workstatus = models.CharField(max_length=2, choices=WORK_STATUS)

    #return all fields or just return specifics
    def __str__(self):
        return self.email


#Skills Model
class TechSkills(models.Model):
    #Members proficiency level based on grade
    PROFICIENCY_LEVELS = (
        ('BG', 'Beginnerr'),
        ('IM', 'Intermediate'),
        ('AD', 'Advanced')
    )
    name = models.CharField(max_length=65)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=100 , choices=PROFICIENCY_LEVELS)




#Companies Model
class Companies(models.Model):
    pass

