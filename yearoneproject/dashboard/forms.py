from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUser

'''Forms for Admin to create and update users'''

#A form for creating new users,Includes all the fields
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name')
        #fields = ('email','first_name','last_name','location','linkedin','github','portfolio','interests','previousoccupation','availability','workstatus')




# A form for updating users. 
# Includes all the fields but replaces password field with admin's disabled password hash display field.
 
class CustomUserChangeForm(UserChangeForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name')



'''Forms for users to create and update their profiles'''