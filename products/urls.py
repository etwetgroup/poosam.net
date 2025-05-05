from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    # Details Title
    path('detailsTitle/', detailsTitle, name='detailsTitle'),
    path('detailsAdd/', detailsAdd, name='detailsAdd'),
    path('detailsTitleInsert/', details_title_insert, name='detailsTitleInsert'),
    path('detailsTitleDatasource/', details_title_datasource, name='detailsTitleDatasource'),
    path('detailsTitleDelete/<int:id>', details_title_delete, name='detailsTitleDelete'),
    path('changeDetailsTitleActive/<int:id>', change_details_title_active, name='changeDetailsTitleActive'),
    path('detailsTitleEdit/', details_title_edit, name='detailsTitleEdit'),
    path('detailsTitleEditSave/', details_title_edit_save, name='detailsTitleEditSave'),

    # Products
    path('productsList/', products_list, name='productsList'),
    path('productsAdd/', products_add, name='productsAdd'),
    path('detailsTitleList/', details_title_list, name='detailsTitleList'),
    path('getProducts/', get_products, name='getProducts'),
    path('productsInsert/', products_insert, name='productsInsert'),
    path('productsDatasource/', products_datasource, name='productsDatasource'),
    path('productsDelete/<int:id>', products_delete, name='productsDelete'),
    path('changeProductsActive/<int:id>', change_products_active, name='changeProductsActive'),
    path('productsEdit/<int:id>/', products_edit, name='productsEdit'),
    path('productsEditList/', products_edit_list, name='productsEditList'),
    path('productsEditSave/', products_edit_save, name='productsEditSave'),
]