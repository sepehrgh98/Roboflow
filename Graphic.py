from PyQt5.QtWidgets import QLabel, QMainWindow, QLineEdit, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsScene, QStyle, QProxyStyle 
import os
from PyQt5 import uic, QtWidgets, QtCore,QtGui
from logic import RoboflowLogic, myImage, DetectionObject
from PyQt5.QtGui import QPixmap
import tkinter.filedialog
from tkinter import *
import glob
import cv2
import io
from PIL.ImageQt import ImageQt
import argparse



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
        self.rotationflag = None
        self.cropPosition =None
        # self.UploadDataBTN.clicked.connect(self.UPloadData)
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
        

        self.upload_frame.setHidden(True)
        self.Add_Label_frame.setHidden(True)
        self.preprocessing_frame.setHidden(True)
        self.filter_frame.setHidden(True)
        self.image_box.setHidden(True)

        self.Test_Train_frame.setHidden(True)
        self.brightness_frame.setHidden(True)
        self.noisy_frame.setHidden(True)
        # self.crop_frame.setHiden(True)
        self.Hue_frame.setHidden(True)
        self.gray_frame.setHidden(True)
        self.Blur_frame.setHidden(True)
        self.rotate_control_frame.setHidden(True)
        self.rotate_frame.setHidden(True)

        self.im1.setHidden(True)
        self.im2.setHidden(True)
        self.im3.setHidden(True)
        self.im4.setHidden(True)
        self.im5.setHidden(True)
        # self.DeleteBTN.setHidden(True)
        # self.DeleteBTN.setHidden(True)
        # self.DeleteBTN.setHidden(True)
        # self.DeleteBTN.setHidden(True)

        self.main_image_crop.setHidden(True)
        self.changed_image_crop.setHidden(True)
        self.CropApplyBTN.setHidden(True)
        


        self.upload_data.clicked.connect(self.upload_button)
        self.filterBTN.clicked.connect(self.filter_button)
        self.preprocessingBTN.clicked.connect(self.preprocessing_button)
        self.RotateApplyBTN.clicked.connect(self.RotateApply)

        self.Hue.clicked.connect(self.hueFilter_graphic)
        self.brightness.clicked.connect(self.changeBrightness_graphic)
        self.noisy.clicked.connect(self.noisyFilter_graphic)
        self.gray.clicked.connect(self.filterGray_graphic)
        self.Blur.clicked.connect(self.filterBlur_graphic)
        self.crop.clicked.connect(self.crop_graphic)
        self.rotate.clicked.connect(self.rotate_graphic)
        self.CropApplyBTN.clicked.connect(self.CropApply)


        self.main_image_crop.mousePressEvent = self.image_crop


        rotate_radio_group=QtWidgets.QButtonGroup(self.radio_rotate_widget)
        rotate_radio_group.addButton(self.clockwis_90)
        rotate_radio_group.addButton(self.counterclockwis_90)
        rotate_radio_group.addButton(self.rotate_180)
        self.clockwis_90.toggled.connect(self.clockwis_90_clicked)
        self.counterclockwis_90.toggled.connect(self.counterclockwis_90_clicked)
        self.rotate_180.toggled.connect(self.rotate_180_clicked)

    def clockwis_90_clicked(self,enabled):
        if enabled :
            path=self.myLogicObject.rotate("ROTATE_90_CLOCKWISE",self.myLogicObject.Data[0])
            pix = QPixmap(path)
            pix = pix.scaled(self.change_image_rotate.size())
            self.change_image_rotate.setPixmap(pix)
            self.change_image_rotate.setPixmap(pix)
            self.rotationflag="ROTATE_90_CLOCKWISE"
            

    def counterclockwis_90_clicked(self,enabled):
        if enabled :
            path=self.myLogicObject.rotate("ROTATE_90_COUNTERCLOCKWISE",self.myLogicObject.Data[0])
            pix = QPixmap(path)
            pix = pix.scaled(self.change_image_rotate.size())
            self.change_image_rotate.setPixmap(pix)
            self.change_image_rotate.setPixmap(pix)
            self.rotationflag="ROTATE_90_COUNTERCLOCKWISE"

    def rotate_180_clicked(self,enabled):
        if enabled :
            path=self.myLogicObject.rotate("ROTATE_180",self.myLogicObject.Data[0])
            pix = QPixmap(path)
            pix = pix.scaled(self.change_image_rotate.size())
            self.change_image_rotate.setPixmap(pix)
            self.change_image_rotate.setPixmap(pix)
            self.rotationflag="ROTATE_180"

    def RotateApply(self):
        Output_copy=self.myLogicObject.Output
        for img in Output_copy :
            self.myLogicObject.Output.remove(img)
            self.myLogicObject.rotate(self.rotationflag,img)
            self.myLogicObject.Output.append(img)
        
        



    def image_crop(self,event):
        self.CropApplyBTN.setHidden(False)
        roi = cv2.selectROI(self.myLogicObject.Data[0].read())
        path=self.myLogicObject.crop(self.myLogicObject.Data[0],roi[0],roi[1],roi[2],roi[3])
        pix = QPixmap(path)
        pix = pix.scaled(self.changed_image_crop.size())
        self.changed_image_crop.setPixmap(pix)
        self.changed_image_crop.setPixmap(pix)
        self.cropPosition=roi


    def CropApply(self):

        Output_copy=self.myLogicObject.Output
        for img in Output_copy :
            self.myLogicObject.Output.remove(img)
            self.myLogicObject.crop(img,self.cropPosition[0],self.cropPosition[1],self.cropPosition[2],self.cropPosition[3])
            self.myLogicObject.Output.append(img)

    def upload_button(self):
        # self.Add_Label_frame.setHidden(True)
        # self.preprocessing_frame.setHidden(True)
        # self.filter_frame.setHidden(True)
        # self.Test_Train_frame.setHidden(True)
        self.upload_frame.setHidden(False)
        self.select_folder.clicked.connect(self.UPloadData_folder)
        self.finished_uploading.clicked.connect(self.finish_upload)
        self.select_files.clicked.connect(self.UPloadData_files)
        self.UPloadData_Drag_Drop()
        # self.UPloadData_Drag_Drop()
    
    def filter_button(self):
        
        # self.upload_frame.setHidden(True)
        # self.Add_Label_frame.setHidden(True)
        # self.preprocessing_frame.setHidden(True)
        # self.Test_Train_frame.setHidden(True)
        self.filter_frame.setHidden(False)
        # self.gray.clicked.connect(self.)
        # self.Blur.clicked.connect(self.)
        
        
        
    
    def preprocessing_button(self):
        # self.upload_frame.setHidden(True)
        # self.Add_Label_frame.setHidden(True)
        # self.Test_Train_frame.setHidden(True)
        # self.filter_frame.setHidden(True)
        self.preprocessing_frame.setHidden(False)
        
        
        # self.rotate.clicked.connect(self.)
        # self.resize.clicked.connect(self.)
        
        



    def UPloadData_folder(self):
        
        Tk().withdraw()      
        slash = tkinter.filedialog.askdirectory()    
        os.path.normpath(slash)                      
        path=glob.glob(slash+"/*") 
        self.myLogicObject.p=path                  
        for i in path:
            img=myImage(i)
            self.myLogicObject.cashData_folder.append(img)
       
    
    def UPloadData_files(self):
        Tk().withdraw()                              
        slash = tkinter.filedialog.askopenfilename()    
        path=os.path.normpath(slash)                                  
        img=myImage(path)
        self.myLogicObject.cashData_files.append(img)
        
        


    def UPloadData_Drag_Drop(self):
        pass
        # self.Dragdrop=DragDrop()


      


    def finish_upload(self):
        self.myLogicObject.cashData_folder.extend(self.myLogicObject.cashData_files)
        self.myLogicObject.Data = self.myLogicObject.cashData_folder.copy()
        self.myLogicObject.cashData_folder.clear()

        self.image_box.setHidden(False)
        self.UploadData_showimg()
        self.myLogicObject.Output=self.myLogicObject.Data.copy()
    

    def UploadData_showimg(self):
        
        if(len(self.myLogicObject.Data)==1):
            self.im1.setHidden(False)
            self.im1.setScaledContents(True)
            pixmap =QPixmap(self.myLogicObject.Data[0].path)
            self.im1.setPixmap(pixmap)

        elif(len(self.myLogicObject.Data)==2):
            self.im1.setHidden(False)
            self.im2.setHidden(False)
            self.im1.setScaledContents(True)
            self.im2.setScaledContents(True)
            pixmap =QPixmap(self.myLogicObject.Data[0].path)
            self.im1.setPixmap(pixmap)
            pixmap =QPixmap(self.myLogicObject.Data[1].path)
            self.im2.setPixmap(pixmap)
           
        elif(len(self.myLogicObject.Data)==3):
            self.im1.setHidden(False)
            self.im2.setHidden(False)
            self.im3.setHidden(False)
            self.im1.setScaledContents(True)
            self.im2.setScaledContents(True)
            self.im3.setScaledContents(True)
            pixmap =QPixmap(self.myLogicObject.Data[0].path)
            self.im1.setPixmap(pixmap)
            pixmap =QPixmap(self.myLogicObject.Data[1].path)
            self.im2.setPixmap(pixmap)
            pixmap =QPixmap(self.myLogicObject.Data[2].path)
            self.im3.setPixmap(pixmap)

        elif(len(self.myLogicObject.Data)==4):
            self.im1.setHidden(False)
            self.im2.setHidden(False)
            self.im3.setHidden(False)
            self.im4.setHidden(False)
            self.im1.setScaledContents(True)
            self.im2.setScaledContents(True)
            self.im3.setScaledContents(True)
            self.im4.setScaledContents(True)
            pixmap =QPixmap(self.myLogicObject.Data[0].path)
            self.im1.setPixmap(pixmap)
            pixmap =QPixmap(self.myLogicObject.Data[1].path)
            self.im2.setPixmap(pixmap)
            pixmap =QPixmap(self.myLogicObject.Data[2].path)
            self.im3.setPixmap(pixmap)
            pixmap =QPixmap(self.myLogicObject.Data[3].path)
            self.im4.setPixmap(pixmap)

        elif(len(self.myLogicObject.Data)>=5):
            self.im1.setHidden(False)
            self.im2.setHidden(False)
            self.im3.setHidden(False)
            self.im4.setHidden(False)
            self.im5.setHidden(False)
            self.im1.setScaledContents(True)
            self.im2.setScaledContents(True)
            self.im3.setScaledContents(True)
            self.im4.setScaledContents(True)
            self.im5.setScaledContents(True)
            pixmap =QPixmap(self.myLogicObject.Data[0].path)
            self.im1.setPixmap(pixmap)
            pixmap =QPixmap(self.myLogicObject.Data[1].path)
            self.im2.setPixmap(pixmap)
            pixmap =QPixmap(self.myLogicObject.Data[2].path)
            self.im3.setPixmap(pixmap)
            pixmap =QPixmap(self.myLogicObject.Data[3].path)
            self.im4.setPixmap(pixmap)
            pixmap =QPixmap(self.myLogicObject.Data[4].path)
            self.im5.setPixmap(pixmap)
       

    def noisyFilter_graphic(self):
        self.noisy_frame.setHidden(False)
        cv2.imshow("1",self.myLogicObject.noisyFilter()[0])
        
        
    def hueFilter_graphic(self):
        self.Hue_frame.setHidden(False)
        print(self.myLogicObject.hueFilter())
        

    def filterGray_graphic(self):
        self.gray_frame.setHidden(False)
        cv2.imshow("1",self.myLogicObject.filterGray()[0])

    def filterBlur_graphic(self):
        self.Blur_frame.setHidden(False)
        cv2.imshow("1",self.myLogicObject.filterBlur()[0])

    def changeBrightness_graphic(self):
        self.brightness_frame.setHidden(False)
        print(self.myLogicObject.changeBrightness())


    def rotate_graphic(self):
        self.rotate_control_frame.setHidden(False)
        self.rotate_frame.setHidden(False)
        pix = QPixmap(self.myLogicObject.Data[0].path)
        pix = pix.scaled(self.main_image_rotate.size())
        self.main_image_rotate.setPixmap(pix)
        self.change_image_rotate.setPixmap(pix)
        # self.myLogicObject.rotate("ROTATE_180")



    def crop_graphic(self):
        self.main_image_crop.setHidden(False)
        self.changed_image_crop.setHidden(False)
        
        pix = QPixmap(self.myLogicObject.Data[0].path)
        pix = pix.scaled(self.main_image_crop.size())
        self.main_image_crop.setPixmap(pix)
        self.changed_image_crop.setPixmap(pix)

        # img_raw = self.myLogicObject.Data[0].read()
        # roi = cv2.selectROI(img_raw)
        # print(roi)
        # self.myLogicObject.crop(roi[0],roi[1],roi[2],roi[3])





    def show_image_labeling(self):
        self.Add_Label_frame.setHidden(False)
        # for img in self.myLogicObject.Data:
        #     label = QLabel(self.Add_Label_frame)
        #     label.resize(50,50)
        #     pix = QPixmap(img.path)
        #     pix = pix.scaled(label.size())
        #     label.setPixmap(pix)
        #     self.Images_gridLayout.addWidget(label)
        #     label.mousePressEvent = lambda event, img=img: self.Labeling(event, img)

    def Test_Train_Spliter(self):
        training_pr = int(self.Train_Label.text())/100
        test_pr = int(self.Test_Label.text())/100
        validation_pr = int(self.Validation_Label.text())/100
        self.Trd.setText(f"{training_pr*100} %")
        self.myLogicObject.Test_Train_data(training_pr,validation_pr,test_pr)
        self.Ted.setText(f"{test_pr*100} %")
        self.Trt.setText(str(len(self.myLogicObject.training)))
        self.Tet.setText(str(len(self.myLogicObject.test)))
        self.Vd.setText(f"{validation_pr*100} %")
        self.Vt.setText(str(len(self.myLogicObject.validation)))


    def slider_valuechange(self):
        size1 = self.start_slider.value()
        size2 = self.end_slider.value()
        self.Train_Label.setText(str(size1))
        self.Test_Label.setText(str(size2 - size1))
        self.Validation_Label.setText(str(100-size2))


    

    def Labeling(self,event ,img):
        self.image_view_window = PageLabelingWindow(img)
        self.image_view_window.show()

class DragDrop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop")
        self.resize(720, 480)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            img=myImage(f)
            print(img)
            # self.myLogicObject.cashData_files.append(img)


            
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


        


# img=self.myLogicObject.noisyFilter()[0]
#         channels = 1
#         print(img.shape)
#         height, width = img.shape[:2]
#         print(height)
#         print(img.data)
#         bytesPerLine = channels * width
#         qImg = QtGui.QImage(img.data, width, height, QtGui.QImage.Format_RGB)
#         pixmap = QtGui.QPixmap(qImg)
#         self.label_6.setPixmap(pixmap)
#         print(qImg)