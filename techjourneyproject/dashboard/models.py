
from django.core.exceptions import ValidationError
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

    #Email Validator
    def validate_email(value):
        #list of emails to accept
        valid_emails = [
            '@gmail.com',
            '@outlook.com',
            '@yahoo.com',
            '@protonmail.com',
            '@aol.com',
            '@icloud.com',
        ]

        for x in valid_emails:
            if x in value:
                return value
            else:
                raise ValidationError("Email Field only accepts gmail, outlook, yahoo, aol and icloud addressees.")

    #Disable a field from AbstractBaseUser
    username = None
    email = models.EmailField(blank = False, unique = True, validators=[validate_email])

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

    #Specifies that all objects for the class come from CustomUserManager
    objects = CustomUserManager() 
    
    
    def __str__(self):
        return self.email 


#Skills Model
class TechSkills(models.Model):
    #Members Current Work Status
    '''SKILL_LEVEL = (
        ('EX', 'Exposed'),
        ('FM', 'Familiar'),
        ('PR', 'Proficient')
    )
    SKILLS = (
        ('RE', 'React.JS')
        etc...
    )
    
    '''

    name = models.CharField(max_length=65,unique=True)
    #TO WORK TRY 
    # name = models.MultiSelectField(choices=SKILLS)
    #skill_level = models.CharField(max_length=2, choices=SKILL_LEVEL)
    
    #return all fields or just return specifics
    def __str__(self):
        return self.name



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

    #Members willingness to relocate
    RELOCATION_STATUS = (
        ('OK', 'Open To Relocate'),
        ('NO', 'No')
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    #resume = models.ImageField(upload_to="images/") #upload to images folder in database
    picture = models.ImageField(default="defaultuser.png",upload_to="profile_images") #upload to images folder in database
    location = models.CharField(max_length=100)
    personal_goal = models.TextField(max_length=500)
    personal_story = models.TextField(max_length=500)
    education = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    portfolio = models.CharField(max_length=100)
    interests = MultiSelectField(choices=INTERESTS)
    previous_occupation = models.CharField(max_length=100)
    availability = models.CharField(max_length=2, choices=WORK_AVAILABILITY)
    workstatus = models.CharField(max_length=2, choices=WORK_STATUS)
    relocation = models.CharField(max_length=2, choices=RELOCATION_STATUS)

    #Tech Skills field
    skills = models.ManyToManyField(TechSkills,related_name="CustomUsers")


    #return all fields or just return specifics
    def __str__(self):
        return self.email

    #Returns a list version of interests(Allows looping in template in HTML)
    def interests_list(self):
        list = str(self.interests)
        list_ = list.split(',')
        return list_



#Companies Model
class Companies(models.Model):
    #Company representative email-- Would have validators ensuring non-frauds, depending on org.
    email = models.EmailField()

    #ADD FIRSTNAME & LASTNAME USER FIELDS FOR REPRESENTATIVE
    company_name =  models.CharField(max_length=60)
    position_title = models.CharField(max_length=60)
    #MUST BE STARTING SALARY
    salary = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=65)
    skill_one = models.CharField(max_length=100)
    skill_two = models.CharField(max_length=100)
    skill_three = models.CharField(max_length=100)
  
    #return all fields or just return specifics
    def __str__(self):
        return self.company_name