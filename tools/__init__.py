import xml.etree.ElementTree as ET
from typing import Iterable

def gmlpointToXY(gml:str) -> Iterable[float]:
    root = ET.fromstring(gml)
    xy_s = root.find('.//{http://www.opengis.net/gml/3.2}pos').text
    xy = tuple( map(float, xy_s.split(' ') ) )
    return xy