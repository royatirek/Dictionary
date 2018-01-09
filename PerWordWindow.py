from PyQt4.QtGui import *
import dialog_ui
import win32com.client as wincl
from googletrans import Translator



class PerWordDisplay(QDialog, dialog_ui.Ui_Dialog):
    """ This is the class to create the dialog view"""
    def __init__(self, word, searchShortDefn, mnemonics, defArr, syn, hindi):
        QDialog.__init__(self)
        self.setupUi(self)

        # adding attributes to the object
        self._word = word
        self._searchShortDefn=searchShortDefn
        self._mnemonics = mnemonics
        # defArr is the defString created in the Dictionary class of execute.py file
        self._defArr = str(defArr)
        self._syn = str(syn)
        self._hindi=hindi
        self.setMainWord()
        self.voice.clicked.connect(self.speakMainWord)
        self.setHindiWord()
        self.setTextArea()

    def setMainWord(self):
        """ It sets the main word that is clicked and the title of the dialog"""
        self.setWindowTitle(self._word)
        self.mainWord.setText(self._word)

    def setHindiWord(self):
        """ It sets the Hindi translation of the main word"""
        self.hindi.setText(self._hindi)


    def speakMainWord(self):
        """ It uses the win32com module to get the pronunciation of the word"""
        speak = wincl.Dispatch("SAPI.SpVoice")
        print(type(self.voice))
        speak.Speak(self._word)

    def translate(self):
        """ This feature is to translate words into more regional languages using googletrans module and has not been build"""
        translate=Translator()
        translate.translate(self._word, dest="hi",src="en")

    def setTextArea(self):
        """ It sets details of the main word"""
        self.textEdit.setHtml(self._defArr)
        print(self._syn)







