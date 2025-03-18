from django.shortcuts import render
from collaboration.models import Forum
from .models import Category
from datetime import datetime

def add_current_year(request):
    return {'current_year': datetime.now().year}



def home(request):
    return render(request, "base/home.html")
