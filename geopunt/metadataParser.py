import json
from pathlib import Path
from urllib.parse import urlparse, unquote, urlencode
from ..tools.web import getUrlData
import xml.etree.ElementTree as ET

def listServices(meta_id):
    meta_url = f"https://metadata.vlaanderen.be/srv/dut/csw?service=CSW&version=2.0.2&request=GetRecordById&id={meta_id}&ElementSetName=full"        
    response = getUrlData(meta_url)
    mdata = ET.fromstring(response)
    record = mdata.find("{http://www.opengis.net/cat/csw/2.0.2}Record")
    if not record:
        return
    links= record.findall('{http://purl.org/dc/elements/1.1/}URI')

    for link in links:
        _url = link.text 
        if not _url:
            continue
    
        _p = urlparse(_url)
        baseurl = f"{_p.scheme}://{_p.netloc}{_p.path}"
        protocol = link.attrib.get("protocol", 'link')
        layername = link.attrib.get("name", _p.netloc )
        description = link.attrib.get("description", '')
        url_type = protocol
        url = _url

        if 'OGC:WMS' in protocol.upper():
            url_type = 'wms'
            url = baseurl
        elif 'OGC:WFS' in protocol.upper():
            url_type = 'wfs'
            url = baseurl
        elif 'OGC:WMTS' in protocol.upper():
            url_type = 'wmts'
            url = baseurl
        elif 'OGC:WCS' in protocol.upper():
            url_type = 'wcs'
            url = baseurl
        elif 'ogc:ogc-api-features' in protocol.lower():
            url_type = 'ogc-api'
            url = baseurl
        yield {
            "description": description, 'name': layername, 'url': url,'type': url_type
        } 


def getWmsLayerNames( url='',  name_test=None):
    p = urlparse(url)
    baseurl = f"{p.scheme}://{p.netloc}{p.path}"
    if not "request=getcapabilities" in p.query.lower():
      capability = baseurl + "?request=GetCapabilities&version=1.3.0&service=wms"
    else:
      capability = url
        
    response = getUrlData(capability )
    result = ET.fromstring(response)
    layers =  result.findall( ".//{http://www.opengis.net/wms}Layer" ) + result.findall( ".//Layer" ) 
    layerNames=[]

    for lyr in layers:
      name= lyr.find("{http://www.opengis.net/wms}Name")
      if name is None: name= lyr.find("Name")
      title = lyr.find("{http://www.opengis.net/wms}Title")
      if title is None: title = lyr.find("Title")
      style = lyr.find("{http://www.opengis.net/wms}Style/{http://www.opengis.net/wms}Name")
      if ( name != None) and ( title != None ):
         if style == None: layerNames.append(( name.text, title.text, ''))
         else: layerNames.append(( name.text, title.text, style.text))

    if name_test in [l[0] for l in layerNames]:
        return [l for  l in layerNames if l[0] == name_test] 
    return layerNames

def getWFSLayerNames( url, name_test=None):
    p = urlparse(url)
    baseurl = f"{p.scheme}://{p.netloc}{p.path}"
    if not "request=getcapabilities" in p.query.lower() or p.path.lower().endswith("capabilities.xml" ): 
        capability = baseurl + "?request=GetCapabilities&version=2.0.0&service=wfs"
    else: 
        capability = url
        
    response = getUrlData(capability )
    result = ET.fromstring(response)
    version = '1.0.0'
    if 'version' in result.attrib:
        version = result.attrib['version'] 
       
    wfs_ns= {'wfs': 'http://www.opengis.net/wfs/2.0' if version.startswith('2.0.') 
                                                     else 'http://www.opengis.net/wfs' } 
    layers = result.findall( ".//wfs:FeatureType" , wfs_ns)
    layerNames=[]

    for lyr in layers:
        name= lyr.find("wfs:Name", wfs_ns)
        title = lyr.find("wfs:Title", wfs_ns)
        srs = lyr.find("wfs:SRS", wfs_ns)
        if ( name != None) and ( title != None ):
            if srs == None: layerNames.append(( name.text, title.text, 'EPSG:31370'))
            else: layerNames.append(( name.text, title.text, srs.text))

    if name_test in [l[0] for l in layerNames]:
        return ([l for  l in layerNames if l[0] == name_test] , version)
    return (layerNames, version)

def getWMTSlayersNames( url,  name_test=None):
    p = urlparse(url)
    baseurl = f"{p.scheme}://{p.netloc}{p.path}"
    if not "capabilities" in p.query.lower() or 'capabilities' in p.path:
        capability = baseurl + "?service=WMTS&request=Getcapabilities"
    else:
        capability = url
            
    response = getUrlData(capability )
    result = ET.fromstring(response)

    content = result.find( "{http://www.opengis.net/wmts/1.0}Contents" )
    layers =  content.findall( "{http://www.opengis.net/wmts/1.0}Layer" )
    layerNames = []

    matrixSets = content.findall("{http://www.opengis.net/wmts/1.0}TileMatrixSet")

    for lyr in layers:
        name= lyr.find("{http://www.opengis.net/ows/1.1}Identifier")
        title = lyr.find("{http://www.opengis.net/ows/1.1}Title")
        matrix = lyr.find("{http://www.opengis.net/wmts/1.0}TileMatrixSetLink/{http://www.opengis.net/wmts/1.0}TileMatrixSet")
        format = lyr.find("{http://www.opengis.net/wmts/1.0}Format")

        srsList = [ n.find("{http://www.opengis.net/ows/1.1}SupportedCRS").text
                    for n in matrixSets if n.find("{http://www.opengis.net/ows/1.1}Identifier").text == matrix.text]

        if srsList: srs =  "EPSG:"+ srsList[0].split(':')[-1]
        else: srs = ""

        if ( name != None) and ( title != None ) and ( matrix != None ) and ( format != None ):
              layerNames.append(( name.text, title.text, matrix.text, format.text, srs ))

    if name_test in [l[0] for l in layerNames]:
        return [l for  l in layerNames if l[0] == name_test] 
    return layerNames

def getWCSlayerNames( url,  name_test=None):
    wcsNS = "http://www.opengis.net/wcs/1.1"
    p = urlparse(url)
    baseurl = f"{p.scheme}://{p.netloc}{p.path}"

    if not "getcapabilities" in p.query.lower():
      capability = baseurl + "?request=GetCapabilities&version=1.1.0&service=wcs"
    else:
      capability = url

    response = getUrlData(capability )

    if 'xmlns:wcs="http://www.opengis.net/wcs/1.1.1"' in response:
        wcsNS = "http://www.opengis.net/wcs/1.1.1"

    result = ET.fromstring(response)
    content = result.find( "{%s}Contents" % wcsNS)
    layers =  content.findall( "{%s}CoverageSummary" % wcsNS)
    layerNames = []

    for lyr in layers:
       Identifier= lyr.find("{%s}Identifier" % wcsNS)
       title = lyr.find("{http://www.opengis.net/ows/1.1}Title")
       if ( Identifier != None) and (title != None):
            layerNames.append(( Identifier.text, title.text ))

    if name_test in [l[0] for l in layerNames]:
        return [l for  l in layerNames if l[0] == name_test] 
    return layerNames

def get_ogc_api_collections(url,  default_name=''):
    p = urlparse(url)
    parts =[ i for i in p.path.split('/') if i != '']

    if 'collections' in parts:
        idx = parts.index('collections')
        path_until = '/'.join(parts[:idx])
        baseurl = f"{p.scheme}://{p.netloc}/{path_until}/collections"
        if len(parts) >= idx+1:
            default_name = parts[idx+1] 
    else:
        baseurl = f"{p.scheme}://{p.netloc}/{p.path}/collections"


    resp = getUrlData( baseurl , params={'f': 'application/json'} )
    collections = json.loads(resp)
    lyrNames = [ (c['id'] , c.get('title', default_name) , c.get('description', ''))
            for c in collections["collections"] if 'id' in c
        ]
    if default_name in [c[0] for c in lyrNames]:
        lyrNames = [ next((r for r in lyrNames if r[0] == default_name) ) ]

    return lyrNames

def makeWFSuri( url, name='', srsname="EPSG:31370", version='1.0.0', bbox=None ):
    p = urlparse(url)
    baseurl = f"{p.scheme}://{p.netloc}{p.path}"
    params = {  'SERVICE': 'WFS',
                'VERSION': version ,
                'REQUEST': 'GetFeature',
                'TYPENAME': name,
                'SRSNAME': srsname }
    if bbox: 
        params['BBOX'] = ",".join([str(s) for s in bbox])

    uri = baseurl + '?' + unquote( urlencode(params) )
    return uri

def makeWMTSuri( url, layer, tileMatrixSet, styles='', format='image/png', crs='EPSG:3857' ):
    p = urlparse(url)
    baseurl = f"{p.scheme}://{p.netloc}{p.path}"
    uri = ( f"crs={crs}"
            f"&dpiMode=7"
            f"&featureCount=10"
            f"&format={format}"
            f"&layers={layer}"
            f"&tileMatrixSet={tileMatrixSet}"
            f"&tilePixelRatio=0"
             '&styles='
            f"&url={baseurl}" )
    print(uri)
    return uri

def makeWCSuri( url, layer ):
    p = urlparse(url)
    baseurl = f"{p.scheme}://{p.netloc}{p.path}"
    uri = f'url={baseurl}&tilePixelRatio=0&identifier={layer}'
    return uri

def makeOGCAPIuri( url, name='' ):
    p = urlparse(url)
    parts =[ i for i in p.path.split('/') if i != '']
    if 'collections' in parts:
        idx = parts.index('collections')
        path_until = '/'.join(parts[:idx])
        baseurl = f"{p.scheme}://{p.netloc}/{path_until}"
    else:
        baseurl = f"{p.scheme}://{p.netloc}/{p.path}"

    uri = (
        f"url={baseurl}"
        f"$typename={name}"
        '&restrictToRequestBBOX=1'
        '&pageSize=10000'
        '&pagingEnabled=enabled'
    )
    return uri


def xmlIsEmpty(xml_file, gmlException=True):
    try:
        tree = ET.parse(xml_file)  
        root = tree.getroot()
        if gmlException and "ExceptionReport" in root.tag:
            return True
        
        return not len(root)
    except:
        return True