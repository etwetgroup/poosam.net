from django.urls import path
from .views import *

app_name = 'membership'

urlpatterns = [
    path('userMgmt/', userMgmt, name='userMgmt'),
    path('userDataSource/', user_datasource, name='userDataSource'),
    path('changeUserActive/<int:id>', change_user_active, name='changeUserActive'),
    path('userDelete/<int:id>', user_delete, name='userDelete'),
    path('userAdd/', user_add, name='userAdd'),
    path('userInsert/', user_insert, name='userInsert'),
    path('userEdit/<int:id>/', user_edit, name='userEdit'),
    path('userEditSave/', user_edit_save, name='userEditSave'),
]