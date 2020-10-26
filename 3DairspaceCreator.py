import re
from helperFunctions import splitCoordinates, altStr2Num, ft2m
from simplekml import Kml, Folder, AltitudeMode
from pnt2line import distance
from AIPparser import parseTMA, parseLHSG

airspaceName_1 = 'BUDAPEST CTR'
line_1 = '473546N 0190523E - 473457N 0190856E - 473230N 0191930E - 472400N 0193400E - 472307N 0193247E - 471632N 0192347E - 471457N 0192138E - 472410N 0190642E - 472613N 0190619E - 472941N 0190336E - 473022N 0190325E - 473038N 0190321E - 473546N 0190523E'
topAlt_1 = '3500 FT ALT'
bottomAlt_1 = 'GND'
clss_1 = 'D'

class Airspace:
    name: str
    points = ()
    airspaceClass: str
    ceiling: int
    floor: int
    numPoints: int
    color: str
    colorDict = {
        'C' : '800000ff',
        'D' : 'ffB222ff',
        'G' : 'ffC0C0C0'
    }

    def __init__(self, name, gps, top, bottom, clss):
        self.name = name
        self.points = gps
        self.airspaceClass = clss
        self.floor = ft2m(bottom)
        self.ceiling = ft2m(top)
        self.numPoints = len(self.points)
        self.color = self.colorDict[self.airspaceClass]

    def generatePoly(self, doc):
        self.upperBoundary(doc)
        self.lowerBoundary(doc)
        self.sides(doc)

    def lowerBoundary(self, doc):
        arr = []
        for x in range(self.numPoints):
            l = list(self.points[x])
            l.append(self.floor)
            arr.append(tuple(l))
        
        floorPoly = doc.newpolygon(name=self.name, outerboundaryis=arr)
        floorPoly.polystyle.color = self.color
        floorPoly.altitudemode = AltitudeMode.absolute
        
        return

    def upperBoundary(self, doc):
        arr = []
        for x in range(self.numPoints):
            l = list(self.points[x])
            l.append(self.ceiling)
            arr.append(tuple(l))

        ceilingPoly = doc.newpolygon(name=self.name, outerboundaryis=arr)
        ceilingPoly.polystyle.color = self.color
        ceilingPoly.altitudemode = AltitudeMode.absolute

        return

    def sides(self, doc):
        for x in range(self.numPoints - 1):
            p1 = list(self.points[x])
            p1.append(self.ceiling)
            p2 = list(self.points[x])
            p2.append(self.floor)
            p3 = list(self.points[x + 1])
            p3.append(self.floor)
            p4 = list(self.points[x + 1])
            p4.append(self.ceiling)
            sides = doc.newpolygon(name=self.name, outerboundaryis=[tuple(p1), tuple(p2), tuple(p3), tuple(p4)])
            sides.polystyle.color = self.color
            sides.altitudemode = AltitudeMode.absolute

        return

desc = "készítette: Baka Dávid\n\
LHHH - Műegyetemi Sportrepülő Egyesület\n\
https://github.com/bakadave/KMLcreator\n\
david.baka@gmail.com"

if __name__ == "__main__":
    kml = Kml(name="test")
    kml.document = Folder(name="Hungary airspaces", open = 1, description=desc)

    ctr = kml.newfolder(name="Budapest CTR")
    BCTR = Airspace(airspaceName_1, splitCoordinates(line_1), altStr2Num(topAlt_1), altStr2Num(bottomAlt_1), clss_1)
    BCTR.generatePoly(ctr)
    print(BCTR.name + " polygon generated")

    tma = kml.newfolder(name="Budapest TMA")

    ENR2_1 = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-2.1-en-HU.html"
    tmaPhrase = "BUDAPEST TMA"
    TMA = parseTMA(ENR2_1, tmaPhrase, 3)

    for arsp in TMA:
        box = Airspace(arsp[0], splitCoordinates(arsp[1]), altStr2Num(arsp[2]), altStr2Num(arsp[3]), arsp[4])
        fld = tma.newfolder(name=box.name, open = False)
        box.generatePoly(fld)
        print(box.name + " polygon generated")

    glid = kml.newfolder(name="Glider areas")
    ENR5_5 = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-5.5-en-HU.html"
    lhsgPhrase = "LHSG"
    LHSG = parseLHSG(ENR5_5, lhsgPhrase, 0)

    for arsp in LHSG:
        box = Airspace(arsp[0], splitCoordinates(arsp[6]), altStr2Num(arsp[12]), altStr2Num(arsp[8]), "G")
        fld = glid.newfolder(name=box.name, open = False)
        box.generatePoly(fld)
        print(box.name + " polygon generated")

    kml.savekmz("test.kmz")