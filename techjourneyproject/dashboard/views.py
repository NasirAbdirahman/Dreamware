from logging import raiseExceptions
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.validators import validate_email
from django.db.models import Q
from django.core.exceptions import PermissionDenied

#Imported models we create
from .models import Member
from .models import TechSkills
from .models import CustomUser
from .models import Companies

#imported forms
from .forms import MemberProfileForm, UpdateUserForm, CreateMemberForm, UserLoginForm, CompanyProfileForm# MemberSkillsForm


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


#Companies Index page View
def companies(request):
    return render(request, 'companies.html') #renders the templates file


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
        user_form = UpdateUserForm(request.POST, instance=request.user)
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
        user_form = UpdateUserForm(instance=request.user)
        profile_form = MemberProfileForm(instance=request.user.member)


    return render(request, 'memberProfile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )



#Company Dashboard page View
@login_required(login_url='/login/') 
#@permission_required('dashboard.CustomUser.is_company',raise_exception=True) #NOT WORKING(https://stackoverflow.com/questions/62689245/permission-required-decorator-not-working-on-view-in-django)
def companyDashboard(request):
    #Custom permission check for non-company users
    if request.user.is_company is True:# or request.user.is_superuser: #CAN ADD IF ADMIN NEEDS ACCESS
        #Return User's Company Model
        users = Companies.objects.filter(user=request.user)

        #return User's Company Model Skills
        skillOne = request.user.companies.skill_one
        skillTwo = request.user.companies.skill_two
        skillThree = request.user.companies.skill_three
        #return User's Company TechSkills as list
        topSkills ={skillOne,skillTwo,skillThree}

        '''#return User's Company JD
        companyName = request.user.companies.company_name
        position=request.user.companies.position_title
        salary=request.user.companies.salary
        location=request.user.companies.location
        #return User's Company TechSkills as list
        JD =(companyName,position,salary,location)'''

        #filtering all the Members whose skills field contains companies skill
            #If Member MODEL skills contains ANYTHING Company needs
        candidates = Member.objects.filter(skills__name__in = topSkills).distinct() #removes duplicate values returned
    
        return render(request, 'companyDashboard.html',
            {'users': users, 'topSkills':topSkills, 'candidates':candidates}
        )# 'companies':companies}) #{'members' : members ,'skills': skills})

    else:
        raise PermissionDenied()



#Company profile View
@login_required(login_url='/login/') 
#@permission_required('dashboard.is_company',raise_exception=True) #NOT WORKING(https://stackoverflow.com/questions/62689245/permission-required-decorator-not-working-on-view-in-django)
def companyProfile(request):
    #Custom permission check for non-company users
    if request.user.is_company is True:# or request.user.is_superuser: #CAN ADD IF ADMIN NEEDS ACCESS
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = CompanyProfileForm(request.POST,request.FILES, instance=request.user.companies, )
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
            user_form = UpdateUserForm(instance=request.user)
            profile_form = CompanyProfileForm(instance=request.user.companies)


        return render(request, 'companyProfile.html',
            {
                'user_form': user_form,
                'profile_form': profile_form,
            }
        )

    else:
        raise PermissionDenied()


#Member's JobBoard page View
@login_required(login_url='/login/') 
def memberJobBoard(request):
    return render(request, 'memberJobBoard.html') #renders the templates file


#Company's CandidateBoard page View
@login_required(login_url='/login/') 
def companyCandidateBoard(request):
    return render(request, 'companyCandidateBoard.html') #renders the templates file
