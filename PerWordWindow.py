from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import dialog_ui

class PerWordDisplay(QDialog, dialog_ui.Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)










app = QApplication(sys.argv)


newDict = PerWordDisplay()
newDict.show()
app.exec_()
