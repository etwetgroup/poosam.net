from django.urls import path
from .views import *

app_name = 'faq'

urlpatterns = [
    path('faq/', faq, name='faq'),
    path('faqInsert/', faq_insert, name='faqInsert'),
    path('faqDataSource/', faq_datasource, name='faq_datasource'),
    path('faqDelete/<int:id>', faq_delete, name='faqDelete'),
    path('changeFaqActive/<int:id>', change_faq_active, name='changeFaqActive'),
    path('faqEdit/<int:id>/', faq_edit, name='faqEdit'),
    path('faqEditSave/', faq_edit_save, name='faqEditSave'),

    path('survey/', survey, name='survey'),
    path('surveyDataSource/', survey_datasource, name='surveyDataSource'),
    path('surveyDelete/<int:id>', survey_delete, name='surveyDelete'),
    path('changeSurveyActive/<int:id>', change_survey_active, name='changeSurveyActive'),
    path('surveyEdit/<int:id>/', survey_edit, name='surveyEdit'),
    path('surveyEditSave/', survey_edit_save, name='surveyEditSave'),
]