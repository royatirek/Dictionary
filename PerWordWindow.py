from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

import dialog_ui
import win32com.client as wincl
from googletrans import Translator



class PerWordDisplay(QDialog, dialog_ui.Ui_Dialog):
    def __init__(self, word, searchShortDefn, mnemonics, defArr, defDict):
        QDialog.__init__(self)
        self.setupUi(self)

        # adding attributes to the object
        self._word = word
        self._searchShortDefn=searchShortDefn
        self._mnemonics = mnemonics
        self._defArr = str(defArr)
        self._defDict = str(defDict)
        self.setMainWord()
        self.voice.clicked.connect(self.speakMainWord)

        self.setTextArea()

    def setMainWord(self):
        self.setWindowTitle(self._word)
        self.mainWord.setText(self._word)


    def speakMainWord(self):
        speak = wincl.Dispatch("SAPI.SpVoice")
        print(type(self.voice))
        speak.Speak(self._word)

    def translate(self):
        translate=Translator()
        translate.translate(self._word, dest="hi",src="en")

    def setTextArea(self):
        self.textEdit.setHtml(self._defArr)






#app = QApplication(sys.argv)



#perWordObject = PerWordDisplay("hello", "self.query.value(2)","self.query.value(3)",
                                       #"self.query.value(4)", "self.query.value(5)")



#perWordObject.show()
#app.exec_()


