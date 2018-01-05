# -*- coding: utf-8 -*-

"""
/***************************************************************************
 WeedingPlanner
                                 A QGIS plugin
 Create weeding plan from NDVI image
                             -------------------
        begin                : 2016-03-22
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Salvatore Agosta / SAL Engineering s.r.l.
        email                : sagosta@salengineering.it
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
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math


class ReplayMapTool(QgsMapToolPan):
    def __init__(self, canvas,controller):               #WeedingPlannerDockWidget):
        QgsMapToolPan.__init__(self,canvas)
        self.PointArea1 = None
        self.PointArea2 = None
        self.RubberBand = False
        self.RubberBand2 = False
        self.Azimuth = None
        self.controller = controller
        
        
    def canvasPressEvent(self, mouseEvent):
        
        if mouseEvent.button()==Qt.RightButton:
            if self.PointArea1 == None:
                self.r = QgsRubberBand(self.canvas(), True)
                
                self.r2 = QgsRubberBand(self.canvas(), True)
                
                Point = QPoint( mouseEvent.pos().x(), mouseEvent.pos().y())
                MapPt = self.canvas().getCoordinateTransform().toMapCoordinates(Point)
                self.PointArea1 = MapPt
                
            else:
                if self.PointArea2 == None:
                    Point = QPoint( mouseEvent.pos().x(), mouseEvent.pos().y())
                    MapPt = self.canvas().getCoordinateTransform().toMapCoordinates(Point)
                    self.PointArea2 = MapPt
                    self.Azimuth = self.PointArea1.azimuth(self.PointArea2)
                    if self.Azimuth < 0:
                        self.Azimuth += 360
                    
                    
                elif self.PointArea2 != None:                   #else va bene uguale
                    
                    Point = QPoint( mouseEvent.pos().x(), mouseEvent.pos().y())
                    MapPt = self.canvas().getCoordinateTransform().toMapCoordinates(Point)
                    LatoAB = self.DistanceBetweenPoint(self.PointArea1, self.PointArea2)
                    LatoAC = self.DistanceBetweenPoint(self.PointArea1, MapPt)
                    LatoBC = self.DistanceBetweenPoint(self.PointArea2, MapPt)
                    
                    try:
                        Alfa = math.degrees(math.acos((LatoAC**2+LatoAB**2-LatoBC**2)/(-2.0 *LatoAB*LatoAC)))
                        Beta = math.degrees(math.acos((LatoAB**2+LatoBC**2-LatoAC**2)/(-2.0 *LatoBC*LatoAB)))
                    except:
                        return
                    
                    if Alfa > 90 or Beta > 90:
                        if Alfa > 90:
                            Alfa1 = math.radians(180 - Alfa)
                            Distanza = LatoAC* math.sin(Alfa1)
                            
                        else:
                            Beta1 = math.radians(180-Beta)
                            Distanza = LatoBC* math.sin(Beta1)
                            
                    elif Alfa < 90 and Beta < 90:
                        SemiP = (LatoAB + LatoAC +LatoBC)/2.0
                        Area = math.sqrt(SemiP*(SemiP-LatoAC)*(SemiP-LatoBC)*(SemiP-LatoAB))
                        Distanza = 2*Area/LatoAB
                        
                    elif Alfa == 90 or Beta == 90:
                        if Alfa == 90:
                            Distanza == LatoAC
                        else:
                            Distanza == LatoBC
                    
                    Lato = (self.PointArea2.x() - self.PointArea1.x()) * float(MapPt.y() - self.PointArea1.y()) - (self.PointArea2.y() - self.PointArea1.y()) * float(MapPt.x() - self.PointArea1.x())
                    if Lato >= 0:
                        OrthogonalAzimuth = self.Azimuth - 90
                    else:
                        OrthogonalAzimuth = self.Azimuth + 90
                        
                    if OrthogonalAzimuth > 360:
                        OrthogonalAzimuth =  OrthogonalAzimuth - 360
                    elif OrthogonalAzimuth < 0:
                        OrthogonalAzimuth =  OrthogonalAzimuth + 360
                                  
                    cosa, cosb = self.cosdir_azim(OrthogonalAzimuth)  
                    end_point3 = QgsPoint(self.PointArea2.x()+(Distanza*cosa), self.PointArea2.y()+(Distanza*cosb))  
                    end_point4 = QgsPoint(self.PointArea1.x()+(Distanza*cosa), self.PointArea1.y()+(Distanza*cosb))
                    
                    points = [[self.PointArea1, self.PointArea2, end_point3, end_point4]]
                    self.r.setToGeometry(QgsGeometry.fromPolygon(points), None)
                    
                    self.r.setColor(QColor(255,0,0,50))     #100 is Alpha channel??    
                    
                    self.RubberBand = True
                    
                    VerticalAzimuth = self.Azimuth
                    self.PointArea1 = None
                    self.PointArea2 = None
                    self.RubberBand = False
                    self.Azimuth = None
                    self.controller.NDVICalculation(points,OrthogonalAzimuth,VerticalAzimuth)
                    
                
        elif mouseEvent.button()==Qt.LeftButton:
            QgsMapToolPan.canvasPressEvent(self, mouseEvent)
            
    def DistanceBetweenPoint(self,Point1,Point2):
        return math.sqrt(Point1.sqrDist(Point2))  
           
    def cosdir_azim(self,azim):
        az = math.radians(azim)
        cosa = math.sin(az)
        cosb = math.cos(az)
        return cosa,cosb  
    
    def canvasReleaseEvent(self, mouseEvent):    
        QgsMapToolPan.canvasReleaseEvent(self, mouseEvent)
         
    def canvasMoveEvent(self, mouseEvent):
        if mouseEvent.buttons()&Qt.LeftButton:
            QgsMapToolPan.canvasMoveEvent(self, mouseEvent)
            
        else:
            if self.PointArea2 != None:
                
                ThirdPtAzimuth = None
                OrthogonalAzimuth = None
                
                
                if self.RubberBand == True:
                    self.r.reset(True)    
                    self.RubberBand = False
                                
                Point = QPoint( mouseEvent.pos().x(), mouseEvent.pos().y())
                MapPt = self.canvas().getCoordinateTransform().toMapCoordinates(Point)
                
                LatoAB = self.DistanceBetweenPoint(self.PointArea1, self.PointArea2)
                LatoAC = self.DistanceBetweenPoint(self.PointArea1, MapPt)
                LatoBC = self.DistanceBetweenPoint(self.PointArea2, MapPt)
                
                try:
                    Alfa = math.degrees(math.acos((LatoAC**2+LatoAB**2-LatoBC**2)/(-2.0 *LatoAB*LatoAC)))
                    Beta = math.degrees(math.acos((LatoAB**2+LatoBC**2-LatoAC**2)/(-2.0 *LatoBC*LatoAB)))
                except:
                        return
                    
                if Alfa > 90 or Beta > 90:
                    if Alfa > 90:
                        Alfa1 = math.radians(180 - Alfa)
                        Distanza = LatoAC* math.sin(Alfa1)
                        
                    else:
                        Beta1 = math.radians(180-Beta)
                        Distanza = LatoBC* math.sin(Beta1)
                        
                elif Alfa < 90 and Beta < 90:
                    SemiP = (LatoAB + LatoAC +LatoBC)/2.0
                    Area = math.sqrt(SemiP*(SemiP-LatoAC)*(SemiP-LatoBC)*(SemiP-LatoAB))
                    Distanza = 2*Area/LatoAB
                    
                elif Alfa == 90 or Beta == 90:
                    if Alfa == 90:
                        Distanza == LatoAC
                    else:
                        Distanza == LatoBC
                
                
                Lato = (self.PointArea2.x() - self.PointArea1.x()) * float(MapPt.y() - self.PointArea1.y()) - (self.PointArea2.y() - self.PointArea1.y()) * float(MapPt.x() - self.PointArea1.x())
                if Lato >= 0:
                    OrthogonalAzimuth = self.Azimuth - 90
                else:
                    OrthogonalAzimuth = self.Azimuth + 90
                    
                if OrthogonalAzimuth > 360:
                  OrthogonalAzimuth =  OrthogonalAzimuth - 360
                elif OrthogonalAzimuth < 0:
                    OrthogonalAzimuth =  OrthogonalAzimuth + 360
                             
                cosa, cosb = self.cosdir_azim(OrthogonalAzimuth)  
                end_point4 = QgsPoint(self.PointArea1.x()+(Distanza*cosa), self.PointArea1.y()+(Distanza*cosb))  
                end_point3 = QgsPoint(self.PointArea2.x()+(Distanza*cosa), self.PointArea2.y()+(Distanza*cosb))
                
                points = [[self.PointArea1, self.PointArea2, end_point3, end_point4]]
                self.r.setToGeometry(QgsGeometry.fromPolygon(points), None)
                self.r.setColor(QColor(255,0,0,50))     #50 is Alpha channel   
                
                self.RubberBand = True
                
                return
            
            
            elif self.PointArea1 != None:
                
            
                if self.RubberBand2 == True:
                    self.r2.reset(True)
                    self.RubberBand2 = False
                    
                Point = QPoint( mouseEvent.pos().x(), mouseEvent.pos().y())
                MapPt = self.canvas().getCoordinateTransform().toMapCoordinates(Point)
                    
                gLine = QgsGeometry.fromPolyline([self.PointArea1, MapPt ])
                self.r2.setToGeometry(gLine,None)
                self.r2.setColor(QColor(255,0,0))     #50 is Alpha channel
                self.r2.setWidth(3) 
                self.RubberBand2 = True
                return
                    
                
                
        