from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QCursor, QColor
from qgis.core import QgsGeometry, QgsPointXY, QgsWkbTypes
from qgis.gui import QgsMapTool, QgsRubberBand

class lineTool(QgsMapTool):
    def __init__(self, iface, callback):
        QgsMapTool.__init__(self,iface.mapCanvas())
        self.iface  = iface
        self.canvas = iface.mapCanvas()
        self.cursor = QCursor(Qt.CursorShape.CrossCursor)
        self.callback   = callback
        
        self.rubberBand = QgsRubberBand(self.canvas, geometryType
                                        =QgsWkbTypes.LineGeometry)
        self.points  = []
        self.rubberBand.setColor( QColor('red') )
        self.rubberBand.setWidth(1)

    def canvasReleaseEvent(self,event):
        if event.button() == Qt.MouseButton.RightButton:
          self.points.append(QgsPointXY( self.toMapCoordinates( event.pos()) ) )
          if len(self.points) <= 1 : 
              return
        
          self.rubberBand.setToGeometry( QgsGeometry.fromPolylineXY(self.points), None )
          self.callback( self.rubberBand )
          QgsMapTool.deactivate(self)
        else:
          self.points.append(QgsPointXY( self.toMapCoordinates(event.pos()) ) )
          if len(self.points) <= 1 : 
              return
          self.rubberBand.setToGeometry( QgsGeometry.fromPolylineXY(self.points), None )

    def canvasDoubleClickEvent(self,event):
        self.points.append(QgsPointXY( self.toMapCoordinates( event.pos()) ))
        if len(self.points) <= 1 : 
            return
      
        self.rubberBand.setToGeometry( QgsGeometry.fromPolylineXY(self.points), None )
        self.callback( self.rubberBand )
        QgsMapTool.deactivate(self)
    
    def canvasMoveEvent(self, event):
        if len(self.points) >= 1:
            current_point = self.toMapCoordinates(event.pos())
            temp_points = self.points + [current_point]
            self.rubberBand.setToGeometry(QgsGeometry.fromPolylineXY(temp_points), None)

    def activate(self):
         QgsMapTool.activate(self)
         self.canvas.setCursor(self.cursor)

    def isZoomTool(self):
        return False

    def setCursor(self,cursor):
        self.cursor = QCursor(cursor)
        
