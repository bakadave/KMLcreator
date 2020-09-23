"""
Script:     kmz_kml.py
Author:     
Dan.Patterson@carleton.ca
url: https://community.esri.com/docs/DOC-8814-convert-kmz-to-kml

References: many
Purpose: convert kmz to kml base script
"""
#import sys
import zipfile
#import glob
from xml.dom import minidom

def kmz_to_kml(fname):
    """save kmz to kml"""
    zf = zipfile.ZipFile(fname,'r')
    for fn in zf.namelist():
        if fn.endswith('.kml'):
            content = zf.read(fn)
            xmldoc = minidom.parseString(content)
            out_name = (fname.replace(".kmz",".kml")).replace("\\","/")
            out = open(out_name,'w')
            out.writelines(xmldoc.toxml())
            out.close()
        else:
            print("no kml file")
if __name__ == "__main__":
    fname = r"Drive:\Your_Path_here\GIS_central.kmz"
    kmz_to_kml(fname)