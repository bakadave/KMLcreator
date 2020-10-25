from bs4 import BeautifulSoup
import re
#from urllib.request import urlopen

url = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-2.1-en-HU.html"

with open(url) as fp:
    soup = BeautifulSoup(fp, 'html.parser')

ENR2_1 = [a.get_text() for a in soup.find_all('table')[3]]

TMA = ENR2_1[1].split("BUDAPEST TMA")
TMA.pop(0)

for idx, _ in enumerate(TMA):
    TMA[idx] = "BUDAPEST TMA" + TMA[idx]

tma1 = re.split(r"(BUDAPEST TMA\d?\/\w?|BUDAPEST TMA\d?)|(FL\s\d\d\d)|([0-9]{1,4}\sFT\sALT)", TMA[1])
tma1 = list(filter(None, tma1))
print(tma1[3])
