from django.shortcuts import render 
from django.http import HttpResponse  
from django.http import JsonResponse 
from . import chart 
from .predict_as import get_stat_names 
from .predict_as import make_prediction 
from .predict_as import get_avg  
import numpy as np 
import sqlalchemy, sys, os, pandas as pd   
from django.conf import settings 
# import make_prediction 
# import get_stat_names 

# Create your views here.
def home(request): 
    return render(request, 'Home.html')

def stats(request):
    return render(request, 'Stats.html')

def analysis(request):
    return render(request, 'Analysis.html')

def tools(request): 
    return render(request, 'Tools.html') 

def about(request): 
    return render(request, 'About.html')  

def about_content(request):
    return render(request, 'About-content.html')

def stat_manual(request): 
    return render(request, 'StatManual.html')  

def stat_manual_content(request):
    return render(request, 'StatManual-content.html')
    
def load_table(request, page_name):
    template_name = f"Tables/{page_name}.html" 
    return render(request, template_name) 

def load_analysis(request, page_name):
    template_name = f"Analyses/{page_name}.html" 
    return render(request, template_name)

def load_tool(request, page_name):
    template_name = f"Tools/{page_name}.html" 
    return render(request, template_name)

def chart(request):
    return render(request, 'Chart.html')

def predict_as(request): 
    if request.method == "POST":
        stat_names = get_stat_names() 
        stat_vars = np.arange(len(stat_names)) 
        for i in range(len(stat_names)):
            value = request.POST.get(stat_names[i]) 
            try:
                stat_vars[i] = float(value)
            except (TypeError, ValueError):
                stat_vars[i] = get_avg(stat_names[i])
        data = [stat_vars] 
        selected_model = request.POST.get("model") 
        prediction = make_prediction(data, selected_model) 
        output = ''  
        prediction ="True" if prediction==1.0 else "False"  
        output = f'All-Star Prediction: {prediction}'
        return JsonResponse({'prediction': output}) 
    
engine = sqlalchemy.create_engine(f"sqlite:///{os.path.join(settings.BASE_DIR, 'ballindata/DB/ballbase.db')}") 
master = pd.read_sql('master_plt', con=engine) 