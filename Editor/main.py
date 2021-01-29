#!user/bin/env python3


__author__ = "Tooraj_Jahangiri"
__email__ = "toorajjahangiri@gmail.com"

# GUI SOURCE :: 'WANDERSON M.PIMENTA' Made With QtDesigner and PySide2 - PROJECT VERSION 1.0.0 -
# Converted to PySide6

import sys
import os

from PySide6 import QtCore
from PySide6.QtGui import QTextDocument
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtUiTools import loadUiType

# IMPORT FUNCTION
import eFunc

# IMPORT UI FILE
UI_MainWindow, Baseclass = loadUiType(os.path.join(os.path.dirname(__file__), "widget_ui/ui_main.ui"))
print(f"{UI_MainWindow= }\n{Baseclass= }")

class MainWindow(Baseclass, UI_MainWindow):
    SIGNAL_PATH = QtCore.Signal(tuple)        # (FilePath, FileFormat)
    SIGNAL_STATUS = QtCore.Signal(tuple)      # (ActionName, *other)
    WORKING_FILE = None

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        ## ACTIONS BTN CONNECT
        ########################################################################
        self.btn_save.clicked.connect(self.actionSave)
        self.btn_copy.clicked.connect(self.actionCopy)
        self.btn_cut.clicked.connect(self.actionCut)
        self.btn_undo.clicked.connect(self.actionUndo)
        self.btn_redo.clicked.connect(self.actionRedo)
        self.btn_find.clicked.connect(self.actionFind)

        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.Btn_Toggle.clicked.connect(lambda: self.toggleMenu(250, True))

        ## PAGES
        ########################################################################

        # PAGE NEW
        self.btn_new.clicked.connect(self.actionNew)

        # PAGE OPEN
        self.btn_open.clicked.connect(self.actionOpen)

        # PAGE SAVE AS
        self.btn_save_as.clicked.connect(self.actionSaveAs)

        # PAGE EDITOR
        self.btn_editor.clicked.connect(self.actionEditor)

        # PAGE SETTING
        self.btn_setting.clicked.connect(self.actionSetting)

        # SIGNAL CONNECT
        self.SIGNAL_PATH.connect(lambda x: print(x, file=sys.stdout))
        self.SIGNAL_STATUS.connect(lambda x: print(x, file=sys.stdout))

        ## SHOW ==> MAIN WINDOW >> Show in Start app ui
        ########################################################################
        ## ==> END ##
   
    def menu_visible(self, show: bool = True):
        names = lambda x: f"{'  ':2}{x:6}"
        if show is True:
            self.btn_new.setText(names('New'))
            self.btn_open.setText(names('Open'))
            self.btn_save_as.setText(names('Save'))
            self.btn_editor.setText(names('Editor'))
            self.btn_setting.setText(names('Setting'))
        else:
            self.btn_new.setText("")
            self.btn_open.setText("")
            self.btn_save_as.setText("")
            self.btn_editor.setText("")
            self.btn_setting.setText("")

    def toggleMenu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.frame_left_menu.width()
            maxExtend = 150
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                self.menu_visible(True)
                widthExtended = maxExtend
            else:
                self.menu_visible(False)
                widthExtended = standard
                

            # ANIMATION
            self.animation = QtCore.QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def actionNew(self):
        # action ShortCut Ctrl + N
        self.actionSave()
        self.textEdit.clear()
        self.SIGNAL_STATUS.emit(eFunc.talk("New"))               # Signal Status
    
    def actionOpen(self):
        # action ShortCut Ctrl + O
        _formats = eFunc.fileFormat()
        file_name = QFileDialog.getOpenFileName(filter=_formats)
        if file_name != ('', ''):
            self.SIGNAL_STATUS.emit(eFunc.talk("Open", "True"))  # Signal Status
            self.actionNew()

            with open(file_name[0], 'rb') as f_op:
                reader = f_op.read()
            reader = reader.decode("utf-8")
            
            self.textEdit.setText(reader)
            self.SIGNAL_PATH.emit(eFunc.talk(*file_name))
            self.WORKING_FILE = file_name[0]
            del reader
        
        else:
            self.SIGNAL_STATUS.emit(eFunc.talk("Open", "False")) # Signal Status
    
    def actionSaveAs(self):
        # action ShortCut Ctrl + Shift + S
        _formats = eFunc.fileFormat()
        file_name = QFileDialog.getSaveFileName(filter=_formats)
        if file_name != ('', ''):
            self.SIGNAL_PATH.emit(eFunc.talk(*file_name))
                
            with open(file_name[0], 'wb') as fs:
                txt = self.textEdit.toPlainText().encode('utf-8')
                counter = fs.write(txt)
            fs.close
            self.SIGNAL_STATUS.emit(eFunc.talk("SaveAs", f"{counter}", f"{self.WORKING_FILE}"))   # Signal Status
            self.WORKING_FILE = file_name[0]
            del txt, counter
            
        else:
            self.SIGNAL_STATUS.emit(eFunc.talk("SaveAs", "False", "None"))  # Signal Status
    
    def actionSetting(self):
        # action ShortCut None
        self.stackedWidget.setCurrentWidget(self.page_setting)
        self.SIGNAL_STATUS.emit(eFunc.talk("Setting", "Focus"))             # Signal Status

    def actionEditor(self):
        # action ShortCut Ctrl + E
        self.stackedWidget.setCurrentWidget(self.page_editor)
        self.SIGNAL_STATUS.emit(eFunc.talk("Editor", "Focus"))              # Signal Status
    
    def actionSave(self):
        # action ShortCut Ctrl + S
        if self.WORKING_FILE is None:
            self.actionSaveAs()
        else:
            with open(self.WORKING_FILE, 'wb') as fs:
                txt = self.textEdit.toPlainText().encode('utf-8')
                counter = fs.write(txt)
            fs.close
            self.SIGNAL_STATUS.emit(eFunc.talk("Save", f"{counter}", f"{self.WORKING_FILE}"))    # Signal Status

    def actionCopy(self):
        # action ShortCut Ctrl + C
        tmp = self.textEdit.copy()
        self.SIGNAL_STATUS.emit(eFunc.talk("Copy", f"{tmp}"))      # Signal Status
    
    def actionCut(self):
        # action ShortCut Ctrl + X
        tmp = self.textEdit.cut()
        self.SIGNAL_STATUS.emit(eFunc.talk("Cut", f"{tmp}"))      # Signal Status

    def actionUndo(self):
        # action ShortCut Ctrl + Z
        tmp = self.textEdit.undo()
        self.SIGNAL_STATUS.emit(eFunc.talk("Undo", f"{tmp}"))      # Signal Status
    
    def actionRedo(self):
        # action ShortCut Ctrl + Shift + Z
        tmp = self.textEdit.redo()
        self.SIGNAL_STATUS.emit(eFunc.talk("Redo", f"{tmp}"))      # Signal Status

    def actionFind(self, t: str = "Tooraj", CaseSensitively: bool = False):
        # action ShortCut Ctrl + F
        if CaseSensitively:
            tmp = self.textEdit.find(t, QTextDocument.FindCaseSensitively)
            self.SIGNAL_STATUS.emit(eFunc.talk("Find", f"{tmp}", f"{CaseSensitively}"))      # Signal Status
        else:
            tmp = self.textEdit.find(t)
            self.SIGNAL_STATUS.emit(eFunc.talk("Find", f"{tmp}", f"{CaseSensitively}"))      # Signal Status


if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

