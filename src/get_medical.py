from query import get_location
from googlesearch import search

'''
RETURNS THE FINAL TOP
SEARCH RESULTS

'''


def get_links(pin):
    location = get_location(str(pin))
    my_loc = location.final_add()

    query = my_loc

    location_links = []
    for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
        location_links.append(j)
    
    return location_links

