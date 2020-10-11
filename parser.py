from bs4 import BeautifulSoup
#from urllib.request import urlopen

url = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-2.1-en-HU.html"
#/html/body/div[2]/div/div/div[1]/table[3]/tbody/tr[1]

with open(url) as fp:
    soup = BeautifulSoup(fp, 'html.parser')

table = soup.find_all('table')[3]
for row in table.findAll("tr"):
    cells = row.findAll("td")
    print(cells)