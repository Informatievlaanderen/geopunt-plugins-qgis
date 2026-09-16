import os.path
from collections.abc import Iterable
from typing import Optional, Union, List, Tuple

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtGui import QColor

from qgis.core import (
    QgsPoint,
    QgsPointXY,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsGeometry,
    QgsRectangle,
    QgsField,
    QgsProject,
    Qgis,
    QgsCoordinateTransformContext, QgsVectorFileWriter,
    QgsVectorLayer,
    QgsFeature,
    QgsPalLayerSettings,
    QgsTextFormat,
    QgsTextBufferSettings,
    QgsVectorLayerSimpleLabeling,
)
from qgis.gui import QgsVertexMarker
PointLike = Union[QgsPoint, QgsPointXY, Tuple[float, float], List[float]]
class geometryHelper:
    def __init__(self, iface) -> None:
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.adreslayer: Optional[QgsVectorLayer] = None
        self.adresProvider = None
        self.adreslayerid: str = ""

    @staticmethod
    def getMapCrs(iface) -> QgsCoordinateReferenceSystem:
        return iface.mapCanvas().mapSettings().destinationCrs()

    def prjPtToMapCrs(self, xy: PointLike, fromCRS: Union[str, int] = "EPSG:4326") -> QgsPointXY:
        if isinstance(fromCRS, int):
            fromCRS = f"EPSG:{fromCRS}"

        if isinstance(xy, Iterable) and not isinstance(xy, (QgsPoint, QgsPointXY)):
            xy = list(xy)
            point = QgsPointXY(xy[0], xy[1])
        else:
            point = QgsPointXY(xy)

        fromCrs = QgsCoordinateReferenceSystem(fromCRS)
        toCrs = self.getMapCrs(self.iface)
        xform = QgsCoordinateTransform(fromCrs, toCrs, QgsProject.instance())
        return xform.transform(point)

    def prjPtFromMapCrs( self, xy: PointLike, toCRS: Union[str, int] = "EPSG:31370") -> QgsPointXY:
        if isinstance(toCRS, int):
            toCRS = f"EPSG:{toCRS}"

        if isinstance(xy, Iterable) and not isinstance(xy, (QgsPoint, QgsPointXY)):
            xy = list(xy)
            point = QgsPointXY(xy[0], xy[1])
        else:
            point = QgsPointXY(xy)

        toCrs = QgsCoordinateReferenceSystem(toCRS)
        fromCrs = self.getMapCrs(self.iface)
        xform = QgsCoordinateTransform(fromCrs, toCrs, QgsProject.instance())
        return xform.transform(point)

    def prjLineFromMapCrs(self, lineString: Union[QgsGeometry, Iterable[PointLike]], 
                          toCRS: Union[str, int] = "EPSG:4326") -> QgsGeometry:
        if isinstance(toCRS, int):
            toCRS = f"EPSG:{toCRS}"

        fromCrs = self.getMapCrs(self.iface)
        toCrs = QgsCoordinateReferenceSystem(toCRS)
        xform = QgsCoordinateTransform(fromCrs, toCrs, QgsProject.instance())

        wgsLine: List[QgsPoint] = []

        if isinstance(lineString, QgsGeometry):
            wgsLine = [
                QgsPoint(xform.transform(QgsPointXY(pt)))
                for pt in lineString.asPolyline()
            ]
        else:
            wgsLine = [
                QgsPoint(xform.transform(QgsPointXY(list(xy)[0], list(xy)[1])))
                for xy in lineString
            ]

        return QgsGeometry.fromPolyline(wgsLine)

    def prjLineToMapCrs(self, lineString: Union[QgsGeometry, Iterable[PointLike]], 
                        fromCRS: Union[str, int] = "EPSG:4326") -> QgsGeometry:
        if isinstance(fromCRS, int):
            fromCRS = f"EPSG:{fromCRS}"

        fromCrs = QgsCoordinateReferenceSystem(fromCRS)
        toCrs = self.getMapCrs(self.iface)
        xform = QgsCoordinateTransform(fromCrs, toCrs, QgsProject.instance())

        wgsLine: List[QgsPoint] = []

        if isinstance(lineString, QgsGeometry):
            wgsLine = [
                QgsPoint(xform.transform(QgsPointXY(pt)))
                for pt in lineString.asPolyline()
            ]
        else:
            wgsLine = [
                QgsPoint(xform.transform(QgsPointXY(list(xy)[0], list(xy)[1])))
                for xy in lineString
            ]

        return QgsGeometry.fromPolyline(wgsLine)

    def zoomtoPoint(self, point: PointLike, scale: float = 1000.0, crs: Optional[Union[str, int]] = None) -> None:
        if crs is not None:
            pt = self.prjPtToMapCrs(point, crs)
        elif isinstance(point, QgsPoint):
            pt = QgsPointXY(point.x(), point.y())
        elif isinstance(point, QgsPointXY):
            pt = point
        elif isinstance(point, Iterable):
            coords = list(point)
            pt = QgsPointXY(coords[0], coords[1])
        else:
            pt = QgsPointXY(point)

        self.canvas.setCenter(pt)
        self.canvas.zoomScale(scale)
        self.canvas.refresh()

    def zoomtoRec( self, xyMin: PointLike, xyMax: PointLike, crs: Optional[Union[str, int]] = None ) -> None:
        if crs is None:
            crs = self.getMapCrs(self.iface)

        if isinstance(xyMax, Iterable):
            xyMax = QgsPointXY(list(xyMax)[0], list(xyMax)[1])
        if isinstance(xyMin, Iterable):
            xyMin = QgsPointXY(list(xyMin)[0], list(xyMin)[1])

        pmaxpoint = self.prjPtToMapCrs(xyMax, crs)
        pminpoint = self.prjPtToMapCrs(xyMin, crs)

        rect = QgsRectangle(pmaxpoint, pminpoint)
        self.canvas.setExtent(rect)
        self.canvas.refresh()
        if rect.isEmpty() or (rect.width() == 0 and rect.height() == 0):
            self.zoomtoPoint(pminpoint, scale=1000.0)
        else:
            self.canvas.setExtent(rect)
            self.canvas.refresh()

    def zoomtoRec2(self, bounds: List[float], crs: Optional[Union[str, int]] = None) -> None:
        if crs is None:
            crs = self.getMapCrs(self.iface)

        maxpoint = QgsPointXY(bounds[0], bounds[1])
        minpoint = QgsPointXY(bounds[2], bounds[3])

        pmaxpoint = self.prjPtToMapCrs(maxpoint, crs)
        pminpoint = self.prjPtToMapCrs(minpoint, crs)

        rect = QgsRectangle(pmaxpoint, pminpoint)
        self.canvas.setExtent(rect)
        self.canvas.refresh()

    def save_adres_point(self, xy: PointLike, address: str, typeAddress: str = "", 
                         layername: str = "Geopunt_adres", saveToFile: bool = False,  
                         sender=None, startFolder: Optional[str] = None, ) -> None:

        point = QgsPointXY(*xy) if isinstance(xy, (list, tuple)) else QgsPointXY(xy)
        attributes = [
            QgsField("adres", QVariant.String),
            QgsField("type", QVariant.String),
        ]

        mapcrs = self.getMapCrs(self.iface)

        layer, provider = self._getAdresLayer(saveToFile, attributes, layername,
                                               sender, startFolder)
        if layer is None:
            return

        self.adreslayer = layer
        self.adresProvider = provider

        fields = layer.fields()
        fet = QgsFeature(fields)

        xform = QgsCoordinateTransform(
            mapcrs, layer.crs(), QgsProject.instance()
        )
        prjPoint = xform.transform(point)
        fet.setGeometry(QgsGeometry.fromPointXY(prjPoint))

        fet["adres"] = address
        fet["type"] = typeAddress
        provider.addFeatures([fet])

        layer.updateExtents()

        QgsProject.instance().addMapLayer(layer)

        text_format = QgsTextFormat()
        text_format.setSize(12)

        buffer_settings = QgsTextBufferSettings()
        buffer_settings.setEnabled(True)
        buffer_settings.setSize(1)
        buffer_settings.setColor(QColor("white"))

        text_format.setBuffer(buffer_settings)

        palyr = QgsPalLayerSettings()
        palyr.setFormat(text_format)
        palyr.enabled = True
        palyr.fieldName = "adres"
        palyr.placement = QgsPalLayerSettings.Free

        self.adreslayer.setLabelsEnabled(True)
        self.adreslayer.setLabeling(QgsVectorLayerSimpleLabeling(palyr))

        self.adreslayerid = self.adreslayer.id()
        self.canvas.refresh()

    def _pushError(self, message: str) -> None:
        try:
            self.iface.messageBar().pushMessage(
                "geopunt4Qgis", message, level=Qgis.Critical, duration=5)
        except Exception:
            pass

    def _getAdresLayer(self, saveToFile: bool, attributes: List[QgsField],
                       layername: str, sender=None,
                       startFolder: Optional[str] = None):
        """Resolve the layer and write-provider to add a point to.

        A live provider is always returned so ``addFeatures`` never touches a
        dangling (deleted) ``QgsVectorDataProvider``. When the user has
        switched from a temporary (memory) layer to saving to a file, the
        memory layer is exported to a new file and the file layer is used from
        then on, so the previous provider reference is discarded before it can
        be used.
        """
        project = QgsProject.instance()

        # 1. Reuse a layer that is still loaded and whose provider is intact.
        cached_layer = self.adreslayer
        cached_provider = getattr(self, "adresProvider", None)
        cached_ok = (
            cached_layer is not None
            and cached_provider is not None
            and project.mapLayer(cached_layer.id()) is not None
            and cached_provider.isSourceValid()
        )
        if cached_ok:
            if not saveToFile or cached_provider.name() != "memory":
                return cached_layer, cached_provider

            # 2. Memory layer, but the user now wants a file: export it and use
            #    the file layer going forward (drop the memory layer).
            saved = self._saveToFile(sender, startFolder)
            if not saved:
                return None, None
            fpath, fdriver = saved
            if not self._exportLayerTo(cached_layer, fpath, fdriver):
                return None, None
            newlayer, provider = self._openFileLayer(fpath, layername)
            if newlayer is None:
                return None, None
            project.removeMapLayer(cached_layer.id())
            return newlayer, provider

        # 3. No usable cached layer.
        try:
            if saveToFile:
                newlayer, provider = self._saveToFileAndOpen(
                    attributes, layername, sender, startFolder)
                if newlayer is not None:
                    return newlayer, provider

            return self._newMemoryLayer(attributes, layername)
        except RuntimeError:
            self._pushError(
                "Kunnen niet schrijven naar de adreslaag, probeer het opnieuw.")
            return None, None

    def _exportLayerTo(self, layer, fpath: str, driver: str) -> bool:
        opts = QgsVectorFileWriter.SaveVectorOptions()
        opts.fileEncoding = "utf-8"
        opts.driverName = driver
        error, msg, _, _ = QgsVectorFileWriter.writeAsVectorFormatV3(
            layer, fpath, QgsCoordinateTransformContext(), opts)
        if error != QgsVectorFileWriter.NoError:
            self._pushError("Kan de adreslaag niet opslaan: {0}".format(msg))
            return False
        return True

    def _openFileLayer(self, path: str, layername: str):
        layer = QgsVectorLayer(path, layername, "ogr")
        if not layer.isValid() or layer.dataProvider() is None:
            self._pushError(
                "Het adresbestand kon niet geopend worden: {0}".format(path))
            return None, None
        return layer, layer.dataProvider()

    def _saveToFileAndOpen(self, attributes: List[QgsField], layername: str,
                           sender=None, startFolder: Optional[str] = None):
        mem, _ = self._newMemoryLayer(attributes, layername)
        saved = self._saveToFile(sender, startFolder)
        if not saved:
            return None, None
        fpath, fdriver = saved
        if not self._exportLayerTo(mem, fpath, fdriver):
            return None, None
        return self._openFileLayer(fpath, layername)

    def _newMemoryLayer(self, attributes: List[QgsField], layername: str):
        layer = QgsVectorLayer("Point?crs=epsg:31370", layername, "memory")
        if not layer.isValid() or layer.dataProvider() is None:
            return None, None
        layer.dataProvider().addAttributes(attributes)
        layer.updateFields()
        return layer, layer.dataProvider()

    def _saveToFile(self, sender, startFolder: Optional[str] = None) -> Optional[Tuple[str, str]]:
        filter_str = (
            "OGC GeoPackage (*.gpkg);;ESRI Shape Files (*.shp);;"
            "SpatiaLite (*.sqlite);;Geojson File (*.geojson);;"
            "GML ( *.gml);;CSV (*.csv);;MapInfo TAB (*.TAB);;Any File (*.*)"
        )

        fName, _ = QFileDialog.getSaveFileName(
            sender, "open file", directory=startFolder, filter=filter_str
        )

        if not fName:
            return None

        ext = os.path.splitext(fName)[1].upper()

        if "GPKG" in ext:
            flType = "GPKG"
        elif "SHP" in ext:
            flType = "ESRI Shapefile"
        elif "SQLITE" in ext:
            flType = "SQLite"
        elif "GEOJSON" in ext:
            flType = "GeoJSON"
        elif "GML" in ext:
            flType = "GML"
        elif "TAB" in ext:
            flType = "MapInfo File"
        elif "CSV" in ext:
            flType = "CSV"
        else:
            fName += ".shp"
            flType = "ESRI Shapefile"

        return fName, flType

    def addPointGraphic(
        self, xy: PointLike, color: str = "#FFFF00", size: int = 12, pen: int = 1,
        markerType: int = QgsVertexMarker.ICON_BOX, ) -> QgsVertexMarker:

        pt = QgsPointXY(*xy) if isinstance(xy, (list, tuple)) else QgsPointXY(xy)
        marker = QgsVertexMarker(self.canvas)
        marker.setCenter(pt)
        marker.setColor(QColor(0, 0, 0))
        marker.setFillColor(QColor(color))
        marker.setIconSize(size)
        marker.setIconType(markerType)
        marker.setPenWidth(pen)

        return marker

    @staticmethod
    def getBoundsOfPointArray( pointArray: Iterable[PointLike], delta: float = 100) -> List[float]:
        minX = float("inf")
        maxX = float("-inf")
        minY = float("inf")
        maxY = float("-inf")

        for xy in pointArray:
            x, y = list(xy)[:2]
            if x > maxX:
                maxX = x
            if x < minX:
                minX = x
            if y > maxY:
                maxY = y
            if y < minY:
                minY = y

        Xdelta = (maxX - minX) / delta
        Ydelta = (maxY - minY) / delta

        return [minX - Xdelta, minY - Ydelta, maxX + Xdelta, maxY + Ydelta]

    @staticmethod
    def getBoundsOfPoint( xy:PointLike, delta: Optional[float] = None ) -> List[float]:
        x, y = list(xy)[:2]
        if delta is None:
            delta = 300 if x >= 360 else 0.0025

        return [x - delta, y - delta, x + delta, y + delta]