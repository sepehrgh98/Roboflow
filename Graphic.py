from PyQt5.QtWidgets import QLabel, QMainWindow, QLineEdit, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsScene, QStyle, QProxyStyle 
import os
from PyQt5 import uic, QtWidgets, QtCore,QtGui
from logic import RoboflowLogic, myImage, DetectionObject
from PyQt5.QtGui import QPixmap
import tkinter.filedialog
from tkinter import *
import glob
import cv2




ProjectsWindow = uic.loadUiType(os.path.join(os.getcwd(), "ProjectsWindow.ui"))[0]
MainPage = uic.loadUiType(os.path.join(os.getcwd(), "MainPage.ui"))[0]
imageView = uic.loadUiType(os.path.join(os.getcwd(), "imageView.ui"))[0]



class MainGUI(QMainWindow, ProjectsWindow):
    def __init__(self):
        super(MainGUI, self).__init__()
        self.setupUi(self)
        self.newBTN.clicked.connect(self.new_project)
        self.main_w = None


    def new_project(self):
        self.main_w = MainPageWindow()
        self.main_w.show()
        self.close()


class MainPageWindow(QMainWindow, MainPage):
    def __init__(self):
        super(MainPageWindow, self).__init__()
        self.setupUi(self)
        self.myLogicObject = RoboflowLogic("chess", "piece")
        self.UploadDataBTN.clicked.connect(self.UPloadData)
        self.start_slider.setRange(0,90)
        self.end_slider.setRange(90,100)
        self.start_slider.setValue(75)
        self.end_slider.setValue(90)
        self.start_slider.valueChanged.connect(self.slider_valuechange)
        self.end_slider.valueChanged.connect(self.slider_valuechange)
        self.Train_Label.setText("75")
        self.Test_Label.setText("15")
        self.Validation_Label.setText("10")
        self.DoSplit.clicked.connect(self.Test_Train_Spliter)
        self.Test_Train_frame.setHidden(True)
        self.Add_Label_frame.setHidden(True)
        self.TrainTestBTN.clicked.connect(lambda:self.Test_Train_frame.setHidden(False))
        self.addLabelBTN.clicked.connect(self.show_image_labeling)
        # if len(self.myLogicObject.Data):
        #     for image in self.myLogicObject.Data:
        #         print(image)

        # img = myImage(os.getcwd()+r'\Pic.jpg')
        # self.myLogicObject.Data.append(img)


        # imageBTN = QPushButton(self.frame_6)
        # imageBTN.clicked.connect(lambda: self.Labeling(img))
        # imageBTN.setIcon(QtGui.QIcon(self.myLogicObject.Data[0].path))
        # imageBTN.setIconSize(QtCore.QSize(50,50))
        # self.image_view_window = None

    def show_image_labeling(self):
        self.Add_Label_frame.setHidden(False)
        for img in self.myLogicObject.Data:
            label = QLabel(self.Add_Label_frame)
            label.resize(50,50)
            pix = QPixmap(img.path)
            pix = pix.scaled(label.size())
            label.setPixmap(pix)
            self.Images_gridLayout.addWidget(label)
            label.mousePressEvent = lambda event, img=img: self.Labeling(event, img)

    def Test_Train_Spliter(self):
        training_pr = int(self.Train_Label.text())/100
        test_pr = int(self.Test_Label.text())/100
        validation_pr = int(self.Validation_Label.text())/100
        self.myLogicObject.Test_Train_data(training_pr,validation_pr,test_pr)
        self.Trd.setText(f"{training_pr*100} %")
        self.Trt.setText(str(len(self.myLogicObject.training)))
        self.Ted.setText(f"{test_pr*100} %")
        self.Tet.setText(str(len(self.myLogicObject.test)))
        self.Vd.setText(f"{validation_pr*100} %")
        self.Vt.setText(str(len(self.myLogicObject.validation)))


    def slider_valuechange(self):
        size1 = self.start_slider.value()
        size2 = self.end_slider.value()
        self.Train_Label.setText(str(size1))
        self.Test_Label.setText(str(size2 - size1))
        self.Validation_Label.setText(str(100-size2))




    def UPloadData(self):
        Tk().withdraw()                              
        slash = tkinter.filedialog.askdirectory()    
        os.path.normpath(slash)                      
        path=glob.glob(slash+"/*")                    
        for i in path:
            img=myImage(i)
            self.myLogicObject.Data.append(img)

        print(self.myLogicObject.Data)


    def Labeling(self,event ,img):
        self.image_view_window = PageLabelingWindow(img)
        self.image_view_window.show()


class PageLabelingWindow(QMainWindow, imageView):
    def __init__(self, img):
        super(PageLabelingWindow, self).__init__()
        self.setupUi(self)
        self.img = img
        self.scene = CustomQgraphicScene(self.ImageView)
        self.ImageView.setScene(self.scene)
        pix = QPixmap(self.img.path)
        pix = pix.scaled(self.ImageView.size())
        self.scene.addPixmap(pix)
        self.scene.position.connect(self.make_label_signal)
        self.selectedRect = None
        self.lineEntry.setEnabled(False)
        self.setLabelBTN.setEnabled(False)
        self.setLabelBTN.clicked.connect(self.add_Label)
        self.FinishedBTN.clicked.connect(self.LabelingFinished)
        self.FinishedBTN.setEnabled(False)
        self.DeleteBTN.setEnabled(False)
        self.DeleteBTN.clicked.connect(self.removeLabel)
        self.lineEntry.textChanged[str].connect(self.onChanged)
        
    
    def onChanged(self, text):
        if text == "":
            self.setLabelBTN.setEnabled(False)
        else:
            self.setLabelBTN.setEnabled(True)

    def LabelingFinished(self):
        self.close()


    def make_label_signal(self, rect):
        self.lineEntry.setEnabled(True)        
        if rect.LogicalObj != None:
            self.lineEntry.setText(rect.LogicalObj.label)
            self.DeleteBTN.setEnabled(True)
        self.selectedRect = rect


    def removeLabel(self):
        if self.selectedRect:
            self.img.detection_obj.remove(self.selectedRect.LogicalObj)
            self.selectedRect.LogicalObj = None
            self.selectedRect.showLabel.deleteLater()
            self.scene.removeItem(self.selectedRect)
            self.DeleteBTN.setEnabled(False)
            self.lineEntry.setText("")

        
        print(self.img.detection_obj)
        if not self.img.detection_obj:
            self.FinishedBTN.setEnabled(False)
    
    def add_Label(self):
        self.FinishedBTN.setEnabled(True)
        LabelText = self.lineEntry.text()
        if self.selectedRect.LogicalObj == None:
            d = DetectionObject((self.selectedRect.start.x() + (self.selectedRect.end.x() - self.selectedRect.start.x())/2,self.selectedRect.start.y() + (self.selectedRect.end.y() -self.selectedRect.start.y())/2), LabelText)
            self.selectedRect.LogicalObj = d
            self.img.add_detection_obj(self.selectedRect.LogicalObj)
            self.selectedRect.showLabel = QLabel(self.selectedRect.LogicalObj.label,self)
            # self.selectedRect.delBTN.setEnabled(False)
            self.LabelLayout.addWidget(self.selectedRect.showLabel)
            # self.selectedRect.delBTN.clicked.connect(lambda:self.removeLabel(self.selectedRect))
        else:
            self.img.detection_obj.remove(self.selectedRect.LogicalObj)
            self.selectedRect.LogicalObj =  DetectionObject((self.selectedRect.start.x() + (self.selectedRect.end.x() - self.selectedRect.start.x())/2,self.selectedRect.start.y() + (self.selectedRect.end.y() -self.selectedRect.start.y())/2), LabelText)
            self.img.add_detection_obj(self.selectedRect.LogicalObj)
            


        self.lineEntry.setText("")
        self.lineEntry.setEnabled(False)
        self.setLabelBTN.setEnabled(False)
        print(self.img.detection_obj)



    def HideLabel(self):
        self.lineEntry.setHidden(True)
        self.setLabelBTN.setHidden(True)
        self.lineEntry.setText("")
        



class CustomQgraphicScene(QtWidgets.QGraphicsScene):
    position = QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super(CustomQgraphicScene, self).__init__(parent)
        self.clickedPosition_start = QtCore.QPointF()
        self.clickedPosition_end = QtCore.QPointF()
        self._current_rect_item = None
        self.clickedRect = None

    def mousePressEvent(self, event):
        if not isinstance(self.itemAt(event.scenePos(), QtGui.QTransform()), CustomQGraphicsRectItem):
            self._current_rect_item = CustomQGraphicsRectItem()
            self._current_rect_item.setBrush(QtGui.QColor(100, 10, 10, 40))
            self._current_rect_item.setFlag(CustomQGraphicsRectItem.ItemIsMovable, True)
            self.addItem(self._current_rect_item)
            self._current_rect_item.start = event.scenePos()
            r = QtCore.QRectF(self._current_rect_item.start , self._current_rect_item.start )
            self._current_rect_item.setRect(r)
        else:
            self.clickedRect = self.itemAt(event.scenePos(), QtGui.QTransform())
            self.clickedPosition_start = event.scenePos()
        super(CustomQgraphicScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._current_rect_item is not None:
            r = QtCore.QRectF(self._current_rect_item.start , event.scenePos()).normalized()
            self._current_rect_item.setRect(r)
        super(CustomQgraphicScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.clickedRect and isinstance(self.itemAt(event.scenePos(), QtGui.QTransform()), CustomQGraphicsRectItem):
            self.clickedPosition_end = event.scenePos()
            destination_x = self.clickedPosition_end.x() - self.clickedPosition_start.x()
            destination_y = self.clickedPosition_end.y() - self.clickedPosition_start.y()
            destination = QtCore.QPointF(destination_x, destination_y)
            self.clickedRect.start  = self.clickedRect.start  + destination
            self.clickedRect.end = self.clickedRect.end + destination
            self.position.emit(self.clickedRect)
        elif not self.clickedRect and isinstance(self.itemAt(event.scenePos(), QtGui.QTransform()), CustomQGraphicsRectItem):
            print(isinstance(self.itemAt(event.scenePos(), QtGui.QTransform()), CustomQGraphicsRectItem))
            self._current_rect_item.end = event.scenePos()
            self.position.emit(self._current_rect_item)

        self.clickedRect = None
        self._current_rect_item = None
        super(CustomQgraphicScene, self).mouseReleaseEvent(event)


class CustomQGraphicsRectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self):
        super(CustomQGraphicsRectItem, self).__init__()
        self.start = QtCore.QPointF()
        self.end = QtCore.QPointF()
        self.LogicalObj = None
        self.showLabel = None


        
