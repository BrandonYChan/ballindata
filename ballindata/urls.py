from django.urls import path, include 
from . import views 
from .views import load_table 
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
    path('load_page/<str:page_name>/', load_table, name='load_table'),
    path('chart/', views.chart, name='chart'), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


