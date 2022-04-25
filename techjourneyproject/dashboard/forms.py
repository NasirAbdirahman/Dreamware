from xml.dom import ValidationErr
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUser, Member, TechSkills
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


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





'''Forms for users to create, update profiles'''


#Form for letting members register as Users
class CreateMemberForm(forms.ModelForm):

    #Fields created for Form
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Legal First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Legal Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'batman@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'password', 'placeholder':"Secret Password"}))    
    
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
    

    '''#validation fn to check for duplicate PWS
        #REMOVED- due to django hdiding PWS, must validate in model or at CustomUser
    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password2 != password2:
            self.add_error('password2', "Your Passwords are not matching")
    
        return password'''

   

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email')
        #fields = '__all__'



# A form for letting members update their user data 
class UpdateMemberForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email',)
        #fields = '__all__'



# Member Model Form - A form for letting members update their profile data
class MemberProfileForm(forms.ModelForm):
    picture = forms.ImageField() #upload to images folder in database
    location = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    personal_story = forms.Textarea()
    education = forms.CharField(max_length=50)
    linkedin = forms.CharField(max_length=50)
    github = forms.CharField(max_length=50)
    portfolio = forms.CharField(max_length=50)
    interests = forms.CheckboxSelectMultiple()
    previous_occupation = forms.CharField(max_length=50)
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
