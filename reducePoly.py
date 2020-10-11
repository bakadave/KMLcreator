from rdp import rdp
from xml.dom import minidom
from simplekml import Kml
from helperFunctions import isClockWise

borderPath = "maps/HUNborder.txt"
# epsilon values:
# 0.1   -> 30 points
# 0.05  -> 68 points
# 0.025 -> 144 points
eps = 0.025

def parseXML():
    xmldoc = minidom.parse('imported maps/HUN_border_HIres.kml')
    itemlist = xmldoc.getElementsByTagName('coordinates')
    dump = itemlist[0].firstChild.nodeValue #extract coordinates from KML
    arr = dump.split(' ') #split coordinate tuples to an array
    coordinates = [] #container to hold coordinates
    for val in arr:
        pair = val.split(',')
        lon = float(pair[0])
        lat = float(pair[1])
        crd = (lon, lat)
        coordinates.append(crd)

    print(len(coordinates))
    return coordinates

def reducePoly(polygon):
    result = []
    mask = rdp(polygon, algo="iter", return_mask = True, epsilon = eps)

    for idx, _ in enumerate(polygon):
        if mask[idx]:
            result.append(polygon[idx])

    print(len(result))
    return result

def Write2file(lst):    
    open(borderPath, 'w').write('\n'.join('%s %s' % x for x in lst))

def createBorderKML():
    kml = Kml(name="Hungary")
    border = kml.newpolygon(name="Hungarian border", outerboundaryis=poly_red)
    border.polystyle.color = '00000f0f'
    kml.save("maps/border.kml")

if __name__ == "__main__":
    poly = parseXML()
    poly_red = reducePoly(poly)

    if not isClockWise(poly_red):
        poly_red.reverse()

    #Write2file(poly_red)
    #createBorderKML()