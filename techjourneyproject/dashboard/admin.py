from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

#Imported models we created
from .models import Member
from .models import TechSkills
from .models import Companies #potential. Not added
from .models import CustomUser
#imported form to manage user creation through adminPanel
from .forms import CustomUserCreationForm, CustomUserChangeForm

#CustomUserAdmin 
class CustomUserAdmin(UserAdmin):

    #forms to create users through adminPanel
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    #Displayed fields of CustomUser Model on admin panel view
    list_display = (
        'email', 'first_name','last_name','is_admin', 'is_staff', 'is_active', 'date_joined', #'location','linkedin','github','portfolio','interests','previousoccupation','availability','workstatus'
    )

    #Displayed filters of CustomUser Model on admin panel view
    list_filter = (
        'email', 'first_name','last_name','is_admin', 'is_staff', 'is_active'#, 'date_joined', 'location','linkedin','github','portfolio','interests','previousoccupation','availability','workstatus'
    )

    #Displayed field sets of CustomUser Model in admin panel(controls the layout of admin add/change page)--Editor privileges
    fieldsets = (
        (None, 
            {
            'fields': (('email', 'password'), ('first_name','last_name'))#'location','linkedin','github','portfolio','interests','previousoccupation','availability','workstatus')
            }
        ),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin')}),#Shows permissions in admin panel
    )
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',), #Extra CSS classes applied to fieldset.("pretty")
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    #Enables a search box on the admin panel (Query returns designated fields)
    search_fields = ('email',)

    #Specifies how lists of objects should be ordered in admin panel
    #changed in django 3.2-Backward compatible; I can use @admin.display in model too
    ordering = ('email',) 


# Registered models 
admin.site.register(Member)
admin.site.register(TechSkills)
admin.site.register(CustomUser, CustomUserAdmin)

# unregister the Group model from admin.
admin.site.unregister(Group)