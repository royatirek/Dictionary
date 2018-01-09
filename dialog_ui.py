# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\dialog_ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(481, 577)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/mw3.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.mainWord = QtGui.QLineEdit(Dialog)
        self.mainWord.setGeometry(QtCore.QRect(10, 20, 351, 41))
        self.mainWord.setStyleSheet(_fromUtf8("font: 16pt \"MS Shell Dlg 2\";"))
        self.mainWord.setReadOnly(True)
        self.mainWord.setObjectName(_fromUtf8("mainWord"))
        self.hindi = QtGui.QLineEdit(Dialog)
        self.hindi.setGeometry(QtCore.QRect(10, 70, 351, 41))
        self.hindi.setStyleSheet(_fromUtf8("font: 16pt \"Mangal\";\n"
""))
        self.hindi.setReadOnly(True)
        self.hindi.setObjectName(_fromUtf8("hindi"))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(10, 10, 461, 111))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.voice = QtGui.QPushButton(self.frame)
        self.voice.setGeometry(QtCore.QRect(394, 10, 41, 41))
        self.voice.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/v2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.voice.setIcon(icon1)
        self.voice.setIconSize(QtCore.QSize(32, 32))
        self.voice.setObjectName(_fromUtf8("voice"))
        self.frame_2 = QtGui.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(9, 140, 461, 421))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.textEdit = QtGui.QTextEdit(self.frame_2)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 461, 421))
        self.textEdit.setStyleSheet(_fromUtf8("font: 10pt \"MS Shell Dlg 2\";"))
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.mainWord.setText(_translate("Dialog", "DemoWord", None))
        self.hindi.setText(_translate("Dialog", "HindiWord", None))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>", None))

import icons_rc
