import os.path
from collections.abc import Iterable
from qgis.PyQt.QtCore import QVariant
from qgis.core import ( QgsPoint, QgsPointXY, QgsCoordinateReferenceSystem, QgsCoordinateTransform, 
                       QgsGeometry, QgsRectangle, QgsField, QgsProject, QgsVectorFileWriter, QgsVectorLayer, 
                       QgsFeature, QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings, 
                       QgsVectorLayerSimpleLabeling)
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtGui import QColor
from qgis.gui import QgsVertexMarker

class geometryHelper(object):
    def __init__(self , iface ):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.adreslayerid = ''
    
    @staticmethod
    def getGetMapCrs(iface):
        return iface.mapCanvas().mapSettings().destinationCrs() 
        
    def prjPtToMapCrs( self, xy , fromCRS="EPSG:4326" ):
        if type(fromCRS) == int: fromCRS = "EPSG:{}".format(fromCRS)

        point = QgsPointXY( list(xy)[0], list(xy)[1] ) if isinstance( xy, Iterable) else QgsPointXY(xy)
        fromCrs = QgsCoordinateReferenceSystem(fromCRS)
        toCrs = self.getGetMapCrs(self.iface)
        xform = QgsCoordinateTransform( fromCrs, toCrs, QgsProject.instance() )
        return   xform.transform( point )
    
    def prjPtFromMapCrs( self, xy , toCRS="EPSG:31370" ):
        if type(toCRS) == int: toCRS = "EPSG:{}".format(toCRS)

        point = QgsPointXY( list(xy)[0], list(xy)[1] ) if isinstance( xy, Iterable) else QgsPointXY(xy)
        toCrs = QgsCoordinateReferenceSystem(toCRS)
        fromCrs = self.getGetMapCrs(self.iface)
        xform = QgsCoordinateTransform( fromCrs, toCrs, QgsProject.instance() )
        return   xform.transform( point )

    def prjLineFromMapCrs(self, lineString, toCRS="EPSG:4326" ):
        if type(toCRS) == int: toCRS = "EPSG:{}".format(toCRS)

        fromCrs = self.getGetMapCrs(self.iface)
        toCrs = QgsCoordinateReferenceSystem(toCRS)
        xform = QgsCoordinateTransform(fromCrs, toCrs, QgsProject.instance() )
        if isinstance(lineString, QgsGeometry):
            wgsLine = [ QgsPoint( xform.transform( QgsPointXY(xy) ) ) for xy in  lineString.asPolyline()]
        if isinstance( lineString, Iterable ):
            wgsLine = [ QgsPoint( xform.transform( QgsPointXY(list(xy)[0], list(xy)[1]) ) ) for xy in  lineString]
        return QgsGeometry.fromPolyline( wgsLine )

    def prjLineToMapCrs(self, lineString, fromCRS="EPSG:4326" ):
        if type(fromCRS) == int: fromCRS = "EPSG:{}".format(fromCRS)

        fromCrs = QgsCoordinateReferenceSystem(fromCRS)
        toCrs = self.getGetMapCrs(self.iface)
        xform = QgsCoordinateTransform(fromCrs, toCrs, QgsProject.instance() )
        if isinstance(lineString, QgsGeometry):
            wgsLine = [ QgsPoint( xform.transform( QgsPointXY(xy) ) ) for xy in  lineString.asPolyline()]
        if isinstance( lineString, Iterable ):
            wgsLine = [ QgsPoint( xform.transform( QgsPointXY(list(xy)[0], list(xy)[1]) ) ) for xy in  lineString]
        return QgsGeometry.fromPolyline( wgsLine )

    def zoomtoRec(self, xyMin, xyMax , crs=None):
        """zoom to rectangle from 2 points with given crs, default= mapCRS"""
        if crs is None:
            crs = self.getGetMapCrs(self.iface)
        
        #convert list ed. to QgsPointXY
        if isinstance( xyMax, Iterable ): xyMax = QgsPointXY( list(xyMax)[0], list(xyMax)[1])
        if isinstance( xyMin, Iterable ): xyMin = QgsPointXY( list(xyMin)[0], list(xyMin)[1])
        
        pmaxpoint = self.prjPtToMapCrs(xyMax, crs)
        pminpoint = self.prjPtToMapCrs(xyMin, crs)
        
        # Create a rectangle to cover the new extent
        rect = QgsRectangle( pmaxpoint, pminpoint )
    
        # Set the extent to our new rectangle
        self.iface.mapCanvas().setExtent(rect)
        # Refresh the map
        self.iface.mapCanvas().refresh()
    
    def zoomtoRec2(self, bounds, crs=None):
        "zoom to rectangle from a list containing: [xmin,ymin,xmax,ymax] with given crs, default= mapCRS"
        if crs is None:
            crs = self.getGetMapCrs(self.iface)
            
        maxpoint = QgsPointXY( bounds[0], bounds[1])
        minpoint = QgsPointXY( bounds[2], bounds[3])
        
        pmaxpoint = self.prjPtToMapCrs(maxpoint, crs)
        pminpoint = self.prjPtToMapCrs(minpoint, crs)
      
        # Create a rectangle to cover the new extent
        rect = QgsRectangle( pmaxpoint, pminpoint )
    
        # Set the extent to our new rectangle
        self.iface.mapCanvas().setExtent(rect)
        # Refresh the map
        self.iface.mapCanvas().refresh()

    def save_adres_point(self, point, address, typeAddress='', layername="Geopunt_adres", 
                                              saveToFile=False, sender=None, startFolder=None ):
        attributes = [QgsField("adres", QVariant.String), QgsField("type", QVariant.String)]
        mapcrs = self.getGetMapCrs(self.iface)
        
        if not QgsProject.instance().mapLayer(self.adreslayerid):
            self.adreslayer = QgsVectorLayer("Point?crs=epsg:31370", layername, "memory")
            self.adresProvider = self.adreslayer.dataProvider()
            self.adresProvider.addAttributes(attributes)
            self.adreslayer.updateFields()

        # add a feature
        fields= self.adreslayer.fields()
        fet = QgsFeature(fields)

        #set geometry and project from mapCRS
        xform = QgsCoordinateTransform( mapcrs, self.adreslayer.crs(), QgsProject.instance() )
        prjPoint = xform.transform( point )
        fet.setGeometry(QgsGeometry.fromPointXY(prjPoint))

        #populate fields
        fet['adres'] = address
        fet['type'] = typeAddress
        self.adresProvider.addFeatures([ fet ])
        ""
        # update layer's extent when new features have been added
        # because change of extent in provider is not propagated to the layer
        self.adreslayer.updateExtents()
        
        # save memoryLAYER to file and replace all references    
        if saveToFile and not QgsProject.instance().mapLayer(self.adreslayerid): 
          save = self._saveToFile( sender, startFolder )
          if save:
             fpath, flType = save                
             error, msg = QgsVectorFileWriter.writeAsVectorFormat(self.adreslayer, fileName=fpath, fileEncoding="utf-8", driverName=flType)
             if error == QgsVectorFileWriter.NoError:
                self.adreslayer = QgsVectorLayer( fpath, layername, "ogr")
                self.adresProvider = self.adreslayer.dataProvider()
             else: 
                del self.adreslayer, self.adresProvider 
                return
          else: 
              del self.adreslayer, self.adresProvider 
              return
          
        #  add to map
        QgsProject.instance().addMapLayer(self.adreslayer)
        
        #labels
        text_format = QgsTextFormat()
        text_format.setSize(12)
        buffer_settings = QgsTextBufferSettings()
        buffer_settings.setEnabled(True)
        buffer_settings.setSize(1)
        buffer_settings.setColor(QColor("white"))
        
        palyr = QgsPalLayerSettings() 
        text_format.setBuffer(buffer_settings)
        palyr.setFormat(text_format)
        
        palyr.enabled = True 
        palyr.fieldName = 'adres' 
        palyr.placement = QgsPalLayerSettings.Free 

        self.adreslayer.setLabelsEnabled(True)
        self.adreslayer.setLabeling( QgsVectorLayerSimpleLabeling(palyr) )
       
        # store layer id and refresh      
        self.adreslayerid = self.adreslayer.id()
        self.canvas.refresh()
      
    def _saveToFile( self, sender, startFolder=None ):
        'save to file'
        filter = "OGC GeoPackage (*.gpkg);;ESRI Shape Files (*.shp);;SpatiaLite (*.sqlite);;Geojson File (*.geojson);;GML ( *.gml);;Comma separated value File (excel) (*.csv);;MapInfo TAB (*.TAB);;Any File (*.*)" 
        Fdlg = QFileDialog()
        Fdlg.setFileMode(QFileDialog.AnyFile)
        fName, __ = QFileDialog.getSaveFileName(sender, "open file", filter=filter, directory=startFolder)
        if fName:
          ext = os.path.splitext( fName )[1]
          if "GPKG" in ext.upper():
            flType = "GPKG"
          elif "SHP" in ext.upper():
            flType = "ESRI Shapefile"
          elif "SQLITE" in ext.upper():
            flType = "SQLite" 
          elif "GEOJSON" in ext.upper():  #no update possible -> hidden
            flType = "GeoJSON"
          elif "GML" in ext.upper():
            flType = "GML"
          elif 'TAB' in ext.upper():
            flType = 'MapInfo File'
          elif 'CSV' in ext.upper():
            flType = 'CSV'
          else:
            fName = fName + ".shp"
            flType = "ESRI Shapefile"
          return (fName , flType )
        else:
            return None
      
    def addPointGraphic(self, xy, color="#FFFF00", size=12, pen=1, markerType=QgsVertexMarker.ICON_BOX ):
        "create a point Graphic at location xy and return it"
        pt = QgsPointXY(xy[0], xy[1]) if isinstance( xy, Iterable) else QgsPointXY(xy)
        m = QgsVertexMarker(self.canvas)
        m.setCenter(pt)
        m.setColor(QColor(0,0,0))
        m.setFillColor(QColor(color))
        m.setIconSize(size)
        m.setIconType(markerType) 
        m.setPenWidth(pen)
        return m

    @staticmethod
    def getBoundsOfPointArray( pointArray, delta=100):
        minX = 1.7976931348623157e+308
        maxX = -1.7976931348623157e+308
        minY = 1.7976931348623157e+308
        maxY = -1.7976931348623157e+308
    
        for xy in pointArray:
            x, y = list(xy)[:2]
            if x > maxX: maxX = x
            if x < minX: minX = x
            if y > maxY: maxY = y
            if y < minY: minY = y
          
        Xdelta = (maxX - minX) /delta
        Ydelta = (maxY - minY) /delta
        
        return [ minX - Xdelta, minY - Ydelta, maxX + Xdelta, maxY + Ydelta]
    
    @staticmethod
    def getBoundsOfPoint( x, y, delta=None):
      if delta is None:
        if x >= 360:
            delta = 300 #x bigger then 360 -> meters
        else:
            delta = 0.0025 #x smaller then 360 -> degrees
      
        xmax = x + delta
        xmin = x - delta
        ymax = y + delta
        ymin = y - delta
        
        return [xmin, ymin, xmax,ymax]
