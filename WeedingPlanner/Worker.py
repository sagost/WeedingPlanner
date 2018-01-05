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



from qgis.core import *
from PyQt4 import QtCore, QtGui
import traceback
from osgeo import gdal,ogr
import numpy as np
import math


            
class Worker(QtCore.QObject):
    '''Example worker for calculating the total area of all features in a layer'''
    def __init__(self, iface, rds, ExtentRettangoloRosso,StripeInterval,StripeWidth,WeedingInterval,MinimumWeedingStripeArea,Point1,Areacosa, Areacosb,cosa, cosb, Band, ValueToCompare,Rule,MinimumDistance):
        QtCore.QObject.__init__(self)
       
        #self.geomList = geomList
        mapRenderer = iface.mapCanvas().mapRenderer()
        self.crsDest = int(mapRenderer.destinationCrs().authid()[5:])
        self.rds = rds
        self.ExtentRettangoloRosso = ExtentRettangoloRosso
        self.StripeInterval = StripeInterval
        self.StripeWidth = StripeWidth
        self.WeedingInterval = WeedingInterval
        self.MinimumWeedingStripeArea = MinimumWeedingStripeArea
        self.Point1 = Point1
        self.Areacosa = Areacosa
        self.Areacosb = Areacosb
        self.cosa = cosa
        self.cosb = cosb
        self.Band = Band
        self.ValueToCompare = ValueToCompare
        self.Rule = Rule
        self.killed = False
        self.MinimumDistance = MinimumDistance
        #self.WeedingList = []
        
    def run(self,nodata_value = 0,global_src_extent=False):
        
        #featListOut = []

        try:
            # calculate the total area of all of the features in a layer


            WeedingPlanLayer = QgsVectorLayer("Polygon?crs=epsg:"+str(self.crsDest)+"&index=yes",  "WeedingPlan", "memory")
            WeedingPlanLayerProvider = WeedingPlanLayer.dataProvider()
            

            rb = self.rds.GetRasterBand(self.Band)              
            rgt = self.rds.GetGeoTransform()
            if nodata_value:
                nodata_value = float(nodata_value)
                rb.SetNoDataValue(nodata_value)
            
            if global_src_extent:
    
                src_offset = self.bbox_to_pixel_offsets(rgt, self.ExtentRettangoloRosso)
                src_array = rb.ReadAsArray(*src_offset)
        
                new_gt = (
                    (rgt[0] + (src_offset[0] * rgt[1])),
                    rgt[1],
                    0.0,
                    (rgt[3] + (src_offset[1] * rgt[5])),
                    0.0,
                    rgt[5]
                )
            
            mem_drv = ogr.GetDriverByName('Memory')
            driver = gdal.GetDriverByName('MEM')
           
            N = 1       
            
            #self.lastweedgeom = []              # le singole geometrie da trattare
            
            
            while N <= self.StripeInterval:
                if N == 1:
                    StripePoint1 = self.Point1
                else:
                    StripePoint1 = QgsPoint(self.Point1.x()+((self.StripeWidth*(N-1))*self.cosa), self.Point1.y()+((self.StripeWidth*(N-1))*self.cosb))
        
                StripePoint4 = QgsPoint(self.Point1.x()+((self.StripeWidth*(N))*self.cosa), self.Point1.y()+((self.StripeWidth*(N))*self.cosb))
                
                Counter = 1
                lastweedgeom = None
                ToNotWeedGeom = []
                while Counter <= self.WeedingInterval:
                    if self.killed is True:
                        break
                    if Counter ==1:
                        WeedAreaPoint1 = StripePoint1
                        WeedAreaPoint2 = StripePoint4
                    else:
                        WeedAreaPoint1 = QgsPoint(StripePoint1.x()+((self.MinimumWeedingStripeArea*(Counter-1))*self.Areacosa), StripePoint1.y()+((self.MinimumWeedingStripeArea*(Counter-1))*self.Areacosb))
                        WeedAreaPoint2 = QgsPoint(StripePoint4.x()+((self.MinimumWeedingStripeArea*(Counter-1))*self.Areacosa), StripePoint4.y()+((self.MinimumWeedingStripeArea*(Counter-1))*self.Areacosb))
                    
                    WeedAreaPoint3 = QgsPoint(StripePoint4.x()+((self.MinimumWeedingStripeArea*(Counter))*self.Areacosa), StripePoint4.y()+((self.MinimumWeedingStripeArea*(Counter))*self.Areacosb))
                    WeedAreaPoint4 = QgsPoint(StripePoint1.x()+((self.MinimumWeedingStripeArea*(Counter))*self.Areacosa), StripePoint1.y()+((self.MinimumWeedingStripeArea*(Counter))*self.Areacosb))
                    
                    ring = ogr.Geometry(ogr.wkbLinearRing)
                    ring.AddPoint(WeedAreaPoint1.x(),WeedAreaPoint1.y())                              
                    ring.AddPoint(WeedAreaPoint2.x(),WeedAreaPoint2.y())
                    ring.AddPoint(WeedAreaPoint3.x(),WeedAreaPoint3.y())
                    ring.AddPoint(WeedAreaPoint4.x(),WeedAreaPoint4.y())
                    geom = ogr.Geometry(ogr.wkbPolygon)                          #và trasformato nello stesso sistema del raster
                    geom.AddGeometry(ring)
                    try:
                        if not global_src_extent:
                            src_offset = self.bbox_to_pixel_offsets(rgt, geom.GetEnvelope())
                            src_array = rb.ReadAsArray(*src_offset)
                
                            new_gt = (
                                (rgt[0] + (src_offset[0] * rgt[1])),
                                rgt[1],
                                0.0,
                                (rgt[3] + (src_offset[1] * rgt[5])),
                                0.0,
                                rgt[5]
                            )
                            
                        mem_ds = mem_drv.CreateDataSource('out')
                        mem_layer = mem_ds.CreateLayer('poly', None, ogr.wkbPolygon)   #le geometrie devono essere dei ogr.wkbPolygon
                        feature = ogr.Feature(mem_layer.GetLayerDefn())
                        feature.SetGeometry(geom)
                        mem_layer.CreateFeature(feature)       #implementare una feature con la singola geometria 
                        
                        rvds = driver.Create('', src_offset[2], src_offset[3], 1, gdal.GDT_Byte)
                        rvds.SetGeoTransform(new_gt)
                        gdal.RasterizeLayer(rvds, [1], mem_layer, None, None, [1], ['ALL_TOUCHED=TRUE'])
                        rv_array = rvds.ReadAsArray()  
                        
                        masked = np.ma.MaskedArray(
                            src_array,
                            mask=np.logical_or(
                                src_array == nodata_value,
                                np.logical_not(rv_array)
                            )
                        )
                        
                        feature_stats = {'max': float(masked.max())}
                        
                        if self.Rule == '>=':
                            if feature_stats.get('max') >= self.ValueToCompare:
                                wkt = geom.ExportToWkt()
                        
                                wkt = str(wkt).split(' ')
                                Point1 = QgsPoint(float(wkt[1][2:-2]),float(wkt[2][:-2]))
                                Point2 = QgsPoint(float(wkt[3][2:-2]),float(wkt[4][:-2]))
                                Point3 = QgsPoint(float(wkt[5][2:-2]),float(wkt[6][:-2]))
                                Point4 = QgsPoint(float(wkt[7][2:-2]),float(wkt[8][:-2]))
                                geometry = QgsGeometry()
                                geometry = geometry.fromPolygon([[Point1, Point2, Point3, Point4]])
                                feature2 = QgsFeature()
                                feature2.setGeometry(geometry)
                                WeedingPlanLayerProvider.addFeatures([feature2])
                                #self.WeedingList.append(feature2)

                                    
                                if lastweedgeom is not None:
                                    Point1 = lastweedgeom.centroid().asPoint()
                                    Point2 = geometry.centroid().asPoint()
                                    if self.DistanceBetweenPoint(Point1,Point2) < self.MinimumDistance:
                                        for geom in ToNotWeedGeom:
                                            feature2 = QgsFeature()
                                            feature2.setGeometry(geom)
                                            WeedingPlanLayerProvider.addFeatures([feature2])
                                            #self.WeedingList.append(feature2)
                                ToNotWeedGeom = []
                                                         
                                lastweedgeom = geometry        
                                        
                            else:
                                wkt = geom.ExportToWkt()
                        
                                wkt = str(wkt).split(' ')
                                Point1 = QgsPoint(float(wkt[1][2:-2]),float(wkt[2][:-2]))
                                Point2 = QgsPoint(float(wkt[3][2:-2]),float(wkt[4][:-2]))
                                Point3 = QgsPoint(float(wkt[5][2:-2]),float(wkt[6][:-2]))
                                Point4 = QgsPoint(float(wkt[7][2:-2]),float(wkt[8][:-2]))
                                geometry = QgsGeometry()
                                geometry = geometry.fromPolygon([[Point1, Point2, Point3, Point4]])
                                ToNotWeedGeom.append(geometry)
                                
                            
                            rvds = None
                            mem_ds = None
                            
                        elif self.Rule == '<=':
                            if feature_stats.get('max') <= self.ValueToCompare:
                                wkt = geom.ExportToWkt()
                        
                                wkt = str(wkt).split(' ')
                                Point1 = QgsPoint(float(wkt[1][2:-2]),float(wkt[2][:-2]))
                                Point2 = QgsPoint(float(wkt[3][2:-2]),float(wkt[4][:-2]))
                                Point3 = QgsPoint(float(wkt[5][2:-2]),float(wkt[6][:-2]))
                                Point4 = QgsPoint(float(wkt[7][2:-2]),float(wkt[8][:-2]))
                                geometry = QgsGeometry()
                                geometry = geometry.fromPolygon([[Point1, Point2, Point3, Point4]])
                                feature2 = QgsFeature()
                                feature2.setGeometry(geometry)
                                WeedingPlanLayerProvider.addFeatures([feature2])
                                    
                                if lastweedgeom is not None:
                                    Point1 = lastweedgeom.centroid().asPoint()
                                    Point2 = geometry.centroid().asPoint()
                                    if self.DistanceBetweenPoint(Point1,Point2) < self.MinimumDistance:
                                        for geom in ToNotWeedGeom:
                                             
                                            feature2 = QgsFeature()
                                            feature2.setGeometry(geom)
                                            WeedingPlanLayerProvider.addFeatures([feature2])
                                ToNotWeedGeom = []
                                                         
                                lastweedgeom = geometry        
                                        
                            else:
                                wkt = geom.ExportToWkt()
                        
                                wkt = str(wkt).split(' ')
                                Point1 = QgsPoint(float(wkt[1][2:-2]),float(wkt[2][:-2]))
                                Point2 = QgsPoint(float(wkt[3][2:-2]),float(wkt[4][:-2]))
                                Point3 = QgsPoint(float(wkt[5][2:-2]),float(wkt[6][:-2]))
                                Point4 = QgsPoint(float(wkt[7][2:-2]),float(wkt[8][:-2]))
                                geometry = QgsGeometry()
                                geometry = geometry.fromPolygon([[Point1, Point2, Point3, Point4]])
                                ToNotWeedGeom.append(geometry)
                                
                            
                            rvds = None
                            mem_ds = None
                            
                        elif self.Rule == '=':
                            if feature_stats.get('max') == self.ValueToCompare:
                                wkt = geom.ExportToWkt()
                        
                                wkt = str(wkt).split(' ')
                                Point1 = QgsPoint(float(wkt[1][2:-2]),float(wkt[2][:-2]))
                                Point2 = QgsPoint(float(wkt[3][2:-2]),float(wkt[4][:-2]))
                                Point3 = QgsPoint(float(wkt[5][2:-2]),float(wkt[6][:-2]))
                                Point4 = QgsPoint(float(wkt[7][2:-2]),float(wkt[8][:-2]))
                                geometry = QgsGeometry()
                                geometry = geometry.fromPolygon([[Point1, Point2, Point3, Point4]])
                                feature2 = QgsFeature()
                                feature2.setGeometry(geometry)
                                WeedingPlanLayerProvider.addFeatures([feature2])
                                    
                                if lastweedgeom is not None:
                                    Point1 = lastweedgeom.centroid().asPoint()
                                    Point2 = geometry.centroid().asPoint()
                                    if self.DistanceBetweenPoint(Point1,Point2) < self.MinimumDistance:
                                        for geom in ToNotWeedGeom:
                                             
                                            feature2 = QgsFeature()
                                            feature2.setGeometry(geom)
                                            WeedingPlanLayerProvider.addFeatures([feature2])
                                ToNotWeedGeom = []
                                                         
                                lastweedgeom = geometry        
                                        
                            else:
                                wkt = geom.ExportToWkt()
                        
                                wkt = str(wkt).split(' ')
                                Point1 = QgsPoint(float(wkt[1][2:-2]),float(wkt[2][:-2]))
                                #print Point1.x() , '    ' , Point1.y()
                                Point2 = QgsPoint(float(wkt[3][2:-2]),float(wkt[4][:-2]))
                                Point3 = QgsPoint(float(wkt[5][2:-2]),float(wkt[6][:-2]))
                                Point4 = QgsPoint(float(wkt[7][2:-2]),float(wkt[8][:-2]))
                                geometry = QgsGeometry()
                                geometry = geometry.fromPolygon([[Point1, Point2, Point3, Point4]])
                                ToNotWeedGeom.append(geometry)
                                
                            
                            rvds = None
                            mem_ds = None
                        
                        elif self.Rule == '>':
                            if feature_stats.get('max') > self.ValueToCompare:
                                wkt = geom.ExportToWkt()
                        
                                wkt = str(wkt).split(' ')
                                Point1 = QgsPoint(float(wkt[1][2:-2]),float(wkt[2][:-2]))
                                #print Point1.x() , '    ' , Point1.y()
                                Point2 = QgsPoint(float(wkt[3][2:-2]),float(wkt[4][:-2]))
                                Point3 = QgsPoint(float(wkt[5][2:-2]),float(wkt[6][:-2]))
                                Point4 = QgsPoint(float(wkt[7][2:-2]),float(wkt[8][:-2]))
                                geometry = QgsGeometry()
                                geometry = geometry.fromPolygon([[Point1, Point2, Point3, Point4]])
                                feature2 = QgsFeature()
                                feature2.setGeometry(geometry)
                                #featListOut.append(feature2)
                                #WeedingPlanLayer.addFeature(feature2,True)
                                WeedingPlanLayerProvider.addFeatures([feature2])
                                
                                
                                    
                                if lastweedgeom is not None:
                                    Point1 = lastweedgeom.centroid().asPoint()
                                    Point2 = geometry.centroid().asPoint()
                                    if self.DistanceBetweenPoint(Point1,Point2) < self.MinimumDistance:
                                        for geom in ToNotWeedGeom:
                                             
                                            feature2 = QgsFeature()
                                            feature2.setGeometry(geom)
                                            WeedingPlanLayerProvider.addFeatures([feature2])
                                ToNotWeedGeom = []
                                                         
                                lastweedgeom = geometry        
                                        
                            else:
                                wkt = geom.ExportToWkt()
                        
                                wkt = str(wkt).split(' ')
                                Point1 = QgsPoint(float(wkt[1][2:-2]),float(wkt[2][:-2]))
                                Point2 = QgsPoint(float(wkt[3][2:-2]),float(wkt[4][:-2]))
                                Point3 = QgsPoint(float(wkt[5][2:-2]),float(wkt[6][:-2]))
                                Point4 = QgsPoint(float(wkt[7][2:-2]),float(wkt[8][:-2]))
                                geometry = QgsGeometry()
                                geometry = geometry.fromPolygon([[Point1, Point2, Point3, Point4]])
                                ToNotWeedGeom.append(geometry)
                                
                            
                            rvds = None
                            mem_ds = None
                            
                        elif self.Rule == '<':
                            if feature_stats.get('max') < self.ValueToCompare:
                                wkt = geom.ExportToWkt()
                        
                                wkt = str(wkt).split(' ')
                                Point1 = QgsPoint(float(wkt[1][2:-2]),float(wkt[2][:-2]))
                                #print Point1.x() , '    ' , Point1.y()
                                Point2 = QgsPoint(float(wkt[3][2:-2]),float(wkt[4][:-2]))
                                Point3 = QgsPoint(float(wkt[5][2:-2]),float(wkt[6][:-2]))
                                Point4 = QgsPoint(float(wkt[7][2:-2]),float(wkt[8][:-2]))
                                geometry = QgsGeometry()
                                geometry = geometry.fromPolygon([[Point1, Point2, Point3, Point4]])
                                feature2 = QgsFeature()
                                feature2.setGeometry(geometry)
        
                                WeedingPlanLayerProvider.addFeatures([feature2])
                                    
                                if lastweedgeom is not None:
                                    Point1 = lastweedgeom.centroid().asPoint()
                                    Point2 = geometry.centroid().asPoint()
                                    if self.DistanceBetweenPoint(Point1,Point2) < self.MinimumDistance:
                                        for geom in ToNotWeedGeom:
                                             
                                            feature2 = QgsFeature()
                                            feature2.setGeometry(geom)
                                            WeedingPlanLayerProvider.addFeatures([feature2])
                                ToNotWeedGeom = []
                                                         
                                lastweedgeom = geometry        
                                        
                            else:
                                wkt = geom.ExportToWkt()
                        
                                wkt = str(wkt).split(' ')
                                Point1 = QgsPoint(float(wkt[1][2:-2]),float(wkt[2][:-2]))
                                Point2 = QgsPoint(float(wkt[3][2:-2]),float(wkt[4][:-2]))
                                Point3 = QgsPoint(float(wkt[5][2:-2]),float(wkt[6][:-2]))
                                Point4 = QgsPoint(float(wkt[7][2:-2]),float(wkt[8][:-2]))
                                geometry = QgsGeometry()
                                geometry = geometry.fromPolygon([[Point1, Point2, Point3, Point4]])
                                ToNotWeedGeom.append(geometry)
                                
                            
                            rvds = None
                            mem_ds = None                            
                            
                
                    except:
                        pass
                    
                    Counter = Counter +1
                
                N = N+1
                
            #WeedingPlanLayer.commitChanges()
            
            if self.killed is False:
                #self.progress.emit(100)
                WeedingPlanLayer.updateExtents()
                #WeedingPlanLayer.commitChanges()
                #ret = (featListOut)
        except Exception, e:
            # forward the exception upstream
            self.error.emit(e, traceback.format_exc())
        
        self.finished.emit(WeedingPlanLayer)
        del WeedingPlanLayer
    
    
    
    def DistanceBetweenPoint(self,Point1,Point2):
        return math.sqrt(Point1.sqrDist(Point2)) 
    
    def bbox_to_pixel_offsets(self,gt, bbox):
        originX = gt[0]
        originY = gt[3]
        pixel_width = gt[1]
        pixel_height = gt[5]
        x1 = int((bbox[0] - originX) / pixel_width)
        x2 = int((bbox[1] - originX) / pixel_width) + 1
        y1 = int((bbox[3] - originY) / pixel_height)
        y2 = int((bbox[2] - originY) / pixel_height) + 1
        xsize = x2 - x1
        ysize = y2 - y1
        return (x1, y1, xsize, ysize)
        
    def kill(self):
        self.killed = True
    finished = QtCore.pyqtSignal(object)
    error = QtCore.pyqtSignal(Exception, basestring)

