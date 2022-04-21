from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver, Signal
from .models import Member
from .models import CustomUser

#Signal file
#Allow certain senders to notify a set of receivers that some action has taken place
#helps decoupled applications get notified when actions occur elsewhere in the framework.

@receiver(post_save,sender=CustomUser) #sender=settings.AUTH_USER_MODEL)
def create_member(sender, instance, created, **kwargs):

    if created:
        #ensures member model not created for admin users
        if instance.has_perm('dashboard.view_Member') is not True:
            #Default data when new user is created,email is immediately passed to member
            default_data = dict(email=instance.email)
            
            #member model created & saved for user
            Member.objects.create(user=instance, **default_data)
            instance.save()
