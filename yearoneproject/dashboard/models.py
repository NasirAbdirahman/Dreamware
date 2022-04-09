from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.
# Model is an object representing my table's data


'''DON'T FORGET VALIDATORS FOR MIN LENGTH'''

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

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
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


#Skills Model
class TechSkills(models.Model):
    #Members proficiency level based on grade
    PROFICIENCY_LEVELS = (
        ('BG', 'Beginner'),
        ('IM', 'Intermediate'),
        ('AD', 'Advanced')
    )
    name = models.CharField(max_length=65)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=100 , choices=PROFICIENCY_LEVELS)




#Companies Model
class Companies(models.Model):
    pass



