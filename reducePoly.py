from rdp import rdp
#import numpy as np
from xml.dom import minidom

xmldoc = minidom.parse('imported maps/HUN_border_HIres.kml')
itemlist = xmldoc.getElementsByTagName('coordinates')
dump = itemlist[0].firstChild.nodeValue #extract coordinates from KML
arr = dump.split(' ') #split coordinate tuples to an array
poly = [] #container to hold coordinates
for val in arr:
    pair = val.split(',')
    lat = float(pair[0])
    lon = float(pair[1])
    crd = (lat, lon)
    poly.append(crd)

print(len(poly))

poly_red = []
mask = rdp(poly, algo="iter", return_mask = True)

print(mask[0:10])

# for idx, item in enumerate(poly):
#     if mask[idx]:
#         poly_red.append(poly[idx])

# print(len(poly_red))