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


#Signal for notification to admin on creation of job posts
'''@receiver(post_save, sender=JobPost)
def admin_approval(sender, instance, created, **kwargs):
    if created:
        #Send email to admin to ask for verification on created job post
    '''
