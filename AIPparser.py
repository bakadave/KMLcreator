from bs4 import BeautifulSoup
import re

def parser(url, phrase, tableIdx):
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
        res = re.split(r"(BUDAPEST TMA\d?\/\w?|BUDAPEST TMA\d?)|(FL\s\d\d\d)|([0-9]{1,4}\sFT\sALT)", asp)
        res = list(filter(None, res))
        result.append(res)

    return result
    #print(result[1])

if __name__ == "__main__":
    tmaURL = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-2.1-en-HU.html"
    tmaPhrase = "BUDAPEST TMA"
    TMA = parser(tmaURL, tmaPhrase, 3)
    print(TMA[0][4])

    gliderURL = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-5.5-en-HU.html"
    gliderPhrase = "LHSG"
    LHSG = parser(gliderURL, gliderPhrase, 0)
    #print(LHSG[0][3])

