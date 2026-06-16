from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',            views.dashboard,  name='dashboard'),
    path('normaliser/', views.normaliser, name='normaliser'),
    path('wiki/',       views.wiki,       name='wiki'),
]
