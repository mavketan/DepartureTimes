# Departure Times

## Description:

Create a service that gives real-time departure time for public transportation (use freely available public API). The app should geolocalize the user.

## Implementation:

- Prototyped project using Django framework
- Used [NextBus](http://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf) XML feed to get predicted bus timing
- New django-admin command "populate" created to get all route/direction/stop information from Nextbus XML feeds and store it in database to provide faster user response. This command needs to be run before deployment to populate the database
	  - Usage:
	python manage.py populate
- Based on user's current location nearby busstops within radius 'r' are displayed
- Detailed information about busstop (like route/direction) are displayed on infowindow for marker click event
- Bus prediction can be obtained by selcting route/direction/stop

## Deployment:

Project is deployed on heroku. Click [here](http://departuretimes.herokuapp.com) to get real time prediction for San Francisco Municipal Transportation Agency.

To spoof geolocation change the browser setting or provide location detail in URL.

Try some examples,
- http://departuretimes.herokuapp.com/?lat=37.7716899&lon=-122.50984
- http://departuretimes.herokuapp.com/?lat=37.7622299&lon=-122.46669
- http://departuretimes.herokuapp.com/?lat=37.7919199&lon=-122.39815
- http://departuretimes.herokuapp.com/?lat=37.7172899&lon=-122.40773
- http://departuretimes.herokuapp.com/?lat=37.7677699&lon=-122.42909

## TODO:

- Add cronjob to update database periodically
- Use PostreSQL (Current implementation uses default database SQLite)
- Make html presentation better
- Add error handling and logging 
- Move JavaScript to /static/ file
