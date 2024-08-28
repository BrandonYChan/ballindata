from django.shortcuts import render
from django.http import HttpResponse  
from . import chart 

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
