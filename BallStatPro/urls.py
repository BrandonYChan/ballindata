from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('analysis/', views.analysis, name = 'Analysis'), 
    path('stats/', views.stats, name = 'Stats'), 
    path('about/', views.about, name='About'), 
    path('Analyses/greatest_season/', views.greatest_season, name='greatest_season'),
]


