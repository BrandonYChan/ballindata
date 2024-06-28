from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
def home(request): 
    return render(request, 'Home.html')

def stats(request):
    return render(request, 'Stats.html')

def analysis(request):
    return render(request, 'Analysis.html')

def about(request): 
    return render(request, 'About.html')  

def about_content(request):
    return render(request, 'About-content.html')
    
def load_table(request, page_name):
    template_name = f"Tables/{page_name}.html" 
    return render(request, template_name) 

def load_other(request, page_name):
    template_name = f"Other/{page_name}.html" 
    return render(request, template_name)