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
    QgsVectorFileWriter,
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

        if not QgsProject.instance().mapLayer(self.adreslayerid):
            self.adreslayer = QgsVectorLayer(
                "Point?crs=epsg:31370", layername, "memory"
            )
            self.adresProvider = self.adreslayer.dataProvider()
            self.adresProvider.addAttributes(attributes)
            self.adreslayer.updateFields()

        fields = self.adreslayer.fields()
        fet = QgsFeature(fields)

        xform = QgsCoordinateTransform(
            mapcrs, self.adreslayer.crs(), QgsProject.instance()
        )
        prjPoint = xform.transform(point)
        fet.setGeometry(QgsGeometry.fromPointXY(prjPoint))

        fet["adres"] = address
        fet["type"] = typeAddress
        self.adresProvider.addFeatures([fet])

        self.adreslayer.updateExtents()

        if saveToFile and not QgsProject.instance().mapLayer(self.adreslayerid):
            save = self._saveToFile(sender, startFolder)
            if save:
                fpath, flType = save
                error, _ = QgsVectorFileWriter.writeAsVectorFormat(
                    self.adreslayer,
                    fileName=fpath,
                    fileEncoding="utf-8",
                    driverName=flType,
                )
                if error == QgsVectorFileWriter.NoError:
                    self.adreslayer = QgsVectorLayer(fpath, layername, "ogr")
                    self.adresProvider = self.adreslayer.dataProvider()
                else:
                    return
            else:
                return

        QgsProject.instance().addMapLayer(self.adreslayer)

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