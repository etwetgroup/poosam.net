from django.urls import path
from .views import *

app_name = 'userauth'

urlpatterns = [
    path('', login_view, name='login'),
    path('auth/', auth_view, name='auth'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('profileChange/', profile_change, name='profileChange'),
    path('ProfileChangeSave/', profile_change_save, name='ProfileChangeSave'),
    path('PasswordChange/', password_change, name='PasswordChange'),
    path('PasswordChangeSave/', password_change_save, name='PasswordChangeSave'),
]