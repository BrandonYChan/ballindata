from django.urls import path, include 
from . import views 
from .views import load_table 
from .views import load_analysis 
from .views import load_tool 
# from .views import season_select 
# from . import chart 


from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('', views.home, name='Home'),
    path('analysis/', views.analysis, name = 'Analysis'), 
    path('stats/', views.stats, name = 'Stats'), 
    path('tools/', views.tools, name = 'Tools'), 
    path('about/', views.about, name='About'), 
    path('about-content/', views.about_content, name='About-content'),
    path('stat_manual/', views.stat_manual, name='StatManual'), 
    path('stat_manual_content/', views.stat_manual_content, name='StatManual-content'),
    path('load_table/<str:page_name>/', load_table, name='load_table'),
    path('load_analysis/<str:page_name>/', load_analysis, name='load_analysis'), 
    path('load_tool/<str:page_name>/', load_tool, name='load_tool'),  
    path('chart/', views.chart, name='chart'), 
    path('predict_allstar/', views.predict_as, name='predict_allstar'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


