import re
from simplekml import *

#lat = '472011N'
#lon = '0181744E'

airspaceName = 'BUDAPEST TMA1'
line = '472011N 0181744E - 470220N 0182212E - 465337N 0190031E - 465726N 0185421E - 470324N 0184445E - 472011N 0181744E'
topAlt = 'FL 195'
bottomAlt = '9500 FT ALT'
clss = 'C'

class Airspace:
    name: str
    points = ()
    airspaceClass: str
    ceiling: int
    floor: int
    numPoints: int

    def __init__(self, name, gps, clss, top, bottom):
        self.name = name
        self.points = gps
        self.airspaceClass = clss
        self.floor = bottom
        self.ceiling = top
        self.numPoints = len(self.points)

    def lowerBoundary(self):
        arr = []
        for x in range(self.numPoints):
            l = list(self.points[x])
            l.append(self.floor)
            arr.append(tuple(l))
        return arr

    def upperBoundary(self):
        arr = []
        for x in range(self.numPoints):
            l = list(self.points[x])
            l.append(self.ceiling)
            arr.append(tuple(l))
        return arr

#creates a list of tuples from the coordinates
def splitCoordinates(string):
    lst = []
    arr = string.split(' - ')
    for coord in arr:
        lat = coordStr2dms(coord.rpartition(' ')[0])
        lon = coordStr2dms(coord.partition(' ')[2])
        lon = dms2dd(lon)
        lat = dms2dd(lat)
        crd = (lon, lat)
        lst.append(crd)
    
    return lst

def coordStr2dd(val):
    if val[0] == "0":
        len = 3
    else:
        len = 2
    integer = int(val[:len])
    dec = int(val[len:-1]) / 10000
    return integer + dec

def coordStr2dms(val):
    if val[0] == "0":
        len = 3
    else:
        len = 2
    d = int(val[:len])
    m = int(val[len:len+2])
    s = int(val[len+2:-1])
    return [d,m,s]

def altStr2Num(val):
    if ("FL" in val):
        return int(val.partition(' ')[2]) * 100
    if ("FT" in val):
        return int(val.partition(' ')[0])

def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def printDMS(deg):
    print(str(deg[0]) + "°" + str(deg[1]) + "'" + str(round(deg[2],4)) + "\"")

def dms2dd(deg):
    dd = float(deg[0]) + float(deg[1])/60 + float(deg[2]) / (60*60)
    dd = round(dd,5)
    return dd

if __name__ == "__main__":    
    kml = Kml(name="test")
    kml.document = Folder(name="Budapest TMA", open = 1)
    tma1 = Airspace(airspaceName, splitCoordinates(line), clss, altStr2Num(topAlt), altStr2Num(bottomAlt))

    tma_1C = kml.newpolygon(name=tma1.name, outerboundaryis=tma1.lowerBoundary())
    tma_1C.polystyle.color = '990000ff'
    tma_1C.altitudemode = AltitudeMode.absolute

    tma_1F = kml.newpolygon(name=tma1.name, outerboundaryis=tma1.upperBoundary())
    tma_1F.polystyle.color = '990000ff'
    tma_1F.altitudemode = AltitudeMode.absolute

    kml.save("test.kml")
    