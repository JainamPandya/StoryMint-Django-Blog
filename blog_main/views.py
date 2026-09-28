from django.http import HttpResponse,HttpRequest
from django.shortcuts import render

def home(request):
    return render(request,'home.html')



