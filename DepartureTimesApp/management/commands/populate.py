""" command to fetch route/direction/stop details using NextBus API and populate into db"""

from django.core.management.base import BaseCommand, CommandError
from DepartureTimesApp.models import Agency, Route, Direction, Busstop, Stop
from DepartureTimesApp.views import get_agencies, get_route_list, get_route_details

class Command(BaseCommand):
    help = 'Populates database using NextBus API'

    def handle(self, *args, **options):
        self.remove()
        self.add()
    
    def add_agency_info(self, a):
        # Add all route/direction/stops for agency
        routes = get_route_list(a.agency_tag)
        print routes
        for rt in routes:
            print '-------------------New Route-------------------------'
            print 'create Route(route_tag=' + rt +', title=' + routes[rt] + ')'
            r = Route(agency=a, route_tag=rt, title=routes[rt])
            r.save()
            
            xml_root = get_route_details(a.agency_tag, rt) 
            #print xml_root
            for route in xml_root:
                for child in route:
                    if child.tag == 'stop':
                        print 'create Busstop(stop_tag=' +child.attrib['tag']
                        bs = Busstop(stop_tag=child.attrib['tag'], title=child.attrib['title'],
                                     lat=child.attrib['lat'], lon=child.attrib['lon'], stopId=child.attrib['stopId'])
                        bs.save()

                for child in route:
                    if child.tag == 'direction':
                        #r = Route.objects.get(route_tag=rt)
                        print 'create Direction(direction_tag=' +child.attrib['tag']
                        d = Direction(route=r, direction_tag=child.attrib['tag'], title=child.attrib['title'],
                                         name=child.attrib['name'])
                        d.save()
                        for direction_stop in child:
                            print 'create Stop(direction_tag=' + child.attrib['tag'] + ', stop_tag='+direction_stop.attrib['tag']
                            bs = Busstop.objects.get(stop_tag=direction_stop.attrib['tag'])
                            s = Stop(direction=d, stop=bs)
                            s.save()
                    
    def remove(self):
        # Remove all data 
        print '-------------------Deleting all data-----------------'
        Agency.objects.all().delete()
        Route.objects.all().delete()
        Direction.objects.all().delete()
        Busstop.objects.all().delete()
        Stop.objects.all().delete()

    def add(self):
        # Add data for agency sf-muni
        agencies = get_agencies()
        print(len(agencies))
        total_routes = 0
        for at in agencies:
            print "found agency: " + at + ": " + agencies[at]   
            
            if at == 'sf-muni':
                print 'create Agency(agency_tag=' + at+', title='+ agencies[at] +')'
                a = Agency(agency_tag=at, title=agencies[at])
                a.save()

                self.add_agency_info(a) 
