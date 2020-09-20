import re
from typing import NamedTuple
import simplekml

#lat = '472011N'
#lon = '0181744E'

airspaceName = 'BUDAPEST TMA4'
line = '474111N 0185850E - 473556N 0185145E - 473355N 0185502E - 473057N 0185951E - 473721N 0190503E - 473827N 0190316E - 474111N 0185850E'
topAlt = 'FL 195'
bottomAlt = '2500 FT ALT'
clss = 'C'

class Coordinate(NamedTuple):
    lon: int = []
    lat: int = []

class Airspace:
    name: str
    lon: int
    lat: int
    airspaceClass: str
    top: int
    bottom: int
    numPoints: int

    def __init__(self, name, gps, airspaceClass, top, bottom):
        self.name = name
        self.lat = gps.lat
        self.lon = gps.lon
        self.clss = airspaceClass
        self.bottom = bottom
        self.top = top
        self.numPoints = len(self.lon)

    def outerboundary(self):
        bdr = '['
        for idx in range(self.numPoints):
            bdr += '('
            bdr += str(self.lon[idx])
            bdr += ','
            bdr += str(self.lat[idx])
            bdr += ',0'
            bdr += ')'
            bdr += ','
        bdr = bdr[:-1]
        bdr += ']'
        return bdr


def splitCoordinates(string):
    coordinate = Coordinate()
    arr = string.split(' - ')
    for coord in arr:
        coordinate.lat.append(coordStr2Num(coord.partition(' ')[0]))
        coordinate.lon.append(coordStr2Num(coord.rpartition(' ')[2]))
    
    return coordinate

def coordStr2Num(val):
    if val[0] == "0":
        len = 3
    else:
        len = 2
    integer = int(val[:len])
    dec = int(val[len:-1]) / 10000
    return integer + dec

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
    print(str(d) + "°" + str(m) + "'" + str(round(sd,4)) + "\"")
    return [d, m, sd]

if __name__ == "__main__":
    kml = simplekml.Kml()
    tma1 = Airspace(airspaceName, splitCoordinates(line), clss, altStr2Num(topAlt), altStr2Num(bottomAlt))
    #kml.newpoint(name=tma1.name, coords=[(tma1.lon[0], tma1.lat[0])])
    print(tma1.outerboundary())
    
    #kml.newpolygon(name=tma1.name, outerboundaryis=[(18.585,47.4111,0),(18.514499999999998,47.3556,0),(18.5502,47.3355,0),(18.5951,47.3057,0),(19.0503,47.3721,0),(19.0316,47.3827,0),(18.585,47.4111,0)])
    #kml.save("test.kml")