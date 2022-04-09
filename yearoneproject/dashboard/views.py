from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


#Imported models we create
from .models import Member
from .models import TechSkills



'''
    This is where all the views/pages are created
'''

# Create your views here.

#Index/Home page View
def index(request):
    #using the data from the DB
    members = Member.objects.all()
    skills = TechSkills.objects.all()
    return render(request, 'index.html', {'members' : members, 'skills': skills}) #renders the templates file


#Dashboard page View
def dashboard(request):
    return render(request, 'dashboard.html')


#User profile View-- This is where they will be able to edit
def user(request):
    #IS taking the form data from index.html and rendering it to user.html
    text = request.POST['text']
    return render(request, 'user.html', {'userText': text})#key:value


#User Registration View 
def register(request):
    #Ensure it is a POST method
    if request.method == 'POST':
        #Data collected from registration form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #Validate Password matching
        if password == password2:
            #Validate email not used
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Your email is already in use. Please use another one')
                return redirect('register') #redirected user
            #Validate username not used
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Your username is already in use. Please use another one')
                return redirect('register') #redirected user
            #create the new Member
            else:
                User.objects.create_user(username = username, email = email, password = password)
                #Save the member & redirect to the login
                return redirect('login')
        else:
            messages.info(request, 'Passwords are not matching')
            return redirect('register')
    else:
        return render(request, 'register.html')


#User Login View 
def view_login(request):
    #Ensure it is a POST method
    if request.method == 'POST':
        #Data collected from registration form
        username = request.POST['username']
        password = request.POST['password']

        #authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/dashboard')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:
        return render(request, 'login.html')


#User Logout 
def view_logout(request):
    logout(request)
    return redirect('/')

