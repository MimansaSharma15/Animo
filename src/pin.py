import geopy
from geopy import Nominatim

'''
get_add

PARAMS: PINCODE

-->
RETURNS THE LOCATION
AND THE COORDINATE OF THE 
ENTERED PINCODE

'''


class get_add():
    def __init__(self,pin):
        geolocator = Nominatim(user_agent="my application")
        zipcode1 = str(pin)
        self.location = geolocator.geocode(zipcode1)
               
    def address(self):
        return self.location.address
    
    def coordinates(self):
        return self.location.latitude, self.location.longitude
