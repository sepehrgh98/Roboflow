from PyQt5.QtWidgets import QMainWindow
import os
from PyQt5 import uic
from logic import RoboflowLogic


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
        pass
        
