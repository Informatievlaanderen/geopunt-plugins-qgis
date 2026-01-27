import json, urllib.parse as urlparse
from ..tools.web import getUrlData
from .metadataParser import listServices
from typing import Iterable

from .KEYS import KEYS

API_KEY = KEYS.get('datavindplaats')
BASEURL = "https://datavindplaats.api.vlaanderen.be"

class datavindPlaats(object):
    def __init__(self):
        self.headers ={'x-api-key': API_KEY } 
        self.baseUrl = BASEURL
        self.types = [{'Alles':''}, {'Dataset','type/dataset'}, {'Service':'type/service'}]

    def _suggestions(self, q:str, c:int=10) -> dict:
        url = self.baseUrl + '/v1/catalogrecords/suggestions'
        resp = getUrlData( url, params={'q': q, 'limit': c} , headers=self.headers )
        return json.loads(resp)
    
    def getSuggestions(self, q:str) -> Iterable[str]:
        return self._suggestions(q)["itemListElement"]
    
    def findItems(self, q:str, c:int=100, offset:int=0, taxonomy:str=None):
        url = self.baseUrl + '/v1/catalogrecords'
        params = {'q': q, 'limit': c, 'offset': offset} 
        if taxonomy: 
            params['taxonomy']= taxonomy
        resp =  getUrlData(url, params=params, headers=self.headers)
        return  json.loads(resp)
    
    def findAllItems(self, q:str, taxonomy:str='') -> Iterable[dict]:
        firstReq = self.findItems(q, c=100, offset=0, taxonomy=taxonomy)
        totalItems = firstReq['totalItems']
        items = firstReq['member']
        for offset in range(100, totalItems+1):
            req = self.findItems(q, c=100, offset=offset, taxonomy=taxonomy)
            items += req['member']

        return items
    
    def getItemData(self, identifier:str) -> dict:
        url = self.baseUrl + '/v1/catalogrecords/' + identifier
        resp = getUrlData( url, headers=self.headers)
        return json.loads(resp)
    
    @staticmethod
    def _urlType(url:str) -> str:
        if type(url) is not str:
            return 'other'
        url = url.lower()
        uri = urlparse.urlparse(url)
        if 'rest/services' in uri.path:
            return 'arcgis-fs'
        if 'ogc/features' in uri.path:
            return 'ogc-api'
        if 'wfs' in uri.path or 'ows' in uri.path or 'service=wfs' in uri.query:
            return 'wfs'
        if 'wms' in uri.path or 'service=wms' in uri.query:
            return 'wms'
        if 'wcs' in uri.path or 'service=wcs' in uri.query:
            return 'wcs'
        if 'wmts' in url:
            return 'wmts'
        return 'link'


    def findLinks(self, identifier:str) -> Iterable[dict]:
        links = [n for n in listServices(identifier) if n]

        if links == []:
            rec = self.getItemData(identifier).get("catalogRecord")
            topic = rec.get("primaryTopic")
            if "endpointUrl" in topic:
                url = topic['endpointUrl']
                if url:
                    urltype = self._urlType(url)
                    name = topic.get('title', url) 
                    links.append({'name': name, 'url': url, 'type': urltype})
                
            if "distribution" in topic:
                for distro in topic["distribution"]:
                    accessUrl = distro["accessUrl"] if 'accessUrl' in distro else None 
                    downloadUrl = distro["downloadUrl"] if 'downloadUrl' in distro else None
                    url = accessUrl or downloadUrl
                    if url is None:
                        continue
                    name = distro.get('title', url) 
                    urltype = self._urlType(url)
                    links.append({'name': name, 'url': url, 'type': urltype})

        return links