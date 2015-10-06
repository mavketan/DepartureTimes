from django.shortcuts import render, render_to_response
from models import Agency, Route, Direction, Busstop, Stop
import json
import requests
import xml.etree.ElementTree as ET
import math

# Create your views here.
from django.http import HttpResponse

def get_nearest_busstops(lat1, lon1, r):
    
    all_busstops = Busstop.objects.all()
    nearest_busstops = []
    for bs in all_busstops:
        lat2 = bs.lat
        lon2 = bs.lon
        dist = math.acos(math.sin(math.pi * lat1/180) * math.sin(math.pi * lat2/180) + math.cos(math.pi * lat1/180) * math.cos(math.pi * lat2/180) * math.cos(math.pi * (lon1-lon2)/180)) * 180/math.pi * 60 * 1.1515 * 1.609344
        if dist <= r:
            bs_tuple = (bs.stop_tag, bs.title, bs.lat, bs.lon, bs.stopId) ##
            s_tuple_list = [] ##
            for s in Stop.objects.all().filter(stop__stop_tag=bs.stop_tag):
                agency = s.direction.route.agency.agency_tag
                route_tag = s.direction.route.route_tag
                direction_tag = s.direction.direction_tag
                stop_tag = bs.stop_tag
                #pred = get_predictions(agency, route_tag, direction_tag, stop_tag)
                pred_string = ''
                #if len(pred) == 0:
                #    pred_string = 'No bus for selected route at this time'
                #else:
                #    pred_string = 'Predicted time for vehicles arriving:'
                #    for t in pred:
                #        pred_string = pred_string + t + 'minutes, ' 
                s_tuple = (s.direction.title, s.direction.route.title, s.direction.route.agency.title, pred_string)##
                s_tuple_list.append(s_tuple)    ##
                #bs_tuple = (bs.stop_tag, bs.title, bs.lat, bs.lon, bs.stopId, s.direction.title, s.direction.route.title, s.direction.route.agency.title, pred_string) ##
                #nearest_busstops.append(bs_tuple)##
            busstop = (bs_tuple, s_tuple_list)
            nearest_busstops.append(busstop)
    
    return nearest_busstops

def show_nearest_busstops(request):

    lat1 = float(request.GET['lat'])
    lon1 = float(request.GET['lon'])
    r= float(request.GET['r'])
    busstops = get_nearest_busstops(lat1, lon1, r)
    #busstop_list = list(busstops.values_list('code', flat=True))
    return HttpResponse(json.dumps(busstops), content_type='application/json')

def show_map(request):
    
    lat1 = request.GET.get('lat', False)
    lon1 = request.GET.get('lon', False)
    if lat1 and lon1:
        return render_to_response("map.html", {"lat":lat1, "lon":lon1})
    else:
        return render_to_response("map.html", {"lat":"0", "lon":"0"}); 

def get_agencies():
    
    """ returns all available agencies """

    xml_query_string = 'http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList'
    xml_request = requests.get(xml_query_string)
    agencies = {}
    root = ET.fromstring(xml_request.text)

    for child in root:
        agencies[child.attrib['tag']] = child.attrib['title']
    return agencies

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

def get_route_details(agency, route_tag):

    """ get complete route details """

    xml_query_string = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a='+agency+'&r='+route_tag
    xml_request = requests.get(xml_query_string)
    route_directions = {}
    root = ET.fromstring(xml_request.text)
    
    return root

def get_route_list_db(agency):

    """ returns route list for agency from model """
    
    all_routes = Route.objects.filter(agency__agency_tag=agency)
    routes = {}
    for r in all_routes:
        routes[r.route_tag] = r.title

    return routes
    
def show_routes(request):

    routes = get_route_list_db('sf-muni')
    return HttpResponse(json.dumps(routes), content_type='application/json')

def show_homepage(request):

    #routes = get_route_list_db('sf-muni')
    #return render_to_response("home.html",
    #                            {"routes" : routes})
    lat1 = request.GET.get('lat', False)
    lon1 = request.GET.get('lon', False)
    if lat1 and lon1:
        return render_to_response("home.html", {"lat":lat1, "lon":lon1})
    else:
        return render_to_response("home.html", {"lat":"0", "lon":"0"}); 
    

def get_directions_db(agency, route_tag):

    """ returns directions for given route_tag from model """
    
    all_directions = Direction.objects.filter(route__route_tag=route_tag)
    route_directions = {}
    for d in all_directions:
        route_directions[d.direction_tag] = d.title

    return route_directions

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
    route_directions = get_directions_db('sf-muni', route_tag)

    return HttpResponse(json.dumps(route_directions), content_type='application/json')

def get_stops_db(agency, route_tag, direction_tag):

    """ returns stops for given route and direction from model """
    
    all_stops = Stop.objects.filter(direction__direction_tag=direction_tag)
    stops = {}
    for s in all_stops:
        stops[s.stop.stop_tag] = s.stop.title
        #stops.append(s.stop.title)

    return stops

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
    stops = get_stops_db('sf-muni', route_tag, direction_tag)

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
