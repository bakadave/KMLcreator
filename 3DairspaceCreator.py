import re
from helperFunctions import splitCoordinates, altStr2Num
from simplekml import Kml, Folder, AltitudeMode
from pnt2line import distance
from AIPparser import parser

airspaceName_1 = 'BUDAPEST TMA2/A'
line_1 = '474419N 0181530E - 472900N 0181531E - 472421N 0181642E - 472232N 0181709E - 472011N 0181744E - 470324N 0184445E - 471342N 0185839E - 471844N 0185029E - 472115N 0184623E - 472409N 0184140E - 472531N 0183928E - 473231N 0183928E - 473653N 0183928E - 474919N 0185613E - 474914N 0190432E - 474907N 0191518E - 473849N 0193152E - 473835N 0193214E - 474906N 0194628E - 475644N 0193408E - 480519N 0192017E along border HUNGARY_SLOVAKREPUBLIC - 474419N 0181530E'
topAlt_1 = 'FL 195'
bottomAlt_1 = '5500 FT ALT'
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

    def __init__(self, name, gps, top, bottom, clss):
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

if __name__ == "__main__":
    kml = Kml(name="test")
    kml.document = Folder(name="Budapest TMA", open = 1)

    ENR2_1 = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-2.1-en-HU.html"
    tmaPhrase = "BUDAPEST TMA"
    TMA = parser(ENR2_1, tmaPhrase, 3)

    for tma in TMA:
        box = Airspace(tma[0], splitCoordinates(tma[1]), altStr2Num(tma[2]), altStr2Num(tma[3]), tma[4])
        #kml.document = Folder(name=box.name, open = False)
        box.generatePoly()
        print(box.name + " polygon generated")

    kml.save("test.kml")