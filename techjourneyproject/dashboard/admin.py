from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

#Imported models we created
from .models import Member
from .models import TechSkills
from .models import Companies
from .models import CustomUser
from .models import JobPost

#imported form to manage user creation through adminPanel
from .forms import CustomUserCreationForm, CustomUserChangeForm

#CustomUserAdmin Panel
class CustomUserAdmin(UserAdmin):

    #forms to create users through adminPanel
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    #Displayed fields of CustomUser Model on admin panel view
    list_display = (
        'email', 'first_name','last_name','is_admin', 'is_staff', 'is_active', 'is_company', 'date_joined'
    )

    #Displayed filters of CustomUser Model on admin panel view
    list_filter = (
        'is_admin', 'is_staff', 'is_active','is_company'
    )

    #Displayed field sets of CustomUser Model in admin panel(controls the layout of admin add/change page)--Editor privileges
    fieldsets = (
        (None, 
            {
            'fields': (('email', 'password'), ('first_name','last_name'))
            }
        ),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin','is_company')}),
    )
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',), #Extra CSS classes applied to fieldset.("pretty")
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','is_company')}
        ),
    )

    #Enables a search box on the admin panel (Query returns designated fields)
    search_fields = ('email',)

    #Specifies how lists of objects should be ordered in admin panel
    #changed in django 3.2-Backward compatible; I can use @admin.display in model too
    ordering = ('email',) 


##############################################################################################################
##############################################################################################################

#MemberModelAdmin Panel
class MemberModelAdmin(admin.ModelAdmin):
    #Displayed fields of Member Model on admin panel
    list_display = (
        'user','education','previous_occupation',
    )

    #Displayed filters of Member Model on admin panel
    list_filter = (
        'education', 'previous_occupation',
    )

    #Search field
    search_fields = ('education', 'previous_occupation',)


##############################################################################################################
##############################################################################################################

#CompanyModelAdmin Panel
class CompanyModelAdmin(admin.ModelAdmin):
    #Displayed fields of Member Model on admin panel
    list_display = (
        'user','company_name',
    )

    #Displayed filters of Member Model on admin panel
    list_filter = (
        'company_name',
    )

    #Search field
    search_fields = ('company_name',)


##############################################################################################################
##############################################################################################################

#JobPostAdmin Panel
class JobPostAdmin(admin.ModelAdmin):
    #Displayed fields of JobPost Model on admin panel
    list_display = (
        'company_name', 'position_title','admin_approved','date_posted'
    )

    #Displayed filters of JobPost Model on admin panel
    list_filter = (
        'company_name', 'position_title','admin_approved','date_posted'
    )

    #Search field
    search_fields = ('company_name', 'position_title')



# Registered models & Admin Panels
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Member,MemberModelAdmin)
admin.site.register(TechSkills)
admin.site.register(Companies, CompanyModelAdmin)
admin.site.register(JobPost, JobPostAdmin)

# unregister the Group model from admin.
admin.site.unregister(Group)