from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
#Imported models we create
from .models import Member
from .models import TechSkills
from .models import CustomUser

#imported forms
from .forms import MemberProfileForm, UpdateMemberForm, CreateMemberForm# MemberSkillsForm


'''
    This is where all the views/pages are created
    Create your views here.
'''



#Index/Home page View
def index(request):
    #using the data from the DB
    members = Member.objects.all()
    skills = TechSkills.objects.all()
    return render(request, 'index.html', {'members' : members, 'skills': skills}) #renders the templates file


#User Login View 
def view_login(request):
    #Ensure it is a POST method
    if request.method == 'POST':
        #Data collected from registration form
        email = request.POST['email']
        password = request.POST['password']

        #authenticate user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('/dashboard')
        else:
            messages.info(request, 'Email or password is Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')



#User Logout 
def view_logout(request):
    logout(request)
    return redirect('/')



#Dashboard page View
@login_required(login_url='/login/') 
def dashboard(request):
    members = Member.objects.all()
    skills = TechSkills.objects.all()
    return render(request, 'dashboard.html',{'members' : members, 'skills': skills})



#User profile update View
@login_required(login_url='/login/') 
def profile(request):

    if request.method == 'POST':
        user_form = UpdateMemberForm(request.POST, instance=request.user)
        profile_form = MemberProfileForm(request.POST, instance=request.user.member)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile was updated successfully')
            return redirect('profile')
        #else:
            # Redirect back to the same page if the data
            # was invalid
            #return render(request, "memberProfile.html", {'user_form': user_form,'profile_form': profile_form} ) 
    else:
        user_form = UpdateMemberForm(instance=request.user)
        profile_form = MemberProfileForm(instance=request.user.member)


    return render(request, 'memberProfile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )



#User Registration View 
def register(request):

    if request.method == 'POST':
        createuser_form = CreateMemberForm(request.POST)
        if createuser_form.is_valid():
            #empty object created
            user = createuser_form.save(commit=False)

            
            #Password is set/save here
            user.set_password(
                createuser_form.cleaned_data.get('password')
            )
            user.save()
            messages.success(request, 'Your profile was created successfully')
            return redirect('/login')
        else:
            #Redirect back if  data was invalid
            return render(request, "register.html", {'createuser_form': createuser_form} ) 
    else:
        createuser_form = CreateMemberForm()


    return render(request, 'register.html',{'createuser_form': createuser_form})