from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.validators import validate_email
from django.db.models import Q
#Imported models we create
from .models import Member
from .models import TechSkills
from .models import CustomUser
from .models import Companies

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
            
            #User redirection logic
            if user is not None:

                #Company redirect
                if user.is_company is True:
                    login(request,user)
                    return redirect('companyDashboard')
                #Member redirect
                else:
                    login(request,user)
                    return redirect('memberDashboard')

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


#Member Dashboard page View
@login_required(login_url='/login/')
def memberDashboard(request):
    #Return User's Member Model
    users = Member.objects.filter(user=request.user)

    #Returns User's Member Skills
    skills = list(request.user.member.skills.all())
    #member_skills = list(skills)

    #filtering all the companies whose skill fields(Skill_one,skill_two,skill_three) contains members skill
    companies = Companies.objects.filter(#If Company MODEL skill_one contains ANYTHING user has
        Q(skill_one__in = skills) | 
        Q(skill_two__in = skills) |
        Q(skill_three__in = skills)
    )

    #If Company MODEL skill_one contains ANYTHING user has
    #companies = Companies.objects.filter(skill_one__in=member_skills)
    #companiesskills = Companies.objects.values_list('skill_one','skill_two', 'skill_three')#flat returns single values

    #interests = Member.objects.filter(interests = request.user.member.get_interests_display)
    
    #members = Member.objects.all()
    
    return render(request, 'memberDashboard.html',{'users': users, 'companies':companies}) #{'members' : members ,'skills': skills})



#Member profile View
@login_required(login_url='/login/') 
def memberProfile(request):

    if request.method == 'POST':
        user_form = UpdateMemberForm(request.POST, instance=request.user)
        profile_form = MemberProfileForm(request.POST,request.FILES, instance=request.user.member, )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile was updated successfully')
            return redirect('memberProfile')
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


#Company Dashboard page View
@login_required(login_url='/login/')
def companyDashboard(request):
    #Return User's Member Model
    users = Companies.objects.filter(user=request.user)

    #Returns User's Member Skills
    #skills = list(request.user.member.skills.all())
    #member_skills = list(skills)

    #filtering all the companies whose skill fields(Skill_one,skill_two,skill_three) contains members skill
    '''companies = Companies.objects.filter(#If Company MODEL skill_one contains ANYTHING user has
        Q(skill_one__in = skills) | 
        Q(skill_two__in = skills) |
        Q(skill_three__in = skills)
    )'''

    #If Company MODEL skill_one contains ANYTHING user has
    #companies = Companies.objects.filter(skill_one__in=member_skills)
    #companiesskills = Companies.objects.values_list('skill_one','skill_two', 'skill_three')#flat returns single values

    #interests = Member.objects.filter(interests = request.user.member.get_interests_display)
    
    #members = Member.objects.all()
    
    return render(request, 'companyDashboard.html',{'users': users,})# 'companies':companies}) #{'members' : members ,'skills': skills})




#Company profile View
@login_required(login_url='/login/') 
def companyProfile(request):

    if request.method == 'POST':
        user_form = UpdateMemberForm(request.POST, instance=request.user)
        profile_form = MemberProfileForm(request.POST,request.FILES, instance=request.user.member, )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile was updated successfully')
            return redirect('companyProfile')
        else:
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "companyProfile.html", 
                {
                'user_form': user_form,
                'profile_form': profile_form,
                }
            ) 
    else:
        user_form = UpdateMemberForm(instance=request.user)
        #profile_form = MemberProfileForm(instance=request.user.member)


    return render(request, 'companyProfile.html',
        {
            'user_form': user_form,
            #'profile_form': profile_form,
        }
    )

