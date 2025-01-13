from django.shortcuts import render 
from django.http import HttpResponse  
from django.http import JsonResponse 
from . import chart 
# from .predict_as import get_stat_names 
from .predict_as import make_prediction 
import numpy as np 
import sqlalchemy, sys, os, pandas as pd   
from django.conf import settings 
# import make_prediction 
# import get_stat_names 
# import tensorflow as tf 
from .forms import DropDownModelForm 
from decimal import Decimal

# Create your views here.
base_dir = "Main/"
def home(request): 
    template_name=base_dir + 'Home.html'
    return render(request, template_name)

def stats(request):
    template_name=base_dir + 'Stats.html' 
    return render(request, template_name)

def analysis(request):
    template_name=base_dir + 'Analysis.html'
    return render(request, template_name)

def tools(request): 
    template_name=base_dir + 'Tools.html'
    return render(request, template_name) 

def about(request): 
    template_name=base_dir + 'About.html'
    return render(request, template_name)  

def about_content(request):
    template_name='Other/' + 'About-content.html'
    return render(request, template_name)

def stat_manual(request): 
    template_name=base_dir + 'StatManual.html'
    return render(request, template_name)  

def stat_manual_content(request):
    template_name='Other/' + 'StatManual-content.html'
    return render(request, template_name)
    
def load_table(request, page_name):
    template_name = f"Tables/{page_name}.html" 
    return render(request, template_name) 

def load_analysis(request, page_name):
    template_name = f"Analyses/{page_name}.html" 
    return render(request, template_name)

def load_tool(request, page_name):
    template_name = f"Tools/{page_name}.html" 
    return render(request, template_name)

def predict_as(request): 
    if request.method == "POST":
        selected_model = request.POST.get("model") 
        stat_names = request.POST.getlist('stats') 
        stat_vars = [] 
        for i in range(len(stat_names)):
            value = request.POST.get(stat_names[i])   
            try:
                stat_vars.append(float(value)) 
            except (TypeError, ValueError):
                stat_vars.append(0) 
        data = [stat_vars]
        prediction = round(float(make_prediction(stat_names, data, selected_model) * 100), 4)
        return JsonResponse({'prediction': prediction}) 

def dropdown_form(request): 
    form = DropDownModelForm() 
    return render(request, )

# def react_app(request):
#     return render(request, 'index.html') 
