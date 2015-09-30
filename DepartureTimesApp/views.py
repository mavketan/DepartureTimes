from django.shortcuts import render, render_to_response
from models import Line

# Create your views here.
from django.http import HttpResponse
def foo(request):
    return HttpResponse("Departure Time App!")

def foo1(request):
    name = "Ketan"
    html = "<html><body>Departure Time App! Hello from %s!</body></html>" % name
    return HttpResponse(html)

def foo2(request):
    return render_to_response("home.html",
                {"Testing" : "Django Template Inheritance ",
                "HelloHello" : "Departure Time App! Hello World - Django!"})

def foo3(request):
    #return HttpResponse("Departure Time App!")
    return render_to_response("home2.html",
                {"lines" : Line.objects.all()})

