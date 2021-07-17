from PyQt5.QtWidgets import QMainWindow
import os
from PyQt5 import uic
from logic import RoboflowLogic

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
        self.UploadDataBTN.clicked.connect(self.UPloadData)
        self.myLogicObject = RoboflowLogic("chess", "piece")

    def UPloadData(self):
       
        Tk().withdraw()                              #to hide the window behind the selector screen
        slash = tkinter.filedialog.askdirectory()    #swlwct file dialog
        os.path.normpath(slash)                      # / --> //
        path=glob.glob(slash+"/*")                    #  read multiple images address    
        for i in path:
            img=myImage(i)
            self.data.append(img)
         


class myImage:
   
    def __init__(self,path):
        self.detection_obj=[]
        self.path=path
        img = cv2.imread(self.path)


    
     

         