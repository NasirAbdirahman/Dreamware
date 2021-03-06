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
from django.utils.safestring import mark_safe
#Imported models we create
from .models import Member
from .models import TechSkills
from .models import CustomUser
from .models import Companies
from .models import JobPost

#imported forms
from .forms import MemberProfileForm, UpdateUserForm, CreateMemberForm, UserLoginForm, CompanyProfileForm, JobPostForm# MemberSkillsForm


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


############################################################################
############################################################################

# MEMBER MODEL VIEWS


#Member Dashboard page View
@login_required(login_url='/login/')
def memberDashboard(request):
    #Return User's Member Model
    users = Member.objects.filter(user=request.user)
    #Returns Member's Tech Skills
    member_skills = request.user.member.skills.all()
    
    #loops thru all skills and makes it into a list of names
    #skills = list(request.user.member.skills.all())
    skills = [skill.name for skill in member_skills]


    # Fetch all Job postings that are APPROVED BY ADMIN,
    # filtering all the job posts whose skill fields contains anything in members_skill
    # returning top 7 matched jobs by date posted then alphabetically
    jobs = JobPost.objects.filter(admin_approved=True).filter(
        Q(skill_one__in = skills) | 
        Q(skill_two__in = skills) |
        Q(skill_three__in = skills)
    ).order_by('-date_posted','company_name')[:7]
    
    return render(request, 'memberDashboard.html',{'users': users, 'jobs':jobs})


#Member profile View
@login_required(login_url='/login/') 
def memberProfile(request):

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = MemberProfileForm(request.POST,request.FILES, instance=request.user.member )
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


#Member's JobBoard page View
@login_required(login_url='/login/') 
def memberJobBoard(request):
    if request.user.member or request.user.is_admin is True:

        # Fetch all Job postings that are APPROVED BY ADMIN,
        # Then order by date_posted descending, then alphabetically
        jobs = JobPost.objects.filter(admin_approved=True).order_by('-date_posted','company_name')
    
        return render(request, 'memberJobBoard.html', {'jobs':jobs}) #renders the templates file
    else:
        raise PermissionDenied()



############################################################################
############################################################################

# COMPANY MODEL VIEWS


#Company Dashboard page View
@login_required(login_url='/login/') 
def companyDashboard(request):
    #Custom permission check for non-company users
    if request.user.is_company is True:
        
        #Return User's Company Model
        users = Companies.objects.filter(user=request.user)

        # Returns all the job posts of company
        # ordered by those who have been APPROVED BY ADMIN = TRUE
        jobPosts = JobPost.objects.filter(company=request.user.companies).order_by('-admin_approved')

        #returns skills on each job post
        skillOne = [job.skill_one for job in jobPosts]  
        skillTwo = [job.skill_two for job in jobPosts]  
        skillThree = [job.skill_three for job in jobPosts]
        #Merge all jobpost skills into list
        topSkills = [*skillOne,*skillTwo,*skillThree]

        #filtering all the Members whose skills field contains any sought companies skill
        #removes duplicate values returned,returns only 7 candidates, then order by last name
        candidates = Member.objects.filter(skills__name__in = topSkills).distinct().order_by('last_name')[:7] 

        return render(request, 'companyDashboard.html',
            {'users': users,'jobPosts':jobPosts, 'candidates':candidates}
        )

    else:
        raise PermissionDenied()



#Company profile View
@login_required(login_url='/login/') 
def companyProfile(request):
    #Custom permission check for non-company users
    if request.user.is_company is True:
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = CompanyProfileForm(request.POST,request.FILES, instance=request.user.companies)
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



#Company Job Posting View
def companyJobPost(request):
    if request.user.is_company is True or request.user.is_superuser: #CAN ADD IF ADMIN NEEDS ACCESS
        if request.method == 'POST':
            post_form = JobPostForm(request.POST)
            if post_form.is_valid():
                #Create form instance
                job = post_form.save(commit=False)
                #assign company to job post
                job.company = request.user.companies
                #Save form
                job.save()

                messages.success(request,
                    mark_safe('We have received your job post! We will review it to ensure compliance with our guidelines. <br/>We will inform you within 24hrs, when it is published. Thank you!'
                    ))
                return redirect('jobPost')
            else:
                # Redirect back to the same page if the data
                # was invalid
                return render(request, "jobPost.html",{'post_form': post_form,}) 
        else:
            post_form = JobPostForm()

        return render(request, 'jobPost.html',{'post_form': post_form,})
    else:
        raise PermissionDenied()



#Company's CandidateBoard page View
@login_required(login_url='/login/') 
def companyCandidateBoard(request):
    #Custom permission check for non-company users
    if request.user.is_company is True:
        #Fetch all candidates, then order by last name
        candidates = Member.objects.order_by('last_name')
        return render(request, 'companyCandidateBoard.html', {'candidates':candidates}) #renders the templates file
    else:
        raise PermissionDenied()