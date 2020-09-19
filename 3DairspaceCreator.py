import re
from typing import NamedTuple

#lat = '472011N'
#lon = '0181744E'

airspaceName = 'BUDAPEST TMA1'
line = '472011N 0181744E - 470220N 0182212E - 465337N 0190031E - 465726N 0185421E - 470324N 0184445E - 472011N 0181744E'
topAlt = 'FL 195'
bottomAlt = '9500 FT ALT'
clss = 'C'

class Coordinate(NamedTuple):
    lat: int = []
    lon: int = []

class Airspace(NamedTuple):
    name: str
    points: Coordinate
    clss: str
    top: int
    bottom: int

def splitCoordinates(string):
    coordinate = Coordinate()
    arr = string.split(' - ')
    for coord in arr:
        coordinate.lat.append(coordStr2Num(coord.partition(' ')[0]))
        #print(str(lat[idx]) + "°")
        coordinate.lon.append(coordStr2Num(coord.rpartition(' ')[2]))
        #print(str(lon[idx]) + "°")
    
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
    tma1 = Airspace(airspaceName, splitCoordinates(line), clss, altStr2Num(topAlt), altStr2Num(bottomAlt))
    print(tma1)