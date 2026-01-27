import json
from ..tools.web import getUrlData


class capakey(object):
    def __init__(self):
        self.baseUrl = "https://geo.api.vlaanderen.be/capakey/v2/" 
    EPSG_CODES =  [31370, 4326, 3857, 3812]

    def getMunicipalities(self):
        url = "{0}/municipality/".format(self.baseUrl)
        response = getUrlData(url)
        municipalities = json.loads(response)
        if municipalities: return municipalities["municipalities"]
        else : return []

    def getMunicipalitieInfo(self, niscode, srs=3812, geometryType="no" ):
        'srs is espg-code:  31370, 4326, 3857, 3812  and geometryType must be: "no", "full", "bbox"'
        data = {}
        if srs in self.EPSG_CODES: 
            data["srs"] = srs
        if geometryType in ["no", "full", "bbox"]: 
            data["geometry"] = geometryType
        
        url = "{0}/municipality/{1}".format( self.baseUrl, niscode )
        response = getUrlData(url, params=data)
        municipality = json.loads(response)
        return municipality

    def getDepartments(self, niscode):
        url = "{0}/municipality/{1}/department/".format( self.baseUrl, niscode)
        response = getUrlData(url)
        departments = json.loads(response)
        if departments: 
            return departments['departments']
        else : 
            return []             

    def getDepartmentInfo(self, niscode, departmentCode, srs=3812, geometryType="no" ):
        'srs is espg-code:  31370, 4326, 3857, 3812  and geometryType must be: "no", "full", "bbox"'
        data = {}
        if srs in self.EPSG_CODES: data["srs"] = srs
        if geometryType in ["no", "full", "bbox"]: data["geometry"] = geometryType

        url = "{0}/municipality/{1}/department/{2}".format(self.baseUrl, niscode, departmentCode)
        response = getUrlData(url, params=data)
        department = json.loads(response)
        return department

    def getSections(self, niscode, departmentCode):
        url = "{0}/municipality/{1}/department/{2}/section/".format( self.baseUrl, niscode, departmentCode)
        response = getUrlData(url)
        secties =  json.loads(response)
        if secties: 
            return secties['sections']
        else :
            return []       

    def getSectionInfo(self, niscode, departmentCode, sectieCode, srs=3812, geometryType="no" ):
        'srs is espg-code: 31370, 4326, 3857, 3812 and geometryType must be: "no", "full", "bbox"'
        data = {}
        if srs in self.EPSG_CODES: data["srs"] = srs
        if geometryType in ["no", "full", "bbox"]: data["geometry"] = geometryType
      
        url = "{0}/municipality/{1}/department/{2}/section/{3}".format( 
                                  self.baseUrl, niscode, departmentCode, sectieCode)
        response = getUrlData(url, params=data )
        sectie = json.loads(response)
        return sectie 

    def getParcels(self, niscode, departmentCode, sectieCode):
        url = "{0}/municipality/{1}/department/{2}/section/{3}/parcel".format( 
                              self.baseUrl, niscode, departmentCode, sectieCode)
        response = getUrlData(url)
        parcels =  json.loads(response)
        if parcels: 
            return parcels['parcels']
        else: 
            return []       
          
    def getParcel(self, niscode, departmentCode, sectieCode, perceelnummer, srs=3812, geometryType="no"):
        'srs is espg-code:  31370, 4326, 3857, 3812 and geometryType must be: "no", "full", "bbox"'
        data = {}
        data["srs"] = srs
        data["geometry"] = geometryType
  
        url = "{0}/municipality/{1}/department/{2}/section/{3}/parcel/{4}".format( 
                              self.baseUrl, niscode, departmentCode, sectieCode, perceelnummer)
        response = getUrlData(url, params=data )
        parcel =  json.loads(response)
        return parcel
