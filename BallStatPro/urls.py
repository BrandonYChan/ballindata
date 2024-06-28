from django.urls import path 
from . import views 
from .views import load_table 

urlpatterns = [
    path('', views.home, name='Home'),
    path('analysis/', views.analysis, name = 'Analysis'), 
    path('stats/', views.stats, name = 'Stats'), 
    path('about/', views.about, name='About'), 
    path('about-content/', views.about_content, name='About-content'),
    path('load_page/<str:page_name>/', load_table, name='load_table'),
]


