from django.urls import path
from .views import *

app_name = 'website'

urlpatterns = [
    path('website/', website, name='website'),
    path('pages/', pages, name='pages'),
    path('changeWebSite/', change_website, name='changeWebSite'),
    path('uploadFile/', uploadFile, name='uploadFile'),
    path('saveLink/', saveLink, name='saveLink'),
]