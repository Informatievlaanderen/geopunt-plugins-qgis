import json
from ..tools.web import getUrlData

class Adres(object):
  def __init__(self):
      self.locUrl = "https://geo.api.vlaanderen.be/geolocation/v4/Location"
      self.sugUrl = "https://geo.api.vlaanderen.be/geolocation/v4/Suggestion"
      
  def fetchLocation(self, q: str, c=1):
      try:
        resp = getUrlData(self.locUrl, params={"q": q, "c": c} )
        locationResult = json.loads( resp )
        if "Message" in locationResult:
           return locationResult["Message"]
      except:
         return []
      return locationResult.get("LocationResult", [])

  def fetchSuggestion(self, q: str, c=5):
      suggestion =  json.loads( getUrlData(self.sugUrl, params={"q": q, "c": c} ) )
      return suggestion.get("SuggestionResult", [])
