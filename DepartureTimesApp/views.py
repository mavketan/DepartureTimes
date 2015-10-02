from django.shortcuts import render, render_to_response
from models import Line
import json
import requests
import xml.etree.ElementTree as ET

# Create your views here.
from django.http import HttpResponse
def foo(request):
    return HttpResponse("Departure Time App!")

def foo1(request):
    name = "Ketan"
    html = "<html><body>Departure Time App! Hello from %s!</body></html>" % name
    return HttpResponse(html)

def foo2(request):
    return render_to_response("home3.html",
                {"Testing" : "Django Template Inheritance ",
                "HelloHello" : "Departure Time App! Hello World - Django!"})

def foo3(request):
    #return HttpResponse("Departure Time App!")
    return render_to_response("home2.html",
                {"lines" : Line.objects.all()})

def get_route_list(agency):

    """ returns route list for agency """

    # Get XML data containing routeList for sf-muni agency
    xml_query_string = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a='+agency
    xml_request = requests.get(xml_query_string)
    routes = {}
    root = ET.fromstring(xml_request.text)
    for child in root:
        routes[child.attrib['tag']] = child.attrib['title']
    return routes

def show_routes(request):

    routes = get_route_list('sf-muni')
    return HttpResponse(json.dumps(routes), content_type='application/json')

def show_homepage(request):

    routes = get_route_list('sf-muni')
    return render_to_response("home.html",
                                {"routes" : routes})

def get_directions(agency, route_tag):

    """ returns directions for given route_tag """

    xml_query_string = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a='+agency+'&r='+route_tag
    xml_request = requests.get(xml_query_string)
    route_directions = {}
    root = ET.fromstring(xml_request.text)
    for route in root:
        for child in route:
            if child.tag == 'direction':
                route_directions[child.attrib['tag']] = child.attrib['title']

    return route_directions

def show_directions(request):

    route_tag = request.GET['RT']
    route_directions = get_directions('sf-muni', route_tag)

    return HttpResponse(json.dumps(route_directions), content_type='application/json')

def get_stops(agency, route_tag, direction_tag):

    """ returns stops for given route and direction """
    xml_query_string = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a='+agency+'&r='+route_tag
    xml_request = requests.get(xml_query_string)
    stops = []
    root = ET.fromstring(xml_request.text)
    for route in root:
        for child in route:
            if child.tag == 'direction':
                if child.attrib['tag'] == direction_tag:
                    for stop in child:
                        stops.append(stop.attrib['tag'])
    return stops

def show_stops(request):

    route_tag = request.GET['RT']
    direction_tag = request.GET['DT']
    stops = get_stops('sf-muni', route_tag, direction_tag)

    return HttpResponse(json.dumps(stops), content_type='application/json')


def get_predictions(agency, route_tag, direction_tag, stop_tag):

    """ returns predictions for given route and stop """

    xml_query_string = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a='+agency+'&r='+route_tag+'&s='+stop_tag+'&useShortTitles=true'
    xml_request = requests.get(xml_query_string)
    pred = []
    root = ET.fromstring(xml_request.text)
    for prediction in root:
        for direction in prediction:
            for p in direction:
                pred.append(p.attrib['minutes'])
    return pred

def show_predictions(request):

    route_tag = request.GET['RT']
    direction_tag = request.GET['DT']
    stop_tag = request.GET['ST']

    pred = get_predictions('sf-muni', route_tag, direction_tag, stop_tag)

    return HttpResponse(json.dumps(pred), content_type='application/json')
