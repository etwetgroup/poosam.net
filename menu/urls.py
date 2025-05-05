from django.urls import path
from .views import *

app_name = 'menu'

urlpatterns = [
    path('mainMenu/', main_menu, name='mainMenu'),
    path('menuAdd/', menu_add, name='menuAdd'),
    path('subMenuAdd/<int:id>/', sub_menu_add, name='subMenuAdd'),
    path('mainMenuInsert/', main_menu_insert, name='mainMenuInsert'),
    path('mainSubMenuInsert/', main_submenu_insert, name='mainSubMenuInsert'),
    path('mainMenuParentDataSource/', main_menu_parent_datasource, name='mainMenuParentDataSource'),
    path('mainSubMenuDatasource/', main_submenu_datasource, name='mainSubMenuDatasource'),
    path('mainMenuDelete/<int:id>', main_menu_delete, name='mainMenuDelete'),
    path('menuEdit/<int:id>/', main_menu_edit, name='menuEdit'),
    path('subMenuEdit/<int:id>/', sub_menu_edit, name='subMenuEdit'),
    path('mainMenuEditSave/', main_menu_edit_save, name='mainMenuEditSave'),
    path('changeMainMenuActive/<int:id>', change_main_menu_active, name='changeMainMenuActive'),
    
    # URL Category paths
    path('urlCategories/', url_category_main, name='urlCategories'),
    path('urlCategoryAdd/', url_category_add, name='urlCategoryAdd'),
    path('urlCategoryInsert/', url_category_insert, name='urlCategoryInsert'),
    path('urlCategoryEdit/<int:id>/', url_category_edit, name='urlCategoryEdit'),
    path('urlCategoryEditSave/', url_category_edit_save, name='urlCategoryEditSave'),
    path('urlCategoryDelete/<int:id>', url_category_delete, name='urlCategoryDelete'),
    path('urlCategoryDatasource/', url_category_datasource, name='urlCategoryDatasource'),
    path('changeUrlCategoryActive/<int:id>', change_url_category_active, name='changeUrlCategoryActive'),
]