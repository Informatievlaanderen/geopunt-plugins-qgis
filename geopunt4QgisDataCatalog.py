# -*- coding: utf-8 -*-
"""
/***************************************************************************
geopunt4QgisDataCatalog
                A QGIS plugin
"Tool om geopunt in QGIS te gebruiken"
                -------------------
    begin                : 2014-07-15
    copyright            : (C) 2014 by Kay Warrie
    email                : kaywarrie@gmail.com
***************************************************************************/

/***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************/
"""
from PyQt4 import QtCore, QtGui
from ui_geopunt4QgisDataCatalog import Ui_geopunt4QgisDataCatalogDlg
from qgis.core import *
from qgis.gui import QgsMessageBar 
import metadata, os, json, webbrowser, sys
import geometryhelper as gh

class geopunt4QgisDataCatalog(QtGui.QDialog):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self, None)
        self.setWindowFlags( self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint )
        self.setWindowFlags( self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.iface = iface
    
        # initialize locale
        locale = QtCore.QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(os.path.dirname(__file__), 'i18n', 'geopunt4qgis_{}.qm'.format(locale))
        if os.path.exists(localePath):
            self.translator = QtCore.QTranslator()
            self.translator.load(localePath)
            if QtCore.qVersion() > '4.3.3': QtCore.QCoreApplication.installTranslator(self.translator)
    
        self._initGui()

    def _initGui(self):
        """setup the user interface"""
        self.ui = Ui_geopunt4QgisDataCatalogDlg()
        self.ui.setupUi(self)
        
        self.md = metadata.MDReader()
        self.gh = gh.geometryHelper( self.iface )
        
        #setup a message bar
        self.bar = QgsMessageBar() 
        self.bar.setSizePolicy( QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed )
        self.ui.verticalLayout.addWidget(self.bar)
        
        self.ui.buttonBox.addButton( QtGui.QPushButton("Sluiten"), QtGui.QDialogButtonBox.RejectRole )
        
        #vars
        self.wms = None
        self.dl = None
        self.to = 0
        self.start = 1
        self.count = 0
        self.step = 30
        self.zoek = ''
        
        self.model = QtGui.QStandardItemModel( self )
       
        self.ui.resultView.setModel( self.model )
        
        #eventhandlers 
        self.ui.zoekBtn.clicked.connect(self.onZoekClicked)
        self.ui.addWMSbtn.clicked.connect(self.addWMS)
        self.ui.DLbtn.clicked.connect(lambda: self.openUrl(self.dl))
        self.ui.pageNextBtn.clicked.connect(self.nextPage)
        self.ui.pagePrvBtn.clicked.connect(self.previousPage)
        self.ui.resultView.clicked.connect(self.resultViewClicked)
        self.finished.connect(self.clean)
      
    def _setModel(self, records):   
        self.model.clear()
         
        for rec in records:
            title = QtGui.QStandardItem( rec['title'] )         #0
            wms = QtGui.QStandardItem( rec['wms'] )             #1
            downloadLink = QtGui.QStandardItem(rec['download']) #2
            id = QtGui.QStandardItem( rec['uuid'] )             #3
            abstract  = QtGui.QStandardItem( rec['abstract'] )  #4           
            self.model.appendRow([title,wms,downloadLink,id,abstract])

    #eventhandlers
    def resultViewClicked(self):
        if self.ui.resultView.selectedIndexes(): 
           row = self.ui.resultView.selectedIndexes()[0].row()  
           
           title  = self.model.data( self.model.index( row, 0) )
           self.wms = self.model.data( self.model.index( row, 1) )
           self.dl = self.model.data( self.model.index( row, 2) )
           uuid  = self.model.data( self.model.index( row, 3) )
           abstract = self.model.data( self.model.index( row, 4) )
           
           self.ui.descriptionText.setText(
             """<h3>%s</h3><div>%s</div><br/>
             <a href='https://metadata.geopunt.be/zoekdienst/apps/tabsearch/index.html?uuid=%s'>Ga naar fiche</a>""" % 
              (title , abstract, uuid ))
           
           if self.wms: self.ui.addWMSbtn.setEnabled(1)
           else: self.ui.addWMSbtn.setEnabled(0)
             
           if self.dl: self.ui.DLbtn.setEnabled(1)
           else: self.ui.DLbtn.setEnabled(0)
               
    def onZoekClicked(self):
        self.zoek = self.ui.zoekTxt.text()
        start = 1
        to = self.step
        
        self.search( start, to )  
       
    def previousPage(self):
        start = self.start - self.step
        if start <= 0: return
        
        if self.count == self.to: 
          to =  self.count - ( self.count % self.step )
        else:  
          to =  self.to  - self.step
       
        self.search( start, to) 
      
    def nextPage(self):
        if ( self.start + self.step ) > self.count: return
      
        start = self.start + self.step
        
        if self.count == self.to: 
          to = self.count
        else:  
          to =  self.to  + self.step

        self.search( start, to) 
           
    def search(self, start, to):
        searchResult = self.md.search( self.zoek , start, to )  

        self.count, self.start, self.to = ( searchResult.count, searchResult.start, searchResult.to )
        pages = ((( self.to -1 ) / self.step ) +1 , (self.count /self.step) +1 )
        self.ui.pageLbl.setText( " %s/%s" % pages )
        self.ui.msgLbl.setText("Aantal resultaten: %s" % self.count )
        self._setModel(searchResult.records)

    def openUrl(self, url):
        if url: webbrowser.open_new_tab( url.encode("utf-8") )

    def addWMS(self):
        crs = self.iface.mapCanvas().mapRenderer().destinationCrs().authid()
        if crs != 'EPSG:31370' or  crs != 'EPSG:3857' or  crs != 'EPSG:3043':
           crs = 'EPSG:31370' 
           
        lyrs =  metadata.getWmsLayerNames( self.wms ) 
        if len(lyrs) == 0:
            self.bar.pushMessage("WMS", 
            QtCore.QCoreApplication.translate("geopunt4QgisDataCatalog", "Kan geen lagen vinden in: %s" % self.wms ), 
                                level=QgsMessageBar.WARNING, duration=10)
            return 
        elif len(lyrs) == 1:
            layerTitle = lyrs[0][1]
        else:
            layerTitle, accept = QtGui.QInputDialog.getItem(self, "WMS toevoegen", 
                                              "Kies een laag om toe te voegen", [n[1] for n in lyrs], editable=0) 
            if not accept: return
        
        layerName = [n[0] for n in lyrs if n[1] == layerTitle ][0]
        style = [n[2] for n in lyrs if n[1] == layerTitle ][0]
        url= self.wms.split('?')[0]

        if crs != 'EPSG:31370' or  crs != 'EPSG:3857' : 
           crs = 'EPSG:31370' 
        wmsUrl = "url=%s&layers=%s&format=image/png&styles=%s&crs=%s" % (url, layerName, style , crs) 
        
        try:
            rlayer = QgsRasterLayer(wmsUrl, layerTitle, 'wms') 
            if rlayer.isValid():
               rlayer.renderer().setOpacity(0.8)
               QgsMapLayerRegistry.instance().addMapLayer(rlayer)
            else:  
                self.bar.pushMessage("Error", 
                QtCore.QCoreApplication.translate("geopunt4QgisDataCatalog", "Kan WMS niet laden"), 
                level=QgsMessageBar.CRITICAL, duration=10) 
        except: 
            self.bar.pushMessage("Error", str( sys.exc_info()[1] ), level=QgsMessageBar.CRITICAL, duration=10)
            return 
           
    def clean(self):
        self.model.clear()
        self.ui.zoekTxt.setText("")
        self.ui.descriptionText.setText('')
        self.ui.pageLbl.setText( "0/0" )
        self.ui.msgLbl.setText("" )