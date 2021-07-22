import sys
from PyQt5.QtWidgets import QApplication
from Graphic import MainGUI
from logic import RoboflowLogic


myLogicObject = RoboflowLogic("chess", "piece")


app = QApplication(sys.argv)
w = MainGUI()
w.show()
sys.exit(app.exec_())