from django.db import models

# Create your models here.

class Agency(models.Model):

    """ Agenecy info """

    agency_tag = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    regionTitle = models.CharField(max_length=50)
    
    def __str__(self):
        return self.agency_tag

class Route(models.Model):

    """ Route info """

    #agency_tag = models.CharField(max_length=20)
    agency = models.ForeignKey(Agency) 
    route_tag = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Direction(models.Model):

    """ Direction info """

    #route_tag = models.CharField(max_length=20) 
    route = models.ForeignKey(Route)
    direction_tag = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Busstop(models.Model):

    """ Busstop info """

    stop_tag = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    lat = models.FloatField() 
    lon = models.FloatField()
    stopId = models.IntegerField()
    
    def __str__(self):
        return self.title

class Stop(models.Model):

    """ Stop details with direction """

    #direction_tag = models.CharField(max_length=20, primary_key=True)
    #stop_tag = models.CharField(max_length=20, primary_key=True)
    direction = models.ForeignKey(Direction)
    stop = models.ForeignKey(Busstop)
