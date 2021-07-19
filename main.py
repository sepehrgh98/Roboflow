import sys
from PyQt5.QtWidgets import QApplication
from Graphic import MainGUI
from logic import RoboflowLogic


myLogicObject = RoboflowLogic("chess", "piece")
myLogicObject.Test_Train_data(0.75,0.2,0.05)

app = QApplication(sys.argv)
w = MainGUI()
w.show()
sys.exit(app.exec_())