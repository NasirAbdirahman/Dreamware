from django.contrib import admin

#Imported models we created
from .models import Member
from .models import TechSkills
from .models import Companies #potential. Not added


# Registered models 
admin.site.register(Member)
admin.site.register(TechSkills)
