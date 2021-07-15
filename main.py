import sys
from PyQt5.QtWidgets import QApplication
from Graphic import MainGUI


app = QApplication(sys.argv)
w = MainGUI()
w.show()
sys.exit(app.exec_())