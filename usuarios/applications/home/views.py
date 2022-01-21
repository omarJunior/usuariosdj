from django.shortcuts import render
from django.views.generic import (TemplateView)

# Create your views here.

#Renderizar la vista al home
class HomePage(TemplateView):
    template_name = "home/index.html"


