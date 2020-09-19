import re
from typing import NamedTuple
import simplekml

#lat = '472011N'
#lon = '0181744E'

airspaceName = 'BUDAPEST TMA1'
line = '472011N 0181744E - 470220N 0182212E - 465337N 0190031E - 465726N 0185421E - 470324N 0184445E - 472011N 0181744E'
topAlt = 'FL 195'
bottomAlt = '9500 FT ALT'
clss = 'C'

class Coordinate(NamedTuple):
    lon: int = []
    lat: int = []

class Airspace(NamedTuple):
    name: str
    lon: int
    lat: int
    airspaceClass: str
    top: int
    bottom: int

    def outerboundary(lat, lon):
        bdr = '('
        idx = 0
        for len(lat) in lon:
            bdr += lat[idx]
            bdr += ','
            bdr += lon[idx]
            bdr += ',0'
            bdr += ')'
            bdr += ','
        bdr = bdr[:-1]


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
    tma1 = Airspace(airspaceName, splitCoordinates(line).lat, splitCoordinates(line).lon, clss, altStr2Num(topAlt), altStr2Num(bottomAlt))
    #kml.newpoint(name=tma1.name, coords=[(tma1.lon[0], tma1.lat[0])])
    #kml.newpolygon(name=tma1.name, outerboundaryis=[(tma1.lon, tma1.lat)])
    #kml.save("test.kml")
    print(tma1.outerboundary)