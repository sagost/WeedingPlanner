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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox,QWidget
from PyQt4.QtCore import pyqtSignal
from qgis.core import *
from ReplayMapTool import *
from Worker import Worker
from osgeo import gdal, ogr
from osgeo.gdalconst import *
import numpy as np
import sys
import processing
from weeding_parameter import Ui_WeedingParameter

gdal.PushErrorHandler('CPLQuietErrorHandler')

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'weeding_planner_dockwidget_base.ui'))


class WeedingPlannerDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface,parent=None):
        """Constructor."""
        super(WeedingPlannerDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        
        self.mapTool=ReplayMapTool(self.iface.mapCanvas(),self)
        
        self.LoadtoolButton.clicked.connect(self.LoadLayer)
        self.NewAreapushButton.clicked.connect(self.NewArea)
        self.ParameterpushButton.clicked.connect(self.SetParameter)
        self.DissolvepushButton.clicked.connect(self.Dissolve)
        self.FillHolespushButton.clicked.connect(self.FillHoles)
        
        self.Band = 1
        self.Rule = '>='
        self.ValueToCompare = 0.35
        self.VerticalPolicy = 0.3
        self.HorizontalPolicy = 0.5
        self.MinimumDistance = 2.0
        
        
        
        
        
        
    def closeEvent(self, event):
        if self.mapTool.RubberBand == True:
            self.iface.mapCanvas().scene().removeItem(self.mapTool.r)
        self.Band = 1
        self.Rule = '>='
        self.ValueToCompare = 0.35
        self.VerticalPolicy = 0.3
        self.HorizontalPolicy = 0.5   
        self.closingPlugin.emit()
        event.accept()
        
    def LoadLayer(self):
        self.NDVIcomboBox.clear()
        self.FieldcomboBox.clear()
        LayerRegistryItem = QgsMapLayerRegistry.instance().mapLayers()
        for id, layer in LayerRegistryItem.iteritems():
            if layer.type() == QgsMapLayer.RasterLayer:
                self.NDVIcomboBox.addItem(layer.name(), id)
            elif layer.type() == QgsMapLayer.VectorLayer:
                if layer.geometryType() == 2:
                    self.FieldcomboBox.addItem(layer.name(), id)
                
            
            if self.NDVIcomboBox.count() > 0 and self.FieldcomboBox.count()>0:
                self.ParameterpushButton.setEnabled(True)
                
                
                
    def NewArea(self):
               
        self.PointArea1 = None
        self.PointArea2 = None
        self.RubberBand = False
        canvas = self.iface.mapCanvas()
        mapRenderer = canvas.mapRenderer()
        ProjectCrs= mapRenderer.destinationCrs()
        CrsDescription =  ProjectCrs.description().split(' ')
        
        UtmSystem = 0
        for x in CrsDescription:
            if x != 'UTM':
                UtmSystem = 0
                
            else:
                UtmSystem = 1
                break
            
        if UtmSystem == 0:
            w = QWidget()
            QMessageBox.warning(w, "Message", "Please set an UTM projection before continue!")
            
        else:
            if self.iface.mapCanvas().mapTool()!=self.mapTool:
                QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
                self.mapTool_previous=self.iface.mapCanvas().mapTool()
                self.iface.mapCanvas().setMapTool(self.mapTool)
            
    def SetParameter(self):
        QApplication.restoreOverrideCursor()
        NDVILayerName = self.NDVIcomboBox.itemData(self.NDVIcomboBox.currentIndex())
        NDVILayer = QgsMapLayerRegistry.instance().mapLayer(NDVILayerName)
        BandNumber = NDVILayer.bandCount()
        NDVILayer = None
        self.SpecDialog = WeedingParameter(BandNumber,self.ValueToCompare, self.VerticalPolicy,self.HorizontalPolicy,self.Rule, self.Band,self.MinimumDistance)
        self.SpecDialog.exec_()
        
        self.Band = self.SpecDialog.Band
        self.Rule = self.SpecDialog.Rule
        self.ValueToCompare = self.SpecDialog.ValueToCompare
        
        
        self.VerticalPolicy = self.SpecDialog.VerticalPolicy
        self.HorizontalPolicy = self.SpecDialog.HorizontalPolicy
        
        self.MinimumDistance = self.SpecDialog.MinimumDistance
        
        self.NewAreapushButton.setEnabled(True)
        
               
            
    def NDVICalculation(self, FieldRubberBand, OrthogonalAzimuth,VerticalAzimuth):
        
        QApplication.restoreOverrideCursor()
        NDVILayerName = self.NDVIcomboBox.itemData(self.NDVIcomboBox.currentIndex())
        NDVILayer = QgsMapLayerRegistry.instance().mapLayer(NDVILayerName)
        NDVILayerSource = NDVILayer.source()

        
        self.mapTool.r.reset(True)    
        self.mapTool.RubberBand = False
        del self.mapTool.r
        
        self.mapTool.r2.reset(True)
        self.mapTool.RubberBand2 = False
        del self.mapTool.r2
        
        
        self.iface.mapCanvas().unsetMapTool(self.mapTool)
        Point1 = QgsPoint(FieldRubberBand[0][0])
        Point2 = QgsPoint(FieldRubberBand[0][1])
        Point3 = QgsPoint(FieldRubberBand[0][2])
        Point4 = QgsPoint(FieldRubberBand[0][3])
        
        
        Distance_1_4 = self.mapTool.DistanceBetweenPoint(Point1, Point4)
        Distance_1_2 = self.mapTool.DistanceBetweenPoint(Point1, Point2)
        
        AngoloVerticale = Point1.azimuth(Point2)
        AngoloOrizzontale = Point1.azimuth(Point4)
        
        cosa, cosb = self.mapTool.cosdir_azim(AngoloVerticale)
        cosc, cosd = self.mapTool.cosdir_azim(AngoloOrizzontale)
        
        
        Rettangolo1Point1 = Point1
        Rettangolo1Point2 = QgsPoint(Point1.x()+((Distance_1_2/4.0)*cosa), Point1.y()+((Distance_1_2/4.0)*cosb))
        Rettangolo1Point3 = QgsPoint(Point4.x()+((Distance_1_2/4.0)*cosa), Point4.y()+((Distance_1_2/4.0)*cosb))
        Rettangolo1Point4 = Point4
        Rettangolo1 = [[Rettangolo1Point1,Rettangolo1Point2,Rettangolo1Point3,Rettangolo1Point4]]
        
        Rettangolo2Point1 = Rettangolo1Point2
        Rettangolo2Point2 = QgsPoint(Rettangolo2Point1.x()+((Distance_1_2/4.0)*cosa), Rettangolo2Point1.y()+((Distance_1_2/4.0)*cosb))
        Rettangolo2Point3 = QgsPoint(Rettangolo1Point3.x()+((Distance_1_2/4.0)*cosa), Rettangolo1Point3.y()+((Distance_1_2/4.0)*cosb))
        Rettangolo2Point4 = Rettangolo1Point3
        Rettangolo2 = [[Rettangolo2Point1,Rettangolo2Point2,Rettangolo2Point3,Rettangolo2Point4]]
        
        Rettangolo3Point1 = Rettangolo2Point2
        Rettangolo3Point2 = QgsPoint(Rettangolo3Point1.x()+((Distance_1_2/4.0)*cosa), Rettangolo3Point1.y()+((Distance_1_2/4.0)*cosb))
        Rettangolo3Point3 = QgsPoint(Rettangolo2Point3.x()+((Distance_1_2/4.0)*cosa), Rettangolo2Point3.y()+((Distance_1_2/4.0)*cosb))
        Rettangolo3Point4 = Rettangolo2Point3
        Rettangolo3 = [[Rettangolo3Point1,Rettangolo3Point2,Rettangolo3Point3,Rettangolo3Point4]]
        
        Rettangolo4Point1 = Rettangolo3Point2
        Rettangolo4Point2 = Point2
        Rettangolo4Point3 = Point3
        Rettangolo4Point4 = Rettangolo3Point3
        Rettangolo4 = [[Rettangolo4Point1,Rettangolo4Point2,Rettangolo4Point3,Rettangolo4Point4]]
        
        ListaRettangoli = [Rettangolo1,Rettangolo2,Rettangolo3,Rettangolo4]
        
        ListaExtent = []
        for Rettangolo in ListaRettangoli:
            
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(Rettangolo[0][0].x(),Rettangolo[0][0].y())                              
            ring.AddPoint(Rettangolo[0][1].x(),Rettangolo[0][1].y())
            ring.AddPoint(Rettangolo[0][2].x(),Rettangolo[0][2].y())
            ring.AddPoint(Rettangolo[0][3].x(),Rettangolo[0][3].y())
            geom2 = ogr.Geometry(ogr.wkbPolygon)
            geom2.AddGeometry(ring)
            
            mem_drv = ogr.GetDriverByName('Memory')
            mem_ds = mem_drv.CreateDataSource('out')
            mem_layer = mem_ds.CreateLayer('poly', None, ogr.wkbPolygon)   #le geometrie devono essere dei ogr.wkbPolygon
            feature = ogr.Feature(mem_layer.GetLayerDefn())
            feature.SetGeometry(geom2)
            mem_layer.CreateFeature(feature)
            ListaExtent.append(mem_layer.GetExtent())
            mem_ds = None
            mem_layer = None
        
        
        MinimumWeedingStripeArea = self.VerticalPolicy        #in meters          #0.5 is the stripe width  could be set in the parameters settings
        
        WeedingStripeAreaDistance = int(math.ceil( (Distance_1_2/4.0)/ MinimumWeedingStripeArea)) * MinimumWeedingStripeArea
        WeedingInterval = WeedingStripeAreaDistance / MinimumWeedingStripeArea

        Areacosa, Areacosb = self.mapTool.cosdir_azim(VerticalAzimuth)
        
        StripeWidth = self.HorizontalPolicy   #in meters          #0.5 is the stripe width  could be set in the parameters settings
       
        AreaWidth = int(math.ceil( (Distance_1_4)/ StripeWidth)) * StripeWidth

        StripeInterval = AreaWidth / StripeWidth     

        cosa, cosb = self.mapTool.cosdir_azim(OrthogonalAzimuth)
        
        rds = gdal.Open(NDVILayerSource, GA_ReadOnly)  
        
        mapRenderer = self.iface.mapCanvas().mapRenderer()
        crsDest = int(mapRenderer.destinationCrs().authid()[5:])
        self.WeedingPlanLayer = QgsVectorLayer("Polygon?crs=epsg:"+str(crsDest)+"&index=yes",  "WeedingPlan", "memory")
        self.WeedingPlanLayerProvider = self.WeedingPlanLayer.dataProvider()
         
        self.WaitWorker = 0
            
        self.startWorker(rds, ListaExtent[0],StripeInterval,StripeWidth,WeedingInterval,MinimumWeedingStripeArea,Rettangolo1Point1,Areacosa, Areacosb,cosa, cosb)
        self.startWorker(rds, ListaExtent[1],StripeInterval,StripeWidth,WeedingInterval,MinimumWeedingStripeArea,Rettangolo2Point1,Areacosa, Areacosb,cosa, cosb)
        self.startWorker(rds, ListaExtent[2],StripeInterval,StripeWidth,WeedingInterval,MinimumWeedingStripeArea,Rettangolo3Point1,Areacosa, Areacosb,cosa, cosb)
        self.startWorker(rds, ListaExtent[3],StripeInterval,StripeWidth,WeedingInterval,MinimumWeedingStripeArea,Rettangolo4Point1,Areacosa, Areacosb,cosa, cosb)
          
        rds = None
        
        return   
            
    
    
    def Dissolve(self):
        
        try:
            processing.runandload("qgis:dissolve",self.iface.activeLayer() , True,'', 'memory: WeedingPlan')
            
        except:
            w = QWidget()
            QMessageBox.warning(w, "Message", "Can't dissolve selected layer!")
          
    
    def FillHoles(self):
        try:
            processing.runandload('qgis:deleteholes', self.iface.activeLayer(), "memory: WeedingPlan")

        except:
            w = QWidget()
            QMessageBox.warning(w, "Message", "Cannot dissolve selected layer!")
        
       
     
    def startWorker(self, rds, ExtentRettangoloRosso,StripeInterval,StripeWidth,WeedingInterval,MinimumWeedingStripeArea,Point1,Areacosa, Areacosb,cosa, cosb):
        # create a new worker instance
        worker = Worker(self.iface,rds, ExtentRettangoloRosso,StripeInterval,StripeWidth,WeedingInterval,MinimumWeedingStripeArea,Point1,Areacosa, Areacosb,cosa, cosb, self.Band, self.ValueToCompare, self.Rule,self.MinimumDistance)
    
        # configure the QgsMessageBar
        messageBar = self.iface.messageBar().createMessage('Processing weeding areas...', )
        cancelButton = QtGui.QPushButton()
        cancelButton.setText('Cancel')
        cancelButton.clicked.connect(worker.kill)
        messageBar.layout().addWidget(cancelButton)
        self.iface.messageBar().pushWidget(messageBar, self.iface.messageBar().INFO)
        self.messageBar = messageBar
    
        # start the worker in a new thread
        thread = QtCore.QThread(self)
        worker.moveToThread(thread)
        worker.finished.connect(self.workerFinished)
        worker.error.connect(self.workerError)
        
        thread.started.connect(worker.run)
        thread.start()
        self.thread = thread
        self.worker = worker
    
    def workerFinished(self, WeedingPlanLayer):

        self.WaitWorker = self.WaitWorker +1   
        if WeedingPlanLayer is not None:
            
            feature_list = WeedingPlanLayer.getFeatures()
            
            Lista = []
            for feat in feature_list:
                Lista.append(feat)
                
            self.WeedingPlanLayerProvider.addFeatures(Lista)
            
            self.iface.messageBar().pushMessage('Weeding plan complete!')
        else:
            # notify the user that something went wrong
            self.iface.messageBar().pushMessage('Weeding plan aborted!', level=QgsMessageBar.CRITICAL, duration=3)
        #print self.WaitWorker    
        if self.WaitWorker == 4:
            self.worker.deleteLater()
            self.thread.quit()
            self.thread.wait()
            self.thread.deleteLater()
            
            VectorLayerName = self.FieldcomboBox.itemData(self.FieldcomboBox.currentIndex())
            VectorLayer = QgsMapLayerRegistry.instance().mapLayer(VectorLayerName)
            self.WeedingPlanLayer.updateExtents()
            QgsMapLayerRegistry.instance().addMapLayer(self.WeedingPlanLayer)
            processing.runandload("qgis:clip",self.WeedingPlanLayer , VectorLayer, 'memory: WeedingPlanAreas')
            
            QgsMapLayerRegistry.instance().removeMapLayer(self.WeedingPlanLayer.id())
            del self.WeedingPlanLayer
            del self.WeedingPlanLayerProvider
            
            self.iface.messageBar().popWidget(self.messageBar)
    
    

    def workerError(self, e, exception_string):
         QgsMessageLog.logMessage('Worker thread raised an exception:\n'.format(exception_string), level=QgsMessageLog.CRITICAL)
         






class WeedingParameter(QDialog,Ui_WeedingParameter):
    def __init__(self,BandNumber,ValueToCompare, VerticalPolicy,HorizontalPolicy,Rule,Band,MinimumDistance):
        QDialog.__init__(self)
        #self.iface = iface
        self.setupUi(self)
        
        self.spinBox.setMaximum(BandNumber)
        self.spinBox.setValue(Band)
        self.doubleSpinBox.setValue(VerticalPolicy)
        self.doubleSpinBox_2.setValue(HorizontalPolicy)
        self.doubleSpinBox_3.setValue(ValueToCompare)
        self.doubleSpinBox_4.setValue(MinimumDistance)
        
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.acceptData)
        
                
                
    def acceptData(self):
        
        WeedingParameter.Band = self.spinBox.value()
        WeedingParameter.Rule = str(self.comboBox_3.currentText())
        WeedingParameter.ValueToCompare = self.doubleSpinBox_3.value()
        
        WeedingParameter.VerticalPolicy = self.doubleSpinBox.value()
        WeedingParameter.HorizontalPolicy = self.doubleSpinBox_2.value()
        
        WeedingParameter.MinimumDistance = self.doubleSpinBox_4.value()
        


