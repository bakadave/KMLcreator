from bs4 import BeautifulSoup

url = "C:/Users/bakad/OneDrive/Desktop/AIRAC/2020-06-18-AIRAC/html/eAIP/LH-ENR-2.1-en-HU.html"
#/html/body/div[2]/div/div/div[1]/table[3]/tbody/tr[1]

with open(url) as fp:
    soup = BeautifulSoup(fp, 'html.parser')

#print(soup.body.find('br', attrs={'id':'ENR212018082312425003910000'}))
print(soup.find_all('Budapest TMA1'))