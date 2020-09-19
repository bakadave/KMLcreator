import re

lat = '472011N'
lon = '0181744E'

airspaceName = 'BUDAPEST TMA1'
line = '472011N 0181744E - 470220N 0182212E - 465337N 0190031E - 465726N 0185421E - 470324N 0184445E - 472011N 0181744E'
topAlt = 'FL 195'
bottomAlt = '9500 FT ALT'
clss 'C'

def parse(val):
    if val[0] == "0":
        len = 3
    else:
        len = 2
    integer = int(val[:len])
    dec = int(val[len:-1]) / 10000
    return integer + dec

def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

lat = parse(lat)
lon = parse(lon)

[d, m, sd] = dd2dms(lat)
print(str(d) + "°" + str(m) + "'" + str(round(sd,4)) + "\"")

[d, m, sd] = dd2dms(lon)
print(str(d) + "°" + str(m) + "'" + str(round(sd,4)) + "\"")