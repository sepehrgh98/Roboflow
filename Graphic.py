from PyQt5.QtWidgets import QLabel, QMainWindow, QLineEdit, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsScene, QStyle, QProxyStyle 
import os
from PyQt5 import uic, QtWidgets, QtCore,QtGui
from logic import RoboflowLogic
from PyQt5.QtGui import QPixmap

from PIL import ImageTk 
from PIL import  Image
import tkinter.filedialog
from tkinter import *
from tkinter import filedialog 
from zipfile import ZipFile
import cv2
import glob



ProjectsWindow = uic.loadUiType(os.path.join(os.getcwd(), "ProjectsWindow.ui"))[0]
MainPage = uic.loadUiType(os.path.join(os.getcwd(), "MainPage.ui"))[0]



class MainGUI(QMainWindow, ProjectsWindow):
    def __init__(self):
        super(MainGUI, self).__init__()
        self.setupUi(self)
        self.newBTN.clicked.connect(self.new_project)
        self.main_w = None


    def new_project(self):
        self.main_w = newProject()
        self.main_w.show()
        self.close()



class newProject(QMainWindow, MainPage):
    def __init__(self):
        super(newProject, self).__init__()
        self.setupUi(self)

        self.myLogicObject = RoboflowLogic("chess", "piece")
        
        self.upload_frame.setHidden(True)
        self.image_box.setHidden(True)
        self.im1.setHidden(True)
        self.im2.setHidden(True)
        self.im3.setHidden(True)
        self.im4.setHidden(True)
        self.im5.setHidden(True)
        # self.DeleteBTN.setHidden(True)
        # self.DeleteBTN.setHidden(True)
        # self.DeleteBTN.setHidden(True)
        # self.DeleteBTN.setHidden(True)

        self.upload_data.clicked.connect(self.upload_Data)
        # self.upload_data.clicked.connect(self.)
        # self.upload_data.clicked.connect(self.)
        # self.preprocessing.clicked.connect(self.)
        # self.generate.clicked.connect(self.)
        
        

    def upload_Data(self):
        self.upload_frame.setHidden(False)
        self.select_folder.clicked.connect(self.UPloadData_folder)
        self.select_files.clicked.connect(self.UPloadData_files)
        self.finished_uploading.clicked.connect(self.finish_upload)


    def UPloadData_folder(self):
        

        Tk().withdraw()                              #to hide the window behind the selector screen
        slash = tkinter.filedialog.askdirectory()    #select file dialog
        os.path.normpath(slash)                      # / --> //
        path=glob.glob(slash+"/*")                    #  read multiple images address    
        for i in path:
            img=myImage(i)
            self.myLogicObject.cash_Data.append(img)
       
    
    def UPloadData_files(self):
        print(self.myLogicObject.Data)
        Tk().withdraw()                              
        slash = tkinter.filedialog.askopenfilename()    
        path=os.path.normpath(slash)                      
                              
        img=myImage(path)
        self.myLogicObject.Data.append(img)
        print(self.myLogicObject.Data)


    def UPloadData_Drag_Drop(self):
        pass



    def finish_upload(self):
        self.myLogicObject.Data = self.myLogicObject.cash_Data.copy()
        self.myLogicObject.cash_Data.clear()
        print(self.myLogicObject.Data)

        self.image_box.setHidden(False)
        self.UploadData_showimg()
    

    def UploadData_showimg(self):
        
        if(len(self.myLogicObject.Data)==1):
            self.im1.setHidden(False)

        elif(len(self.myLogicObject.Data)==2):
            self.im1.setHidden(False)
            self.im2.setHidden(False)

        elif(len(self.myLogicObject.Data)==3):
            self.im1.setHidden(False)
            self.im2.setHidden(False)
            self.im3.setHidden(False)

        elif(len(self.myLogicObject.Data)==4):
            self.im1.setHidden(False)
            self.im2.setHidden(False)
            self.im3.setHidden(False)
            self.im4.setHidden(False)

        elif(len(self.myLogicObject.Data)>=5):
            self.im1.setHidden(False)
            self.im2.setHidden(False)
            self.im3.setHidden(False)
            self.im4.setHidden(False)
            self.im5.setHidden(False)
       
        
        
    


class myImage:
   
    def __init__(self,path):
        self.detection_obj=[]
        self.path=path
        img = cv2.imread(self.path)


    
     

         