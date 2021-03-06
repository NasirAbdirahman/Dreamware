
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
    is_company = models.BooleanField(blank=False,default=False)#Monitors companies active on platform
    date_joined = models.DateTimeField(default=timezone.now)

    #email is the unique identifier
    USERNAME_FIELD = 'email' 

    # required--can't create superuser
    REQUIRED_FIELDS = ['first_name','last_name'] 

    #Specifies that all objects for the class come from CustomUserManager
    objects = CustomUserManager() 
    
    # Overriding save method to values are lowercase before saving into DB
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()

        return super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"


#Skills Model
class TechSkills(models.Model):
    name = models.CharField(max_length=65,unique=True)
    
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
        ('DO', 'Dev-Ops'),
        ('CS', 'Cyber-Sec.')
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
        ('NO', 'No Relocation')
    )

    #inherited information from Custom User
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(blank = False,max_length=50)
    last_name = models.CharField(blank = False,max_length=50)
    email = models.EmailField()
    picture = models.ImageField(default="defaultuser.png",upload_to="profile_images") #upload to images folder in database
    location = models.CharField(max_length=100)
    personal_goal = models.TextField(max_length=500)
    personal_story = models.TextField(max_length=500)
    education = models.CharField(max_length=100) 
    linkedin = models.URLField()
    github = models.URLField()
    portfolio = models.URLField()
    interests = MultiSelectField(choices=INTERESTS)
    previous_occupation = models.CharField(max_length=100)
    availability = models.CharField(max_length=2, choices=WORK_AVAILABILITY)
    workstatus = models.CharField(max_length=2, choices=WORK_STATUS)
    relocation = models.CharField(max_length=2, choices=RELOCATION_STATUS)

    #Tech Skills field
    skills = models.ManyToManyField(TechSkills)


    #return all fields or just return specifics
    def __str__(self):
        return f"{self.user}"

    #Returns a list version of interests(Allows looping in template in view)
    def interests_list(self):
        list = str(self.interests)
        list_ = list.split(',')
        return list_

    # Overriding save method to values are lowercase before saving into DB
    def save(self, *args, **kwargs):
        self.previous_occupation = self.previous_occupation.capitalize()
        return super(Member, self).save(*args, **kwargs)




#Companies Model
class Companies(models.Model):

    #inherited information from Custom User
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField() # WILL have validators ensuring non-frauds, depending on org.
    #USER FIELDS FOR REPRESENTATIVE
    first_name = models.CharField(blank=False,max_length=50)
    last_name = models.CharField(blank=False,max_length=50)
    
    
    #Preferably a company logo/insigniaR OR company point person
    picture = models.ImageField(default="defaultuser.png",upload_to="company_images") #upload to images folder in database
    company_name =  models.CharField(max_length=60, default='To Be Announced') #Default given due to info not asked at creation of company model
    company_title = models.CharField(max_length=100)
    linkedin = models.URLField(default="https://www.linkedin.com")

    #return all fields or just return specifics
    def __str__(self):
        return f"{self.company_name} - {self.user}"

    # Overriding save method so values are lowercase before saving into DB
    def save(self, *args, **kwargs):
        self.company_name = self.company_name.capitalize()
        return super(Companies, self).save(*args, **kwargs)

      
# Job Post Model
class JobPost(models.Model):
    #ADMIN APPROVAL CAPABILITIES
    admin_approved = models.BooleanField(default=False)

    #Custom User's company Model
    company = models.ForeignKey(Companies, related_name="companyjob", on_delete=models.CASCADE)

    #Job Description
    company_name = models.CharField(max_length=60)
    position_title = models.CharField(max_length=60)
    salary = models.IntegerField(null=True, blank=True)#MUST BE STARTING SALARY
    location = models.CharField(max_length=65)
    skill_one = models.CharField(max_length=100)
    skill_two = models.CharField(max_length=100)
    skill_three = models.CharField(max_length=100)
    job_link = models.URLField()
    date_posted = models.DateTimeField(default=timezone.now)
  
    #return all fields or just return specifics
    def __str__(self):
        return self.company_name