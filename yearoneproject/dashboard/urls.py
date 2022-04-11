from django.urls import path
from . import views

''' urls for the app
    render the views for the individual app    
'''

#create urls for app
urlpatterns = [
    #root url
    path('', views.index, name='index'), #describes ('url', function/page/html etc. rendered, name)

    #more urls/views can be created below

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.view_login, name='login'),
    path('logout/', views.view_logout, name='logout'),
]