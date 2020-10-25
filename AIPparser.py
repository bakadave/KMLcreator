from bs4 import BeautifulSoup
import re

def parseTMA(url = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-2.1-en-HU.html", phrase = "BUDAPEST TMA", tableIdx = 3):
    result = []

    with open(url) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    #find all tables
    page = [a.get_text() for a in soup.find_all('table')[tableIdx]]


    airspaces = page[1].split(phrase)   #
    airspaces.pop(0)    #remove first item because it is always empty

    for idx, _ in enumerate(airspaces):
        airspaces[idx] = phrase + airspaces[idx]

    for asp in airspaces:
        res = re.split(r"(BUDAPEST TMA\d?\/\w?|BUDAPEST TMA\d?)|(FL\s[0-9]{3})|([0-9]{4}\sFT\sALT)", asp)
        res = list(filter(None, res))
        result.append(res)

    return result
    #print(result[1])

def parseLHSG(url = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-5.5-en-HU.html", phrase = "LHSG", tableIdx = 0):
    result = []

    with open(url) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    #find all tables
    page = [a.get_text() for a in soup.find_all('table')[tableIdx]]


    airspaces = page[1].split(phrase)   #
    airspaces.pop(0)    #remove first item because it is always empty

    for idx, _ in enumerate(airspaces):
        airspaces[idx] = phrase + airspaces[idx]

    #print(airspaces[20])

    for asp in airspaces:
        res = re.split(r"(^LHSG([^\s]+))|((?<=\n)(.*)\w(?=([0-9]{4}\sFT\sALT)|(FL\s[0-9]{3})))|((?<=/\s)(.*)(?<=[^HX]))|(([0-9]{4}\sFT\sALT)|(FL\s[0-9]{3}))", asp)   #https://regexr.com/
        res = list(filter(None, res))
        result.append(res)

    #print(result[0])
    #print(result[6])

    return result
    #print(result[1])

if __name__ == "__main__":
    TMA = parseTMA()
    #print(TMA[0][4])

    LHSG = parseLHSG()
    #print(LHSG[6])
    print(LHSG[7][0] + ", " + LHSG[7][6] + ", "  + LHSG[7][12] + ", " + LHSG[7][8])

