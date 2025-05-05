from django.urls import path
from .views import *

app_name = 'carousels'

urlpatterns = [
    path('carousels/', carousels, name='carousels'),
    path('carouselsInsert/', carousels_insert, name='carouselsInsert'),
    path('DeleteSlider/', delete_slider, name='DeleteSlider'),
    path('ChangeActiveSlider/', change_active_slider, name='ChangeActiveSlider'),
    path('carouselsEdit/', carousels_edit, name='carouselsEdit'),
    path('carouselsEditSave/', carousels_edit_save, name='carouselsEditSave'),
    path('saveOrder/', save_order, name='saveOrder'),
]