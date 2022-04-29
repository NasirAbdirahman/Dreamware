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
from .forms import MemberProfileForm, UpdateMemberForm, CreateMemberForm, UserLoginForm# MemberSkillsForm


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
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            
            #Data from fields
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            
            #user authenticated
            user = authenticate(request,
                email=email, 
                password=password
            )
            
            if user is not None: 
                login(request,user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Email and/or password is Invalid')
                return redirect('login')
    else:
        login_form = UserLoginForm()
        
    return render(request, 'login.html',{'login_form': login_form})


#User Logout 
def view_logout(request):
    logout(request)
    return redirect('/')


#Dashboard page View
@login_required(login_url='/login/') 
def dashboard(request):
    users = Member.objects.filter(user=request.user)
    #interests = Member.objects.filter(interests = request.user.member.get_interests_display)
    #members = Member.objects.all()
    #skills = TechSkills.objects.all()
    return render(request, 'dashboard.html',{'users': users})#{'members' : members ,'skills': skills})



#User profile update View
@login_required(login_url='/login/') 
def profile(request):

    if request.method == 'POST':
        user_form = UpdateMemberForm(request.POST, instance=request.user)
        profile_form = MemberProfileForm(request.POST,request.FILES, instance=request.user.member, )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile was updated successfully')
            return redirect('profile')
        else:
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "memberProfile.html", 
                {
                'user_form': user_form,
                'profile_form': profile_form,
                }
            ) 
    else:
        user_form = UpdateMemberForm(instance=request.user)
        profile_form = MemberProfileForm(instance=request.user.member)


    return render(request, 'memberProfile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
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