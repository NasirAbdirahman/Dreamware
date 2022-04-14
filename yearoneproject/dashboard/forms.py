from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUser, Member, TechSkills
from django import forms


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





'''Forms for users to update their profiles'''

# A form for letting members update their user data 
class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email',)
        #fields = '__all__'


# A form for letting members update their profile data
class MemberProfileForm(forms.ModelForm):
    picture = forms.ImageField() #upload to images folder in database
    location = forms.CharField(max_length=100)
    personal_story = forms.Textarea()
    education = forms.CharField(max_length=100)
    linkedin = forms.CharField(max_length=100)
    github = forms.CharField(max_length=100)
    portfolio = forms.CharField(max_length=100)
    interests = forms.CheckboxSelectMultiple()
    previous_occupation = forms.CharField(max_length=100)
    availability = forms.CheckboxSelectMultiple
    workstatus = forms.CheckboxSelectMultiple
    skills = forms.ModelMultipleChoiceField(queryset=TechSkills.objects.all(),widget=forms.CheckboxSelectMultiple)
  
    
    class Meta:
        model = Member
        fields = (
            'location','picture','personal_story','education','linkedin',
            'github','portfolio','previous_occupation','availability',
            'workstatus','interests','skills'
            )
        #fields = '__all__'
