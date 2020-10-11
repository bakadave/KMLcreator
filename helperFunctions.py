from math import sin, cos, sqrt, atan2, radians
import sys

borderPath = "imported maps/HUNborder.txt"
border = []

# approximate radius of earth in km
R = 6373.0

#creates a list of tuples from the coordinates
def splitCoordinates(string):
    alongBorder = False
    lst = []
    arr = string.split(' - ')
    for coord in arr:
        lat = dms2dd(coordStr2dms(coord.rpartition(' ')[0]))
        lon = dms2dd(coordStr2dms(coord.partition(' ')[2]))
        crd = (lon, lat)

        #check if national border needs to be inserted after previous point
        if alongBorder:
            handleBorder(lst[-1], crd, lst)
            alongBorder = False

        #if "border" appears in string, border polygon needs to be inserted on next iteration
        if "border" in coord:
            alongBorder = True
 
        lst.append(crd)
    
    return lst

def handleBorder(firstP, lastP, lst):
    if not border:
        importBorder()

    #find closest point in border file to firstP
    minDist = sys.maxsize
    idx1 = 0
    for idx, coord in enumerate(border):
        dst = calculateDistance(firstP, coord)
        if dst < minDist:
            minDist = dst
            idx1 = idx

    #find closest point in border file to lastP
    minDist = sys.maxsize
    idx2 = 0
    for idx, coord in enumerate(border):
        dst = calculateDistance(lastP, coord)
        if dst < minDist:
            minDist = dst
            idx2 = idx
    
    # print(border)
    # print(idx1)
    # print(idx2)

    idx = min(idx1, idx2)
    while idx != (max(idx1, idx2) + 1):
        lst.append(border[idx])
        idx += 1

    # print(firstP)
    # print(lastP)
    
    return

def calculateDistance(pt1, pt2):
    lon1 = radians(pt1[0])
    lat1 = radians(pt1[1])
    lon2 = radians(pt2[0])
    lat2 = radians(pt2[1]) 

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    disatance = R * c
    #print(disatance)

    return disatance

def importBorder():
    with open (borderPath, 'r') as file:
        for line in file:
            line = line[:-1]
            lat = float(line.partition(' ')[2])
            lon = float(line.partition(' ')[0])
            crd = (lon, lat)
            border.append(crd)

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

def crossProduct(a, b):
    z = a[0] * b[1] - b[0] * a[1]
    return z

def isClockWise(lst):
    idx = 0
    sum = 0
    while idx < (len(lst) - 1):
        sum += crossProduct(lst[idx], lst[idx + 1])
        idx +=1
    
    if sum > 0:
        return True
    if sum < 0:
        return False
    else:
        return False