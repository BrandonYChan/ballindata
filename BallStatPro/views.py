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
    
def greatest_season(request): 
    return render(request, 'goat_season.html')