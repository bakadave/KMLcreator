from math import sin, cos, sqrt, atan2, radians
from pnt2line import pnt2line
import sys

borderPath = "maps/HUNborder.txt"
border = []

def ft2m (feet):
    return feet * 0.3048

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

    # find closest point in border file to firstP
    # *we will find this point as an anchor the find the position we need to insert firstP into
    minDist = sys.maxsize
    idx1 = 0
    for idx, coord in enumerate(border):
        dst = calculateDistance(firstP, coord)
        if dst < minDist:
            minDist = dst
            idx1 = idx

    # find the ideal position to insert firstP
    # *firstP needs to be inserted between two points, if the closest point is behind firstP, it needs to be skipped
    # *it is done by examining the distance of the firstP and the two line segments closest to it, if the line segment "after" the closest point is closer,
    # *closest point is shifted
    if pnt2line(firstP,border[idx1 - 1], border[idx1]) > pnt2line(firstP,border[idx1], border[idx1 + 1]):
        idx1 += 1

    #find closest point in border file to lastP
    minDist = sys.maxsize
    idx2 = 0
    for idx, coord in enumerate(border):
        dst = calculateDistance(lastP, coord)
        if dst < minDist:
            minDist = dst
            idx2 = idx

    #find the ideal position to insert lastP
    if pnt2line(lastP,border[idx2 - 1], border[idx2]) > pnt2line(firstP,border[idx2], border[idx2 + 1]):
        idx2 += 1
    

    # handle exception: it is posible that no point needs to be inserted
    if (idx1 == idx2):
        return

    idx = min(idx1, idx2)
    while idx != (max(idx1, idx2) + 1):
        lst.append(border[idx])
        idx += 1
    
    return

# calculates the distance between two points on Earth surface
def calculateDistance(pt1, pt2):
    # approximate radius of earth in km
    R = 6373.0

    lon1 = radians(pt1[0])
    lat1 = radians(pt1[1])
    lon2 = radians(pt2[0])
    lat2 = radians(pt2[1]) 

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

# import national border polygon from file specified in "borderPath"
def importBorder():
    with open (borderPath, 'r') as file:
        for line in file:
            line = line[:-1]
            lat = float(line.partition(' ')[2])
            lon = float(line.partition(' ')[0])
            crd = (lon, lat)
            border.append(crd)

# parses coordinate string from AIP to degree decimal format
def coordStr2dd(val):
    if val[0] == "0":
        len = 3
    else:
        len = 2
    integer = int(val[:len])
    dec = int(val[len:-1]) / 10000
    return integer + dec

# parses coordinate string from AIP to degrees, minutes, seconds format
def coordStr2dms(val):
    if val[0] == "0":
        len = 3
    else:
        len = 2
    d = int(val[:len])
    m = int(val[len:len + 2])
    s = int(val[len + 2:len + 4])
    return [d,m,s]

# converts altitude in string to feet
def altStr2Num(val):
    if ("FL" in val):
        return int(val.partition(' ')[2]) * 100
    if ("FT" in val):
        return int(val.partition(' ')[0])
    if ("GND" in val):
        return int(0)

# degree decimal to degrees, minutes, seconds (DMS) converter
def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

# prints DMS in a pretty format
def printDMS(deg):
    print(str(deg[0]) + "°" + str(deg[1]) + "'" + str(round(deg[2],4)) + "\"")

# degrees, minutes, seconds (DMS) to degree decimal converter
def dms2dd(deg):
    dd = float(deg[0]) + float(deg[1])/60 + float(deg[2]) / (60*60)
    dd = round(dd,5)
    return dd

# returns the cross product of 2D vectors
def crossProduct(a, b):
    return a[0] * b[1] - b[0] * a[1]

# determines polgon rotation
# returns True for CW and False for CCW
def isClockWise(lst):
    idx = 0
    sum = 0
    while idx < (len(lst) - 1):
        sum += crossProduct(lst[idx], lst[idx + 1])
        idx +=1
    
    # cross product is positive if rotation is clockwise
    if sum > 0:
        return True
    if sum < 0:
        return False
    else:
        return False


if __name__ == "__main__":
    splitCoordinates("474541N 0183928E along border HUNGARY_SLOVAKREPUBLIC - 474548N 0182806E - 472827N 0182806E - 472956N 0183216E - 473231N 0183928E - 474541N 0183928E")