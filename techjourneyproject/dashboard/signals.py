from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver, Signal
from .models import JobPost, Member,CustomUser,Companies

#Signal file
#Allow certain senders to notify a set of receivers that some action has taken place
#helps decoupled applications get notified when actions occur elsewhere in the framework.

#Signal for automatic creation of member or company profiles for users
@receiver(post_save,sender=CustomUser) #sender=settings.AUTH_USER_MODEL)
def create_member(sender, instance, created, **kwargs):
    #if CustomUser model is created
    if created:
        #Ensures that Company Model is created for companies but not created for Admins
        if instance.has_perm('dashboard.is_admin') is not True & instance.is_company is True:#instance.has_perm('dashboard.is_company') is True:
            #Default data when new user is created,email is immediately passed to company model
            default_data = dict(email=instance.email,first_name=instance.first_name,last_name=instance.last_name)
            #Company Model created and saved
            Companies.objects.create(user=instance,**default_data)
            instance.save()
            
        #ensures member model not created for admin users
        elif instance.has_perm('dashboard.is_admin') is not True:
            #Default data when new user is created,email is immediately passed to member
            default_data = dict(email=instance.email,first_name=instance.first_name,last_name=instance.last_name)
            
            #member model created & saved for user
            Member.objects.create(user=instance, **default_data)
            instance.save()

# Signal for automatically updating Member/Company model when member/company 
# changes CustomUser data IN EDIT PROFILE
@receiver(pre_save,sender=CustomUser) #sender=settings.AUTH_USER_MODEL)
def update_member(sender, instance,  **kwargs):

    # if CustomUser is company
    if instance.has_perm('dashboard.is_admin') is not True & instance.is_company is True:
        #DELETING CURRENT VALUES
        instance.companies.first_name = str(instance.companies.first_name).replace(instance.companies.first_name,'')
        instance.companies.last_name = str(instance.companies.last_name).replace(instance.companies.last_name,'')
        #instance.companies.email = str(instance.companies.email).replace(instance.companies.email,'')
        
        #NEW VALUES CREATED BY CUSTOMUSER EDITING
        fname = instance.first_name
        lname = instance.last_name
        #email = instance.email

        # ADDING VALUES FROM CUSTOMUSER TO MEMBER MODEL
        instance.companies.first_name += fname
        instance.companies.last_name += lname
        #instance.companies.email += email

        instance.companies.save()

    # if CustomUser is member
    elif instance.has_perm('dashboard.is_admin') is not True:

        #DELETING CURRENT VALUES
        instance.member.first_name = str(instance.member.first_name).replace(instance.member.first_name,'')
        instance.member.last_name = str(instance.member.last_name).replace(instance.member.last_name,'')
        #instance.member.email = str(instance.member.email).replace(instance.member.email,'')

        #NEW VALUES CREATED BY CUSTOMUSER EDITING
        fname = instance.first_name
        lname = instance.last_name
        #email = instance.email

        # ADDING VALUES FROM CUSTOMUSER TO MEMBER MODEL
        instance.member.first_name += fname
        instance.member.last_name += lname
        #instance.member.email += email
        
        instance.member.save()


#Signal for notification to admin on creation of job posts
'''@receiver(post_save, sender=JobPost)
def admin_approval(sender, instance, created, **kwargs):
    if created:
        #Send email to admin to ask for verification on created job post
    '''
