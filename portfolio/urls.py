from django.urls import path
from .views import *

app_name = 'portfolio'

urlpatterns = [
    path('portfolio/', portfolio, name='portfolio'),
    path('portfolioInsert/', portfolio_Insert, name='portfolioInsert'),
    path('ChangeActivePortfolio/', change_active_portfolio, name='ChangeActivePortfolio'),
    path('DeletePortfolio/', delete_portfolio, name='DeletePortfolio'),
    path('portfolioEdit/', portfolio_edit, name='portfolioEdit'),
    path('portfolioEditSave/', portfolio_edit_save, name='portfolioEditSave'),
]