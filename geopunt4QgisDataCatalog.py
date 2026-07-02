from qgis.PyQt.QtCore import (Qt, QSettings, QTranslator, QCoreApplication)
from qgis.PyQt.QtWidgets import QDialog,  QInputDialog
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from .ui_geopunt4QgisDataCatalog import Ui_geopunt4QgisDataCatalogDlg
from qgis.core import Qgis, QgsProject, QgsRasterLayer, QgsVectorLayer
from .geopunt.metadataParser import (getWmsLayerNames, getWFSLayerNames, get_ogc_api_collections, 
                     getWMTSlayersNames,getWCSlayerNames, makeWFSuri, makeWCSuri, makeOGCAPIuri, makeWMTSuri)
from .geopunt.datavindPlaats import datavindPlaats
from .tools.geometry import geometryHelper
import os, webbrowser
from urllib.parse import urlparse

PLUGIN_DIR = os.path.dirname(__file__)
class geopunt4QgisDataCatalog(QDialog):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.pageSize = 100

        # initialize locale
        locale = QSettings().value("locale/userLocale", "en")[:2]
        localePath = os.path.join(PLUGIN_DIR, 'i18n', 'geopunt4qgis_{}.qm'.format(locale))
        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)
            QCoreApplication.installTranslator(self.translator)

        self._initGui()

    def _initGui(self):
        """setup the user interface"""
        self.ui = Ui_geopunt4QgisDataCatalogDlg()
        self.ui.setupUi(self)
        for btn in self.ui.buttonBox.buttons():
            btn.setAutoDefault(False)
            btn.setDefault(False)


        # get settings
        self.s = QSettings()
        self.dvp = datavindPlaats()
        self.gh = geometryHelper(self.iface)

        # vars
        self.firstShow = True
        self.bronnen = None

        self.resultModel = QStandardItemModel(self)
        self.ui.resultView.setModel(self.resultModel)

        # eventhandlers
        self.ui.pageSlider.rangeChanged.connect(lambda _, _max: self.ui.maxPage.setText(str(_max)) )
        self.ui.pageSlider.valueChanged.connect(self.newPage )

        self.ui.prevBtn.clicked.connect(lambda: self.moveSlider(-1)  )
        self.ui.nextBtn.clicked.connect(lambda: self.moveSlider(1) )
        
        self.ui.zoekBtn.clicked.connect(self.searchData)
        self.ui.addWMSbtn.clicked.connect(self.addWMS)
        self.ui.addWFSbtn.clicked.connect(self.addWFS)
        self.ui.addWCSbtn.clicked.connect(self.addWCS)
        self.ui.addWMTSbtn.clicked.connect(self.addWMTS)
        self.ui.ogcAPIbtn.clicked.connect(self.add_ogcapi)

        self.ui.resultView.clicked.connect(self.resultViewClicked)
        self.ui.buttonBox.helpRequested.connect(lambda: webbrowser.open_new_tab(
            "https://www.vlaanderen.be/geopunt/plug-ins/qgis-plug-in/geopunt-catalogus-in-qgis"))
        self.finished.connect(self.clean)

    def _setModel(self, records):
        self.resultModel.clear()
        for rec in records:
            title = QStandardItem(rec['title'])                 # 0
            identifier = QStandardItem(rec["identifier"])       # 1
            description =  QStandardItem(rec["description"])    # 2
            date_modified = QStandardItem(rec["modified"])      # 3
            accessRights = QStandardItem(rec["accessRights"])   # 4
            self.resultModel.appendRow([title,identifier,description,date_modified,accessRights])

    def show(self):
        QDialog.show(self)
        self.setWindowModality(Qt.WindowModality.NonModal)
        if self.firstShow:
            self.firstShow = False

    # eventhandlers
    def moveSlider(self, pos):
        pageNr = self.ui.pageSlider.value() + pos
        self.ui.pageSlider.setValue( pageNr )
        self.ui.pageLbl.setText( str(pageNr) )

    def newPage(self, pageNr):
        if self.resultModel.rowCount() == 0:
            return
        
        offset = (pageNr-1)*100
        self.searchData(offset=offset)

    def resultViewClicked(self):
        self.clean(True)

        if self.ui.resultView.selectedIndexes():
            row = self.ui.resultView.selectedIndexes()[0].row()

            title = self.resultModel.data(self.resultModel.index(row, 0))
            identifier = self.resultModel.data(self.resultModel.index(row, 1))
            _abstract = self.resultModel.data(self.resultModel.index(row, 2))
            _abstract = _abstract.replace('\r\n', ' <br/>').replace('\n', ' <br/>')
            d =[]
            for word in _abstract.split(' '):
                if word.startswith('https://') or word.startswith('http://'):
                    word_url = f"<a target='_blank' href='{word}'>{word}</a>"
                    d.append(word_url)
                else:
                    d.append(word)
            abstract = ' '.join(d)

            msg = f"""<h2>{title}</h2>
            <div>{abstract}</div><br/>""" 

            links = self.dvp.findLinks(identifier)
            if len(links):
                msg += '<div>Links:</div><br/>'
                for link in links:
                    url = link.get('url')
                    urltype = link.get('type')
                    name = link.get('name', title)
                    description = link.get('description', '')

                    if urltype == 'wms':
                        self.wms = url
                        self.wms_lyr = name
                        self.ui.addWMSbtn.setEnabled(1)

                    if urltype == 'wfs':
                        self.wfs = url 
                        self.wfs_lyr = name
                        self.ui.addWFSbtn.setEnabled(1)

                    if urltype == 'wcs':
                        self.wcs = url
                        self.wcs_lyr = name
                        self.ui.addWCSbtn.setEnabled(1)

                    if urltype == 'wmts':
                        self.wmts = url
                        self.wmts_lyr = name
                        self.ui.addWMTSbtn.setEnabled(1)

                    if urltype == 'ogc-api':
                        self.ogcfeats = url
                        self.ogcfeats_lyr = name
                        self.ui.ogcAPIbtn.setEnabled(1)
                    
                    if urltype == 'arcgis-fs':
                        self.arcgis = url
                        self.arcgis_lyr = title
                        self.ui.ogcAPIbtn.setEnabled(1)

                    msg += f"<a target='_blank' title='{description}' href='{url}'>{name}</a> ({urltype})<br/>"

            msg +=   QCoreApplication.translate("geopunt4QgisPoidialog", f"""<div>
             <a href='https://metadata.vlaanderen.be/srv/dut/catalog.search#/metadata/{identifier}'>
             Ga naar metadata fiche</a></div>""")

            self.ui.descriptionText.setText(msg)

    def searchData(self, offset=0):
        self.zoek = self.ui.zoekTxt.text()
        dataType = None
        if  self.ui.typeCbx.currentText() == 'Service' :
            dataType = 'type/service'
        elif  self.ui.typeCbx.currentText() == 'Dataset' :
            dataType = 'type/dataset'
        data = self.dvp.findItems(self.zoek, self.pageSize, offset=int(offset), taxonomy=dataType)
        maxsize = (data['totalItems'] //  self.pageSize) +1
        self.ui.pageSlider.setMaximum(maxsize)
        self.ui.countLbl.setText(f"Aantal gevonden: {data['totalItems']} -> {maxsize} pagina's van {self.pageSize} records" )
        self.parse_searchResults(data['member'])

    def parse_searchResults(self, data):
        if len(data) == 0:
            self.iface.messageBar().pushMessage(
                QCoreApplication.translate("geopunt4QgisPoidialog", "Waarschuwing "),
                QCoreApplication.translate("geopunt4QgisPoidialog",
                        "Er werden geen resultaten gevonde voor deze zoekopdracht"), duration=5)
            return
        self.ui.descriptionText.setText('')
        self._setModel( data )

    def addWMS(self):
        if self.wms is None: 
            return
        lyrs = getWmsLayerNames(self.wms, self.wms_lyr)

        if len(lyrs) == 0:
            self.iface.messageBar().pushMessage("WMS",
                QCoreApplication.translate("geopunt4QgisDataCatalog", 
                     f"Kan geen lagen vinden in: {self.wms}" ), level=Qgis.Warning, duration=10)
            return
        elif len(lyrs) == 1:
            layerTitle = lyrs[0][1]
            layerName  = lyrs[0][0]
        else: 
            layerTitle, accept = QInputDialog.getItem(self, "WMS toevoegen",
                            "Kies een laag om toe te voegen", [n[1] for n in lyrs], editable=0)
            if not accept: return
            layerName = [n[0] for n in lyrs if n[1] == layerTitle][0]
        
        crs = self.gh.getMapCrs(self.iface).authid()
        if  crs != 'EPSG:31370' or crs != 'EPSG:3857' or crs != 'EPSG:3043' or crs != 'EPSG:3812':
            crs = 'EPSG:31370'
        
        p = urlparse(self.wms)
        url = f"{p.scheme}://{p.netloc}{p.path}"

        wmsUrl = f"contextualWMSLegend=0&dpiMode=7&url={url}&layers={layerName}&styles=&format=image/png&crs={crs}"
        rlayer = QgsRasterLayer(wmsUrl, layerTitle, 'wms')
        if rlayer.isValid():
            QgsProject.instance().addMapLayer(rlayer)
        else:
            self.iface.messageBar().pushMessage("Error",
                 QCoreApplication.translate("geopunt4QgisDataCatalog", "Kan WMS niet laden"),
                 level=Qgis.Critical, duration=10)

    def addWMTS(self):
        if self.wmts is None: 
            return
        lyrs = getWMTSlayersNames(self.wmts, self.wmts_lyr)

        if len(lyrs) == 0:
            self.iface.messageBar().pushMessage("WMTS",
                QCoreApplication.translate("geopunt4QgisDataCatalog", 
                     f"Kan geen lagen vinden in: {self.wmts}" ), level=Qgis.Warning, duration=10)
            return
        elif len(lyrs) == 1:
           
            layerName  = lyrs[0][0]
            layerTitle = lyrs[0][1]
            matrix_    = lyrs[0][2]
            format_    = lyrs[0][3]
            srs_       = lyrs[0][4]
        else: 
            layerTitle, accept = QInputDialog.getItem(self, "WMTS toevoegen",
                            "Kies een laag om toe te voegen", [n[1] for n in lyrs], editable=0)
            if not accept: 
                return

            layerName = next(n[0] for n in lyrs if n[1] == layerTitle)
            matrix_   = next(n[2] for n in lyrs if n[1] == layerTitle)
            format_   = next(n[3] for n in lyrs if n[1] == layerTitle)
            srs_      = next(n[4] for n in lyrs if n[1] == layerTitle)

        srs = self.gh.getMapCrs(self.iface).authid() if not srs_ else srs_
        wmsUrl = makeWMTSuri(self.wmts, layer=layerName, tileMatrixSet=matrix_, format=format_, crs=srs )

        rlayer = QgsRasterLayer(wmsUrl, layerTitle, 'wms')
        if rlayer.isValid():
            QgsProject.instance().addMapLayer(rlayer)
        else:
            raise Exception(f"Error loading {layerTitle}: {self.wmts}; {rlayer.error().message()}")
    
    def addWFS(self):
        if self.wfs is None: 
            return
        lyrs, version = getWFSLayerNames(self.wfs, self.wfs_lyr)

        if len(lyrs) == 0:
            self.iface.messageBar().pushMessage("WFS",
                 QCoreApplication.translate("geopunt4QgisDataCatalog",
                 "Kan geen lagen vinden in: %s" % self.wfs), level=Qgis.Warning, duration=10)
            return
        elif len(lyrs) == 1:
            layerName = lyrs[0][0]
            layerTitle = lyrs[0][1]
        else:
            layerTitle, accept = QInputDialog.getItem(self, "WFS toevoegen",
                    "Kies een laag om toe te voegen", [n[1] for n in lyrs], editable=0)
            if not accept: 
                return
            layerName = next(n[0] for n in lyrs if n[1] == layerTitle)
        crs = next( n[2] for n in lyrs if n[0] == layerName)
        wfsUri = makeWFSuri(self.wfs, layerName, srsname=crs, version=version )
        vlayer = QgsVectorLayer(wfsUri, layerTitle, "WFS")
        if vlayer.isValid():
            QgsProject.instance().addMapLayer(vlayer)
        else:
            raise Exception(f"Error loading {layerTitle}: {self.wfs}; {vlayer.error().message()}")

    def addWCS(self):
        if self.wcs is None: return
        lyrs = getWCSlayerNames(self.wcs, self.wcs_lyr) 

        if len(lyrs) == 0:
            self.iface.messageBar().pushMessage("WCS",
                 QCoreApplication.translate("geopunt4QgisDataCatalog",
                 "Kan geen lagen vinden in: %s" % self.wcs), level=Qgis.Warning, duration=10)
            return
        elif len(lyrs) == 1:
            layerName  = lyrs[0][0]
            layerTitle = lyrs[0][1]
        else:
            layerTitle, accept = QInputDialog.getItem(self, "WCS toevoegen",
                    "Kies een laag om toe te voegen", [n[1] for n in lyrs], editable=0)
            if not accept: 
                return
            layerName = next(n[0] for n in lyrs if n[1] == layerTitle)

        wcsUri = makeWCSuri(self.wcs, layerName)
        vlayer = QgsRasterLayer(wcsUri, layerTitle, "wcs")
        if vlayer.isValid():
            QgsProject.instance().addMapLayer(vlayer)
        else:
            raise Exception(f"Error loading {layerTitle}: {self.wcs}; {vlayer.error().message()}")

    def add_ogcapi(self):
        if self.ogcfeats is None and self.arcgis is None: 
            return
        
        if self.arcgis is not None:
            vlayer = QgsVectorLayer( f'url={self.arcgis}', self.arcgis_lyr, "arcgisfeatureserver")
        else:
            lyrs = get_ogc_api_collections(self.ogcfeats, self.ogcfeats_lyr) 
            
            if len(lyrs) == 0:
                self.iface.messageBar().pushMessage("OGC-API",
                    QCoreApplication.translate("geopunt4QgisDataCatalog",
                    "Kan geen lagen vinden in: %s" % self.ogcfeats), level=Qgis.Warning, duration=10)
                return
            elif len(lyrs) == 1:
                layerName  = lyrs[0][0]
                layerTitle = lyrs[0][1]
            else:
                layerTitle, accept = QInputDialog.getItem(self, "OGC laag toevoegen",
                        "Kies een laag om toe te voegen", [n[1] for n in lyrs], editable=0)
                if not accept: 
                    return
                layerName = [n[0] for n in lyrs if n[1] == layerTitle][0]

            ogcUri = makeOGCAPIuri(self.ogcfeats, layerName)
            vlayer = QgsVectorLayer(ogcUri, layerTitle, "ogr")

        if vlayer.isValid():
            QgsProject.instance().addMapLayer(vlayer)
        else:
            raise Exception(f"Error loading {layerTitle}: {ogcUri}; {vlayer.error().message()}")

    def clean(self, partial=False):
        if not partial:
            self.resultModel.clear()
            self.ui.zoekTxt.clear()
            self.ui.countLbl.setText("")

        self.ui.descriptionText.setText('')
        self.wms = self.wmts = self.wfs = self.wcs = self.ogcfeats = self.arcgis = None
        self.wms_lyr= self.wmts_lyr= self.wfs_lyr= self.wcs_lyr= self.ogcfeats_lyr= self.arcgis_lyr = ''
        self.ui.addWMSbtn.setEnabled(0)
        self.ui.addWFSbtn.setEnabled(0)
        self.ui.addWMSbtn.setEnabled(0)
        self.ui.addWMTSbtn.setEnabled(0)
        self.ui.addWCSbtn.setEnabled(0)
        self.ui.ogcAPIbtn.setEnabled(0)