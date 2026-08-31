from qgis.PyQt.QtWidgets import QInputDialog
from qgis.PyQt.QtCore import QCoreApplication

def layernameValid(parentObject):   
    if not hasattr(parentObject, 'layerName'):
      layerName, accept = QInputDialog.getText(None,
          QCoreApplication.translate("geopunt4Qgis", 'Laag toevoegen'),
          QCoreApplication.translate("geopunt4Qgis", 'Geef een naam voor de laag op:') )
      if accept == False: 
         return False
      else: 
         parentObject.layerName = layerName
    return True
