from bs4 import BeautifulSoup
import re
#from urllib.request import urlopen

url = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-2.1-en-HU.html"

with open(url) as fp:
    soup = BeautifulSoup(fp, 'html.parser')

ENR2_1 = [a.get_text() for a in soup.find_all('table')[3]]

#https://regexr.com/ -> for much needed help
#x = re.split(r"(BUDAPEST TMA\d?\/\w?|BUDAPEST TMA\d?)", TMA)
TMA = ENR2_1[1].split("BUDAPEST TMA")
TMA.pop(0)

for idx, _ in enumerate(TMA):
    TMA[idx] = "BUDAPEST TMA" + TMA[idx]

TMAs = []
for row in TMA:
    print(row)
