from typing import Tuple, Iterator
import numpy as np
from qgis.core import (
    QgsRectangle, QgsProject, QgsCoordinateTransform,
    QgsPointXY, QgsRasterLayer, QgsRaster, QgsStyle, QgsRasterShader,
    QgsColorRampShader, QgsSingleBandPseudoColorRenderer, QgsGeometry
)

URL_DHM = "https://geo.api.vlaanderen.be/el-dtm/wcs"

class dhm:
    def __init__(self) -> None:
        self.dhmlayer = self.dhmLayer()
        self.crs = self.dhmlayer.crs()
        self.dhmProvider = self.dhmlayer.dataProvider()
        self.nodata = self.dhmProvider.sourceNoDataValue(1)
        self.t = QgsCoordinateTransform(QgsProject.instance().crs(), self.crs, QgsProject.instance())

    @staticmethod
    def dhmLayer(dtm_url=URL_DHM) -> QgsRasterLayer:
        """
        Create new Raster layer for the DHM-WCS of Flanders.

        Returns:
            QgsRasterLayer: An instance of the DTM layer.
        """
        url = f"{dtm_url}?IgnoreAxisOrientation=1&dpiMode=7&identifier=EL.GridCoverage.DTM&url={dtm_url}"
        dhmlayer = QgsRasterLayer(url, 'Hoogtemodel', 'wcs') 
        dhmProvider = dhmlayer.dataProvider()
        if dhmlayer.isValid():
            colorRamp = QgsStyle().defaultStyle().colorRamp('Turbo')
            fnc = QgsColorRampShader(0, 200)
            fnc.setColorRampType(QgsColorRampShader.Interpolated)
            fnc.setSourceColorRamp(colorRamp)
            fnc.classifyColorRamp(15)

            shader = QgsRasterShader()
            shader.setRasterShaderFunction(fnc)

            renderer = QgsSingleBandPseudoColorRenderer(dhmProvider, 1, shader)
            renderer.setClassificationMin(0)
            renderer.setClassificationMax(200)
            renderer.setOpacity(0.8)

            dhmlayer.setRenderer(renderer)
            return dhmlayer
        raise Exception(f"Kan hoogte laag niet openen: {dtm_url}")

    def identify(self, xy: QgsPointXY, bbox: QgsRectangle = QgsRectangle(), w: int = 0, h: int = 0) -> Tuple[float, float, float]:
        """
        Identify a point on the DHM.

        Returns:
            Tuple[float, float, float]: (x, y, z) where z is np.nan if off-raster or NoData.
        """
        _xy = self.t.transform(xy)
        _bbox = self.t.transformBoundingBox(bbox)

        ident = self.dhmProvider.identify(_xy, QgsRaster.IdentifyFormatValue, boundingBox=_bbox, width=w, height=h)

        if ident.isValid():
            results = ident.results()
            z = results.get(1, np.nan)
            if z != self.nodata and not z is None:
                return (xy.x(), xy.y(), float(z))
                
        return (xy.x(), xy.y(), np.nan)

    def identifyLine(self, geom: QgsGeometry, dist: float = 50, count: int = None) -> Iterator[Tuple[float, float, float]]:
        """Identify a series of points along a line."""
        if geom.wkbType() != 2: 
            raise Exception("only QgsGeometry of type Line is allowed")
        if count is not None:
            dist = geom.length() / count

        line = geom.densifyByDistance(dist)
        bbox = self.t.transformBoundingBox(geom.boundingBox())
        for pnt in line.asPolyline():
            yield self.identify(pnt, bbox)

    def fetchAsArray(self, geom: QgsGeometry, d: float = 50, c: int = None) -> np.ndarray:
        """
        Identify a series of points along a line into a 2D numpy array.

        Returns:
            np.ndarray: Array with shape (N, 4) where columns are [cum_distance, x, y, z]
        """
        if geom.wkbType() != 2: 
            raise Exception("only QgsGeometry of type Line is allowed")

        dist = geom.length() / c if c is not None else d

        self.t = QgsCoordinateTransform(QgsProject.instance().crs(), self.crs, QgsProject.instance())
        line = geom.densifyByDistance(dist).asPolyline()

        pnt0 = line[0]
        x0, y0, z0 = self.identify(pnt0, geom.boundingBox())
        xyzList = [[x0, y0, z0]] 
        rList = [0.0]

        for pnt in line[1:]:
            x, y, z = self.identify(pnt, geom.boundingBox())
            r = np.sqrt((x - x0)**2 + (y - y0)**2)
            rList.append(r)
            x0, y0 = x, y
            xyzList.append([x, y, z])

        rxyz = np.hstack([np.cumsum(rList).reshape(-1, 1), xyzList])
        return rxyz