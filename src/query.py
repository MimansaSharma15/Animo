import requests
from pin import get_add

'''
IMPORTING THE get_add CLASS
-->
RETURNS A GENERATED QUERY
FROM THE PINCODE

'''


class get_location():
    def __init__(self,pin): 
        add = get_add(str(pin))
        self.location = add.address()
        coordinates = add.coordinates()
        self.lon, self.lat = coordinates[0], coordinates[1]

    def final_add(self):    
        q = "psychologist near "+str(self.location)
        return q

