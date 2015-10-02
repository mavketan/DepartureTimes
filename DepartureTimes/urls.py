"""DepartureTimes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from DepartureTimesApp.views import foo, foo1, foo2, foo3, show_homepage, show_routes, show_directions, show_stops, show_predictions

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'DepartureTimesApp/$', foo),
    url(r'DepartureTimesName/$', foo1),
    url(r'DepartureTimesTemplate/$', foo2),
    url(r'DepartureTimesDB/$', foo3),

    url(r'DepartureTimesApp/$', show_homepage),
    url(r'show_routes/$', show_routes),
    url(r'show_directions/$', show_directions),
    url(r'show_stops/$', show_stops),
    url(r'show_predictions/$', show_predictions),
]
