from secrets import choice
from tkinter import Widget
from xml.dom import ValidationErr
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import Companies, CustomUser, Member, TechSkills, JobPost
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.forms.widgets import ClearableFileInput

'''Forms for Admin to create and update users from Admin Panel'''

#A form for creating new users,Includes all the fields
class CustomUserCreationForm(UserCreationForm):
    

    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name')


# A form for updating users. 
# Includes all the fields but replaces password field with admin's disabled password hash display field.
class CustomUserChangeForm(UserChangeForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name')




''' Forms for User to Login '''
#Form for Users/Members to Log in
class UserLoginForm(forms.ModelForm):

    #Fields created for Form
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'batman@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'password', 'placeholder':"Secret Password"}))
   
    class Meta:
        model = Member
        fields = ( 'email',)
        #fields = '__all__'




'''Forms for users to create, update Member/Company profiles'''


#Form for letting users register as Members or Companies
class CreateMemberForm(forms.ModelForm):

    #Fields created for Form
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Legal First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Legal Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'batman@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'password', 'placeholder':"Secret Password"}))    
    
    #For companies to create Accounts-MUST BE CHECKED
    MEMBER_STATUS = (
        (False, 'Member'),
        (True, 'Company'),
    )
    is_company = forms.ChoiceField(widget=forms.RadioSelect,choices=MEMBER_STATUS, initial=False)
   
    #validation to check PW
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password


    #validation to check reused email-(OVERRIDES DEFAULT IN MODEL)
    def clean_email(self):
        # extract the fields from the data
        email = self.cleaned_data['email']

        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', "Your email is already in use. Please use another one")
        return email


   

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email','is_company',)
        #fields = '__all__'



# A form for letting Users update their personal data 
class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(disabled=True)

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email',)
        #fields = '__all__'



# Member Model Form - A form for letting members update their profile data
class MemberProfileForm(forms.ModelForm):

    #upload to images folder in database
    picture = forms.ImageField()
    location = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    personal_story = forms.Textarea()
    personal_goal = forms.Textarea()
    education = forms.CharField()
    linkedin = forms.URLField()
    github = forms.URLField()
    portfolio = forms.URLField()
    interests = forms.CheckboxSelectMultiple()
    previous_occupation = forms.CharField()
    availability = forms.CheckboxSelectMultiple
    workstatus = forms.CheckboxSelectMultiple
    relocation =  forms.CheckboxSelectMultiple
    skills = forms.ModelMultipleChoiceField(required=False,queryset=TechSkills.objects.all(),widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Member
        fields = (
            'picture','location','personal_story','personal_goal','education','linkedin',
            'github','portfolio','previous_occupation','availability',
            'workstatus','interests','relocation' ,'skills'
        )
        #fields = '__all__'


# Company Model Form - A form for letting companies update their profile data
class CompanyProfileForm(forms.ModelForm):

    
    '''first_name = forms.CharField()
    last_name = forms.CharField()'''
    #upload to images folder in database
    picture = forms.ImageField()#Preferably a company logo/insignia
    company_name = forms.CharField()
    company_title = forms.CharField()
    linkedin = forms.URLField()
    
    class Meta:
        model = Companies
        fields = (#'first_name','last_name',
        'picture','company_name','company_title','linkedin')
        #fields = '__all__'


# Job Post Model Form - A form for letting companies create job postings
class JobPostForm(forms.ModelForm):

    company_name = forms.CharField()
    position_title = forms.CharField()
    location = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    salary = forms.IntegerField()
    skill_one = forms.CharField()
    skill_two = forms.CharField()
    skill_three = forms.CharField()
    job_link = forms.URLField()
    
    class Meta:
        model = JobPost
        fields = ('company_name','position_title','location','salary','skill_one','skill_two','skill_three','job_link')
        #fields = '__all__'
