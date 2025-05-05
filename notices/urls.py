from django.urls import path
from .views import *

app_name = 'notices'

urlpatterns = [
    # category
    path('newscategory/', news_category, name='newscategory'),
    path('noticeCategoryInsert/', notice_category_insert, name='noticeCategoryInsert'),
    path('noticeChangeActiveCategory/', notice_change_active_category, name='noticeChangeActiveCategory'),
    path('noticeDeleteCategory/', notice_delete_category, name='noticeDeleteCategory'),
    path('noticeCategoryEdit/', notice_category_edit, name='noticeCategoryEdit'),
    path('noticeCategoryEditSave/', notice_category_edit_save, name='noticeCategoryEditSave'),

    # news
    path('news/<int:id>/', news, name='news'),
    path('newsAdd/<int:id>/', notice_news_add, name='newsAdd'),
    path('noticeNewsInsert/', notice_news_insert, name='noticeNewsInsert'),
    path('noticeDeleteNews/', notice_delete_news, name='noticeDeleteCategory'),
    path('noticeChangeActiveNews/', notice_change_active_news, name='noticeChangeActiveNews'),
    path('newsEdit/<int:id>/<int:idd>/', notice_news_edit, name='newsEdit'),
    path('noticeNewsEditSave/', notice_news_edit_save, name='noticeNewsEditSave'),

    # ordering
    path('saveOrder/', save_order, name='saveOrder'),
]