import re
from simplekml import Kml, Folder, AltitudeMode

airspaceName_1 = 'BUDAPEST TMA1'
line_1 = '472011N 0181744E - 470220N 0182212E - 465337N 0190031E - 465726N 0185421E - 470324N 0184445E - 472011N 0181744E'
topAlt_1 = 'FL 195'
bottomAlt_1 = '9500 FT ALT'
clss_1 = 'C'

class Airspace:
    name: str
    points = ()
    airspaceClass: str
    ceiling: int
    floor: int
    numPoints: int
    color: str
    colorDict = {
        'C' : '990000ff',
        'D' : 'BEB222ff'
    }

    def __init__(self, name, gps, clss, top, bottom):
        self.name = name
        self.points = gps
        self.airspaceClass = clss
        self.floor = bottom
        self.ceiling = top
        self.numPoints = len(self.points)
        self.color = self.colorDict[self.airspaceClass]

    def generatePoly(self):
        self.upperBoundary()
        self.lowerBoundary() 
        self.sides()

    def lowerBoundary(self):
        arr = []
        for x in range(self.numPoints):
            l = list(self.points[x])
            l.append(self.floor)
            arr.append(tuple(l))
        
        floorPoly = kml.newpolygon(name=self.name, outerboundaryis=arr)
        floorPoly.polystyle.color = self.color
        floorPoly.altitudemode = AltitudeMode.absolute
        
        return

    def upperBoundary(self):
        arr = []
        for x in range(self.numPoints):
            l = list(self.points[x])
            l.append(self.ceiling)
            arr.append(tuple(l))

        ceilingPoly = kml.newpolygon(name=self.name, outerboundaryis=arr)
        ceilingPoly.polystyle.color = self.color
        ceilingPoly.altitudemode = AltitudeMode.absolute

        return

    def sides(self):
        for x in range(self.numPoints - 1):
            p1 = list(self.points[x])
            p1.append(self.ceiling)
            p2 = list(self.points[x])
            p2.append(self.floor)
            p3 = list(self.points[x + 1])
            p3.append(self.floor)
            p4 = list(self.points[x + 1])
            p4.append(self.ceiling)
            sides = kml.newpolygon(name=self.name, outerboundaryis=[tuple(p1), tuple(p2), tuple(p3), tuple(p4)])
            sides.polystyle.color = self.color
            sides.altitudemode = AltitudeMode.absolute

        return

#creates a list of tuples from the coordinates
def splitCoordinates(string):
    lst = []
    arr = string.split(' - ')
    for coord in arr:
        lat = dms2dd(coordStr2dms(coord.rpartition(' ')[0]))
        lon = dms2dd(coordStr2dms(coord.partition(' ')[2]))
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
    m = int(val[len:len + 2])
    s = int(val[len + 2:len + 4])
    return [d,m,s]

def altStr2Num(val):
    if ("FL" in val):
        return int(val.partition(' ')[2]) * 100
    if ("FT" in val):
        return int(val.partition(' ')[0])
    if ("GND" in val):
        return int(0)

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
    tma1 = Airspace(airspaceName_1, splitCoordinates(line_1), clss_1, altStr2Num(topAlt_1), altStr2Num(bottomAlt_1))

    kml = Kml(name="test")
    kml.document = Folder(name="Budapest TMA", open = 1)

    tma1.generatePoly()

    kml.save("test.kml")
    