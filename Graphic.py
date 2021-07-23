from PyQt5.QtWidgets import QGridLayout, QLabel, QMainWindow, QHBoxLayout, QWidget ,QVBoxLayout
import os
from PyQt5 import uic, QtWidgets, QtCore,QtGui
from logic import RoboflowLogic, myImage, DetectionObject
from PyQt5.QtGui import QPixmap
import tkinter.filedialog
from tkinter import *
import glob
import cv2
import io
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

from PIL.ImageQt import ImageQt
import random
import pathlib
import time

intro = uic.loadUiType(os.path.join(os.getcwd(), "intro.ui"))[0]
MainPage = uic.loadUiType(os.path.join(os.getcwd(), "MainPage.ui"))[0]
imageView = uic.loadUiType(os.path.join(os.getcwd(), "imageView.ui"))[0]



class MainGUI(QMainWindow, intro):
    def __init__(self):
        super(MainGUI, self).__init__()
        self.setupUi(self)
        self.logoLabel
        self.main_w = None
        self.logoLabel.setScaledContents(True)
        pixmap =QPixmap(os.path.join(os.getcwd(),"logo_big.jpg"))
        self.logoLabel.setPixmap(pixmap)
        self.progressbar.setMaximum(100)
        self.progressbar.setStyleSheet("QProgressBar {border: 2px solid black;border-radius:8px;padding:1px}"
                                       "QProgressBar::chunk {background:#EC524B}")
        self.startProgressBar()
        
        
    @QtCore.pyqtSlot()
    def new_project(self):
        self.main_w = MainPageWindow()
        self.main_w.show()
        self.close()

    def startProgressBar(self):
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.finished.connect(self.new_project)

        self.thread.start()

    def setProgressVal(self, val):
        self.progressbar.setValue(val)


class MainPageWindow(QMainWindow, MainPage):
    def __init__(self):
        
        super(MainPageWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(1452,750)
        #logic object
        self.myLogicObject = RoboflowLogic("chess", "piece")

        #class variables
        self.rotationflag = None
        self.cropPosition =None

        #set Hide or not
        self.finished_uploading.setHidden(True)
        self.delete_selected_folder_file.setHidden(True)
        self.image_box.setHidden(True)
        self.rotate_control_frame.setHidden(True)
        self.CropApplyBTN.setHidden(True)


        #connect signals
        self.upload_data.clicked.connect(self.upload_button)
        self.select_folder.clicked.connect(self.UPloadData_folder)
        self.select_files.clicked.connect(self.UPloadData_files)
        self.delete_selected_folder_file.clicked.connect(self.ClearUPloadData)
        self.finished_uploading.clicked.connect(self.finish_upload)
        self.TrainTestBTN.clicked.connect(self.TrainTestfunc)
        self.addLabelBTN.clicked.connect(self.show_image_labeling)    
        self.preprocessingBTN.clicked.connect(self.preprocessingView)   
        self.filterBTN.clicked.connect(self.filterView)
        self.GenerateBTN.clicked.connect(self.Generate)
        self.DoSplit.clicked.connect(self.Test_Train_Spliter)
        self.rotate.clicked.connect(self.rotate_graphic)
        self.resizeBTN.clicked.connect(self.resizeImage)
        self.RotateApplyBTN.clicked.connect(self.RotateApply)
        self.ResizeApplyBTN.clicked.connect(self.Do_resize)
        self.CropApplyBTN.clicked.connect(self.CropApply)
        self.saveBTN.clicked.connect(self.save)


        #set Enable or not
        self.TrainTestBTN.setEnabled(False)
        self.addLabelBTN.setEnabled(False)
        self.preprocessingBTN.setEnabled(False)
        self.filterBTN.setEnabled(False)
        self.GenerateBTN.setEnabled(False)
        self.main_image_crop.setHidden(True)
        self.changed_image_crop.setHidden(True)
       



        self.start_slider.setRange(0,90)
        self.end_slider.setRange(90,100)
        self.start_slider.setValue(75)
        self.end_slider.setValue(90)
        self.start_slider.valueChanged.connect(self.slider_valuechange)
        self.end_slider.valueChanged.connect(self.slider_valuechange)
        self.Train_Label.setText("75")
        self.Test_Label.setText("15")
        self.Validation_Label.setText("10")
        

        self.upload_frame.setHidden(True)
        self.Test_Train_frame.setHidden(True)
        self.scrollAreaAddLabel.setHidden(True)
        self.filter_frame.setHidden(True)
        self.preprocessing_frame.setHidden(True)
        self.Generate_frame.setHidden(True)


        self.upload_frame.setHidden(True)
        self.scrollAreaAddLabel.setHidden(True)
        self.preprocessing_frame.setHidden(True)
        self.filter_frame.setHidden(True)
        self.Scale_persent.textChanged[str].connect(self.onChanged_Resize)
        self.Scale_persent_brightness.textChanged[str].connect(self.onChanged_brightness)
        self.Scale_persent_noisy_var.textChanged[str].connect(self.onChanged_noise_var)


        self.Test_Train_frame.setHidden(True)
        self.brightness_frame.setHidden(True)
        self.noisy_frame.setHidden(True)
        self.Hue_frame.setHidden(True)
        self.gray_frame.setHidden(True)
        self.Blur_frame.setHidden(True)
        
        self.rotate_frame.setHidden(True)

        self.GrayApplyBTN.clicked.connect(self.GrayApply)
        self.BrightnessApplyBTN.clicked.connect(self.BrightnessApply)
        self.im1.setHidden(True)
        self.im2.setHidden(True)
        self.im3.setHidden(True)
        self.im4.setHidden(True)
        self.im5.setHidden(True)

        self.logo.setScaledContents(True)
        pixmap =QPixmap(os.path.join(os.getcwd(),"logo.jpg"))
        self.logo.setPixmap(pixmap)

  


        self.filterBTN.clicked.connect(self.filter_button)
    
        self.BlurApplyBTN.clicked.connect(self.BlurApply)  

        self.Hue.clicked.connect(self.hueFilter_graphic)
        self.brightness.clicked.connect(self.changeBrightness_graphic)
        self.noisy.clicked.connect(self.noisyFilter_graphic)
        self.gray.clicked.connect(self.filterGray_graphic)
        self.Blur.clicked.connect(self.filterBlur_graphic)
        self.crop.clicked.connect(self.crop_graphic)
        
        
        self.HueApplyBTN.clicked.connect(self.HueApply)
        self.NoisyApplyBTN.clicked.connect(self.NoisyApply)

        self.main_image_crop.mousePressEvent = self.image_crop


        rotate_radio_group=QtWidgets.QButtonGroup(self.radio_rotate_widget)
        rotate_radio_group.addButton(self.clockwis_90)
        rotate_radio_group.addButton(self.counterclockwis_90)
        rotate_radio_group.addButton(self.rotate_180)
        self.clockwis_90.toggled.connect(self.clockwis_90_clicked)
        self.counterclockwis_90.toggled.connect(self.counterclockwis_90_clicked)
        self.rotate_180.toggled.connect(self.rotate_180_clicked)

        self.Resize_Scale_persent = None


    def UPloadData_folder(self):
        Tk().withdraw()      
        slash = tkinter.filedialog.askdirectory()   
        if slash:
            os.path.normpath(slash)                      
            path=glob.glob(slash+"/*") 
            self.myLogicObject.p=path                  
            for i in path:
                img=myImage(i)
                self.myLogicObject.cashData_folder.append(img)

            self.finished_uploading.setHidden(False)
            self.delete_selected_folder_file.setHidden(False)
       
    
    def UPloadData_files(self):
        Tk().withdraw()                              
        slash = tkinter.filedialog.askopenfilename()    
        if slash:
            path=os.path.normpath(slash)                                  
            img=myImage(path)
            self.myLogicObject.cashData_files.append(img)
            self.finished_uploading.setHidden(False)
            self.delete_selected_folder_file.setHidden(False)


    def ClearUPloadData(self):
        self.myLogicObject.cashData_files.clear()
        self.myLogicObject.cashData_folder.clear()
        self.myLogicObject.Data.clear()
        self.myLogicObject.Output.clear()
        self.im1.clear()
        self.im2.clear()
        self.im3.clear()
        self.im4.clear()
        self.im5.clear()
        self.finished_uploading.setHidden(True)
        self.image_box.setHidden(True)


    def upload_button(self):
        self.Generate_frame.setHidden(True)
        self.upload_frame.setHidden(False)
        self.Test_Train_frame.setHidden(True)
        self.scrollAreaAddLabel.setHidden(True)
        self.filter_frame.setHidden(True)
        self.preprocessing_frame.setHidden(True)
        self.upload_data.setStyleSheet('''#upload_data{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                    font: 87 14pt "Segoe UI Black";
                    color:  #EC524B;
                    border: 3px groove #9AD3BC;
                    border-radius:15px; 
                    border-style:outset;}

                ''')
        
  
    def finish_upload(self):
        self.myLogicObject.cashData_folder.extend(self.myLogicObject.cashData_files)
        self.myLogicObject.Data = self.myLogicObject.cashData_folder.copy()
        self.myLogicObject.cashData_folder.clear()
        self.TrainTestBTN.setEnabled(True)
        self.image_box.setHidden(False)
        self.UploadData_showimg()
        self.myLogicObject.Output=self.myLogicObject.Data.copy()
        self.addLabelBTN.setEnabled(True)
        self.preprocessingBTN.setEnabled(True)
        self.filterBTN.setEnabled(True)
        self.GenerateBTN.setEnabled(True)


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



    def TrainTestfunc(self):
        self.upload_frame.setHidden(True)
        self.Test_Train_frame.setHidden(False)
        self.scrollAreaAddLabel.setHidden(True)
        self.filter_frame.setHidden(True)
        self.preprocessing_frame.setHidden(True)
        self.Generate_frame.setHidden(True)
        self.TrainTestBTN.setStyleSheet('''#TrainTestBTN{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                font: 87 14pt "Segoe UI Black";
                color:  #EC524B;
                border: 3px groove #9AD3BC;
                border-radius:15px; 
                border-style:outset;}
                ''')


    def Test_Train_Spliter(self):
        training_pr = int(self.Train_Label.text())/100
        test_pr = int(self.Test_Label.text())/100
        validation_pr = int(self.Validation_Label.text())/100
        self.Trd.setText(f"{training_pr*100} %")
        self.myLogicObject.Test_Train_data(training_pr,validation_pr,test_pr, self.myLogicObject.Data)
        self.Ted.setText(f"{test_pr*100} %")
        self.Trt.setText(str(len(self.myLogicObject.training)))
        self.Tet.setText(str(len(self.myLogicObject.test)))
        self.Vd.setText(f"{validation_pr*100} %")
        self.Vt.setText(str(len(self.myLogicObject.validation)))



    def show_image_labeling(self):
        self.scrollAreaAddLabel.setHidden(False)
        self.upload_frame.setHidden(True)
        self.Test_Train_frame.setHidden(True)
        self.filter_frame.setHidden(True)
        self.preprocessing_frame.setHidden(True)
        self.Generate_frame.setHidden(True)
        self.addLabelBTN.setStyleSheet('''#addLabelBTN{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                font: 10 14pt "Segoe UI Black";
                color:  #EC524B;
                border: 3px groove #9AD3BC;
                border-radius:15px; 
                border-style:outset;}
                ''')
        mywidget = QWidget()
        addLabelLayout = QGridLayout()
        for i in range(len(self.myLogicObject.Data)):
            pix = QPixmap(self.myLogicObject.Data[i].path)
            label = CustomQLabel(id=i)
            label.setFixedSize(200,200)
            label.setStyleSheet='''
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(61, 68, 75, 255), stop:1 rgba(76, 85, 94, 255));
                font: 75 12pt "Nirmala UI";
                color:  rgb(24, 28, 39);
                border: 3px groove rgb(61, 68, 75);
                border-style:outset;
            '''
            pix = pix.scaled(label.size())
            label.setPixmap(pix)
            addLabelLayout.addWidget(label,i/4,i%4)
            label.clicked.connect(self.Labeling)
        mywidget.setLayout(addLabelLayout)
        self.scrollAreaAddLabel.setWidget(mywidget)



    def preprocessingView(self):
        self.upload_frame.setHidden(True)
        self.Test_Train_frame.setHidden(True)
        self.scrollAreaAddLabel.setHidden(True)
        self.filter_frame.setHidden(True)
        self.preprocessing_frame.setHidden(False)
        self.Resize_frame.setHidden(True)
        self.Resize_frame_control.setHidden(True)
        self.Generate_frame.setHidden(True)
        self.preprocessingBTN.setStyleSheet('''#preprocessingBTN{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                    font: 87 14pt "Segoe UI Black";
                    color:  #EC524B;
                    border: 3px groove #9AD3BC;
                    border-radius:15px; 
                    border-style:outset;}
                ''')


    def rotate_graphic(self):
        self.rotate_control_frame.setHidden(False)
        self.rotate_frame.setHidden(False)
        self.main_image_crop.setHidden(True)
        self.changed_image_crop.setHidden(True)
        self.Resize_frame.setHidden(True)
        self.Resize_frame_control.setHidden(True)
        self.rotate.setStyleSheet('''#rotate{
              background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                font: 87 14pt "Segoe UI Black";
                color:  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(217, 74, 69, 255), stop:1 rgba(236, 82, 75, 255));
                border: 3px groove #9AD3BC;
                border-radius:15px; 
                border-style:outset;
                    }
                ''')
        self.resizeBTN.setStyleSheet('''#resizeBTN{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                font: 87 14pt "Segoe UI Black";
                color:  #222831;
                border: 3px groove #9AD3BC;
                border-radius:15px; 
                border-style:outset;
                    }
                ''')
        self.crop.setStyleSheet('''#crop{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                    font: 87 14pt "Segoe UI Black";
                    color:  #222831;
                    border: 3px groove #9AD3BC;
                    border-radius:15px; 
                    border-style:outset;
                    }
                ''')
        pix = QPixmap(self.myLogicObject.Output[0].path)
        pix = pix.scaled(self.main_image_rotate.size())
        self.main_image_rotate.setPixmap(pix)
        self.change_image_rotate.setPixmap(pix)


    def RotateApply(self):
        Output_copy=self.myLogicObject.Output.copy()
        for img in Output_copy :
            self.myLogicObject.Output.remove(img)
            obj = self.myLogicObject.rotate(self.rotationflag,img)
            self.myLogicObject.Output.append(obj)



    def clockwis_90_clicked(self,enabled):
        if enabled :
            img=self.myLogicObject.rotate("ROTATE_90_CLOCKWISE",self.myLogicObject.Output[0])
            pix = QPixmap(img.path)
            pix = pix.scaled(self.change_image_rotate.size())
            self.change_image_rotate.setPixmap(pix)
            self.change_image_rotate.setPixmap(pix)
            self.rotationflag="ROTATE_90_CLOCKWISE"
            

    def counterclockwis_90_clicked(self,enabled):
        if enabled :
            img=self.myLogicObject.rotate("ROTATE_90_COUNTERCLOCKWISE",self.myLogicObject.Output[0])
            pix = QPixmap(img.path)
            pix = pix.scaled(self.change_image_rotate.size())
            self.change_image_rotate.setPixmap(pix)
            self.change_image_rotate.setPixmap(pix)
            self.rotationflag="ROTATE_90_COUNTERCLOCKWISE"




    def rotate_180_clicked(self,enabled):
        if enabled :
            img=self.myLogicObject.rotate("ROTATE_180",self.myLogicObject.Output[0])
            pix = QPixmap(img.path)
            pix = pix.scaled(self.change_image_rotate.size())
            self.change_image_rotate.setPixmap(pix)
            self.change_image_rotate.setPixmap(pix)
            self.rotationflag="ROTATE_180"



    def resizeImage(self):
        self.rotate_control_frame.setHidden(True)
        self.rotate_frame.setHidden(True)
        self.main_image_crop.setHidden(True)
        self.changed_image_crop.setHidden(True)
        self.Resize_frame.setHidden(False)
        self.Resize_frame_control.setHidden(False)
        pix = QPixmap(self.myLogicObject.Output[0].path)
        pix = pix.scaled(self.mainImageResize.size())
        self.mainImageResize.setPixmap(pix)
        self.changedImageResize.setPixmap(pix)
        self.Scale_persent.setText("100")
        self.rotate.setStyleSheet('''#rotate{
              background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                font: 87 14pt "Segoe UI Black";
                color:  #222831;
                border: 3px groove #9AD3BC;
                border-radius:15px; 
                border-style:outset;
                    }
                ''')
        self.resizeBTN.setStyleSheet('''#resizeBTN{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                font: 87 14pt "Segoe UI Black";
                color:  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(217, 74, 69, 255), stop:1 rgba(236, 82, 75, 255));;
                border: 3px groove #9AD3BC;
                border-radius:15px; 
                border-style:outset;
                    }
                ''')
        self.crop.setStyleSheet('''#crop{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                    font: 87 14pt "Segoe UI Black";
                    color:  #222831;
                    border: 3px groove #9AD3BC;
                    border-radius:15px; 
                    border-style:outset;
                    }
                ''')


    def onChanged_Resize(self, text):
        if text == "" or text == "0":
            text = "1"

        if eval(text) > 100 :
            text = "100"

        self.changedImageResize.resize(int(text)/100 * self.mainImageResize.size().height(), int(text)/100 * self.mainImageResize.size().width())
        self.changedImageResize.setScaledContents(True)
        self.Resize_Scale_persent = int(text)


    def Do_resize(self):
        Output_copy=self.myLogicObject.Output.copy()
        for img in Output_copy :
            self.myLogicObject.Output.remove(img)
            obj = self.myLogicObject.resize(img,self.Resize_Scale_persent)
            self.myLogicObject.Output.append(obj)


    def crop_graphic(self):
        self.rotate_control_frame.setHidden(True)
        self.rotate_frame.setHidden(True)
        self.main_image_crop.setHidden(False)
        self.changed_image_crop.setHidden(False)
        self.Resize_frame.setHidden(True)
        self.Resize_frame_control.setHidden(True)
        pix = QPixmap(self.myLogicObject.Output[0].path)
        pix = pix.scaled(self.main_image_crop.size())
        self.main_image_crop.setPixmap(pix)
        self.changed_image_crop.setPixmap(pix)
        self.rotate.setStyleSheet('''#rotate{
              background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                font: 87 14pt "Segoe UI Black";
                color:  #222831;
                border: 3px groove #9AD3BC;
                border-radius:15px; 
                border-style:outset;
                    }
                ''')
        self.resizeBTN.setStyleSheet('''#resizeBTN{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                font: 87 14pt "Segoe UI Black";
                color:  #222831;
                border: 3px groove #9AD3BC;
                border-radius:15px; 
                border-style:outset;
                    }
                ''')
        self.crop.setStyleSheet('''#crop{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                    font: 87 14pt "Segoe UI Black";
                    color:  qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(217, 74, 69, 255), stop:1 rgba(236, 82, 75, 255));
                    border: 3px groove #9AD3BC;
                    border-radius:15px; 
                    border-style:outset;
                    }
                ''')



    def image_crop(self,event):
        self.CropApplyBTN.setHidden(False)
        roi = cv2.selectROI(self.myLogicObject.Output[0].read())
        model_img  = self.myLogicObject.Output[0]
        model_img_height, model_img_width, _ = model_img.read().shape
        obj=self.myLogicObject.crop(self.myLogicObject.Output[0],roi[0]/model_img_width,roi[1]/model_img_height,roi[2]/model_img_width,roi[3]/model_img_height)
        pix = QPixmap(obj.path)
        pix = pix.scaled(self.changed_image_crop.size())
        self.changed_image_crop.setPixmap(pix)
        self.changed_image_crop.setPixmap(pix)
        self.cropPosition=roi


    def CropApply(self):
        Output_copy=self.myLogicObject.Output.copy()
        model_img  = self.myLogicObject.Data[0]
        model_img_height, model_img_width, _ = model_img.read().shape
        for img in Output_copy :
            self.myLogicObject.Output.remove(img)
            obj = self.myLogicObject.crop(img,self.cropPosition[0]/model_img_width,self.cropPosition[1]/model_img_height,self.cropPosition[2]/model_img_height,self.cropPosition[3]/model_img_width)
            self.myLogicObject.Output.append(obj)


    def filterGray_graphic(self):
        self.Blur_frame.setHidden(True)
        self.Hue_frame.setHidden(True)
        self.brightness_frame.setHidden(True)
        self.noisy_frame.setHidden(True)
        self.gray_frame.setHidden(False)
        self.GrayApplyBTN.setHidden(False)
        pix = QPixmap(self.myLogicObject.Output[0].path)
        pix = pix.scaled(self.main_image_gray.size())
        self.main_image_gray.setPixmap(pix)
        img = self.myLogicObject.filterGray(self.myLogicObject.Output[0])
        pix2 = QPixmap(img.path)
        pix2 = pix2.scaled(self.changed_image_gray.size())
        self.changed_image_gray.setPixmap(pix2)


    def GrayApply(self):
        Output_copy=self.myLogicObject.Output.copy()

        for img in Output_copy :
            self.myLogicObject.Output.remove(img)
            obj = self.myLogicObject.filterGray(img)
            self.myLogicObject.Output.append(obj)
            


    def filterBlur_graphic(self):
        self.Blur_frame.setHidden(False)
        self.Hue_frame.setHidden(True)
        self.brightness_frame.setHidden(True)
        self.noisy_frame.setHidden(True)
        self.gray_frame.setHidden(True)
        pix = QPixmap(self.myLogicObject.Output[0].path)
        pix = pix.scaled(self.main_image_blur.size())
        self.main_image_blur.setPixmap(pix)
        img = self.myLogicObject.filterBlur(self.myLogicObject.Output[0])
        pix1 = QPixmap(img.path)
        pix1 = pix1.scaled(self.changed_image_blur.size())
        self.changed_image_blur.setPixmap(pix1)

    def BlurApply(self):
        Output_copy=self.myLogicObject.Output.copy()
        for img in Output_copy :
            self.myLogicObject.Output.remove(img)
            obj = self.myLogicObject.filterBlur(img)
            self.myLogicObject.Output.append(obj)
    

    
    def HueApply(self):
        Output_copy=self.myLogicObject.Output
        for img in Output_copy :
            self.myLogicObject.Output.remove(img)
            obj = self.myLogicObject.hueFilter(img)
            self.myLogicObject.Output.append(obj)


        
    def hueFilter_graphic(self):
        self.Blur_frame.setHidden(True)
        self.Hue_frame.setHidden(False)
        self.brightness_frame.setHidden(True)
        self.noisy_frame.setHidden(True)
        self.gray_frame.setHidden(True)
        pix = QPixmap(self.myLogicObject.Output[0].path)
        pix = pix.scaled(self.main_image_hue.size())
        self.main_image_hue.setPixmap(pix)
        img = self.myLogicObject.hueFilter(self.myLogicObject.Output[0])
        pix2 = QPixmap(img.path)
        pix2 = pix2.scaled(self.changed_image_hue.size())
        self.changed_image_hue.setPixmap(pix2)


    def changeBrightness_graphic(self):
        self.brightness_frame.setHidden(False)
        self.noisy_frame.setHidden(True)
        self.Hue_frame.setHidden(True)
        self.gray_frame.setHidden(True)
        self.Blur_frame.setHidden(True)
        self.Scale_persent_brightness.setText("0")
        pix = QPixmap(self.myLogicObject.Output[0].path)
        pix = pix.scaled(self.main_image_brightness.size())
        self.main_image_brightness.setPixmap(pix)
        self.changed_image_brightness.setPixmap(pix)


    def BrightnessApply(self):
        Output_copy=self.myLogicObject.Output.copy()
        percent = int(self.Scale_persent_brightness.text())
        for img in Output_copy :
            self.myLogicObject.Output.remove(img)
            obj = self.myLogicObject.changeBrightness(img,percent)
            self.myLogicObject.Output.append(obj)




    def onChanged_brightness(self, text):
        if text == "" or text == "0":
            text = "1"

        if eval(text) > 100 :
            text = "100"

        img = self.myLogicObject.changeBrightness(self.myLogicObject.Output[0], int(text))
        pix2 = QPixmap(img.path)
        pix2 = pix2.scaled(self.changed_image_brightness.size())
        self.changed_image_brightness.setPixmap(pix2)


    def noisyFilter_graphic(self):
        self.brightness_frame.setHidden(True)
        self.noisy_frame.setHidden(False)
        self.Hue_frame.setHidden(True)
        self.gray_frame.setHidden(True)
        self.Blur_frame.setHidden(True)
        self.Scale_persent_noisy_var.setText("0.01")
        pix = QPixmap(self.myLogicObject.Output[0].path)
        pix = pix.scaled(self.main_image_noisy.size())
        self.main_image_noisy.setPixmap(pix)
        self.changed_image_noisy.setPixmap(pix)


    
    def NoisyApply(self):
        Output_copy=self.myLogicObject.Output.copy()
        var = float(self.Scale_persent_noisy_var.text())
        for img in Output_copy :
            self.myLogicObject.Output.remove(img)
            obj = self.myLogicObject.noisyFilter(img,0,var)
            self.myLogicObject.Output.append(obj)



    def onChanged_noise_var(self, text):
        if text == "" or text == "0":
            text = "0"

        if eval(text) > 1 :
            text = "1"

        img = self.myLogicObject.noisyFilter(self.myLogicObject.Output[0],0, float(text))
        pix2 = QPixmap(img.path)
        pix2 = pix2.scaled(self.changed_image_noisy.size())
        self.changed_image_noisy.setPixmap(pix2)


    def Generate(self):
        self.Generate_frame.setHidden(False)
        self.upload_frame.setHidden(True)
        self.Test_Train_frame.setHidden(True)
        self.scrollAreaAddLabel.setHidden(True)
        self.filter_frame.setHidden(True)
        self.preprocessing_frame.setHidden(False)
        self.Resize_frame.setHidden(True)
        self.Resize_frame_control.setHidden(True)
        self.GenerateBTN.setStyleSheet('''#GenerateBTN{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                font: 87 14pt "Segoe UI Black";
                color:  #EC524B;
                border: 3px groove #9AD3BC;
                border-radius:15px; 
                border-style:outset;}

                ''')
        if len(self.myLogicObject.Output) > 5:
            out = random.sample(self.myLogicObject.Output, 5)
        else:
            out = self.myLogicObject.Output
        for i in range(0,len(out)):
            pixmap =QPixmap(out[i].path)
            pixmap = pixmap.scaled(eval(f"self.im{i+1}_2").size())
            eval(f"self.im{i+1}_2").setPixmap(pixmap)
            

    def filterView(self):
        self.upload_frame.setHidden(True)
        self.Test_Train_frame.setHidden(True)
        self.scrollAreaAddLabel.setHidden(True)
        self.filter_frame.setHidden(False)
        self.preprocessing_frame.setHidden(True)
        self.Generate_frame.setHidden(True)



    
    def filter_button(self):
        self.filter_frame.setHidden(False)
        self.filterBTN.setStyleSheet(''' #filterBTN{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(154, 211, 188, 255), stop:1 rgba(170, 231, 206, 255));
                    font: 87 14pt "Segoe UI Black";
                    color:  #EC524B;
                    border: 3px groove #9AD3BC;
                    border-radius:15px; 
                    border-style:outset;}
        ''')
        
 

    def UPloadData_Drag_Drop(self):
        pass
        # self.Dragdrop=DragDrop()


       

    def show_image_labeling(self):
        self.scrollAreaAddLabel.setHidden(False)
        self.upload_frame.setHidden(True)
        self.Test_Train_frame.setHidden(True)
        self.filter_frame.setHidden(True)
        self.preprocessing_frame.setHidden(True)
        mywidget = QWidget()
        addLabelLayout = QGridLayout()
        for i in range(len(self.myLogicObject.Data)):
            pix = QPixmap(self.myLogicObject.Data[i].path)
            label = CustomQLabel(id=i)
            label.setFixedSize(200,200)
            label.setStyleSheet='''
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(61, 68, 75, 255), stop:1 rgba(76, 85, 94, 255));
                font: 75 12pt "Nirmala UI";
                color:  rgb(24, 28, 39);
                border: 3px groove rgb(61, 68, 75);
                border-style:outset;
            '''
            pix = pix.scaled(label.size())
            label.setPixmap(pix)
            addLabelLayout.addWidget(label,i/4,i%4)
            label.clicked.connect(self.Labeling)
        mywidget.setLayout(addLabelLayout)
        self.scrollAreaAddLabel.setWidget(mywidget)




    def slider_valuechange(self):
        size1 = self.start_slider.value()
        size2 = self.end_slider.value()
        self.Train_Label.setText(str(size1))
        self.Test_Label.setText(str(size2 - size1))
        self.Validation_Label.setText(str(100-size2))


    

    def Labeling(self):
        sender = self.sender()
        img = self.myLogicObject.Data[sender.id]
        self.image_view_window = PageLabelingWindow(img)
        self.image_view_window.show()


    def save(self):
        self.myLogicObject.test.clear()
        self.myLogicObject.training.clear()
        self.myLogicObject.validation.clear()
        print("666",self.Train_Label.text(),self.Test_Label.text(),self.Validation_Label.text())
        training_pr = int(self.Train_Label.text())/100
        test_pr = int(self.Test_Label.text())/100
        validation_pr = int(self.Validation_Label.text())/100
        print("55",training_pr,validation_pr,test_pr)
        self.myLogicObject.Test_Train_data(training_pr,validation_pr,test_pr,self.myLogicObject.Output)
        print(self.myLogicObject.test)
        print(self.myLogicObject.training)
        print(self.myLogicObject.validation)
        Tk().withdraw()      
        slash = tkinter.filedialog.asksaveasfilename()

        odir = str(slash.split("/")[-1])
        selected_dir = "/".join(slash.split("/")[:-1])
        out  = os.path.join(selected_dir, odir)
        if not pathlib.Path(out).exists():
            os.mkdir(out)


        self.myLogicObject.make_final_files(slash)


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
        
        if not self.img.detection_obj:
            self.FinishedBTN.setEnabled(False)
    
    def add_Label(self):
        self.FinishedBTN.setEnabled(True)
        LabelText = self.lineEntry.text()
        if self.selectedRect.LogicalObj == None:
            d = DetectionObject((self.selectedRect.start.x() + (self.selectedRect.end.x() - self.selectedRect.start.x())/2,self.selectedRect.start.y() + (self.selectedRect.end.y() -self.selectedRect.start.y())/2), LabelText, self.selectedRect.start, self.selectedRect.end)
            self.selectedRect.LogicalObj = d
            self.img.add_detection_obj(self.selectedRect.LogicalObj)
            self.selectedRect.showLabel = QLabel(self.selectedRect.LogicalObj.label,self)
            self.selectedRect.showLabel.setStyleSheet('''QLabel{
                                background-color: #F5B461;
                                font: 87 14pt "Segoe UI Black";
                                color:  #222831;
                                border: 0px groove #9AD3BC;
                                border-radius:15px; 
                                border-style:outset;}
                                ''')
            self.LabelLayout.addWidget(self.selectedRect.showLabel)
        else:
            self.img.detection_obj.remove(self.selectedRect.LogicalObj)
            self.selectedRect.LogicalObj =  DetectionObject((self.selectedRect.start.x() + (self.selectedRect.end.x() - self.selectedRect.start.x())/2,self.selectedRect.start.y() + (self.selectedRect.end.y() -self.selectedRect.start.y())/2), LabelText)
            self.img.add_detection_obj(self.selectedRect.LogicalObj)
            
        self.lineEntry.setText("")
        self.lineEntry.setEnabled(False)
        self.setLabelBTN.setEnabled(False)

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


class CustomQLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def __init__(self,id):
        super(CustomQLabel, self).__init__()
        self.id = id

    def mousePressEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLabel.mousePressEvent(self, event)


class MyThread(QtCore.QThread):
    change_value = QtCore.pyqtSignal(int)
    finish = QtCore.pyqtSignal(bool)
    def run(self):
        cnt = 0
        while cnt < 100:
            cnt+=1
            time.sleep(0.001)
            self.change_value.emit(cnt)
        self.finish.emit(True)
        

    