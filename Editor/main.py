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
from PySide6.QtPrintSupport import QPrintPreviewDialog
from PySide6.QtUiTools import loadUiType

from typing import Callable

# IMPORT WIDGETS
from findmain import FindWidget
from rightProtocol import RightWidget

# IMPORT FUNCTION
import eFunc

# IMPORT UI FILE
UI_MainWindow, Baseclass = loadUiType(os.path.join(os.path.dirname(__file__), "widget_ui/ui_main.ui"))
print(f"{UI_MainWindow= }\n{Baseclass= }")

class MainWindow(Baseclass, UI_MainWindow):
    SIGNAL_PATH = QtCore.Signal(tuple)        # (FilePath, FileFormat)
    SIGNAL_STATUS = QtCore.Signal(tuple)      # (ActionName, *other)
    RW_STATUS = QtCore.Signal(tuple)          # Right Widget Status Signal
    BT_STATUS = QtCore.Signal(tuple)          # Bottom Widget Status Signal
    WORKING_FILE = None
    _RUNTIME = {'FindW': False}
    SigExeMap = {'PATH': [], 'STATUS': []}
    ActiveWidget = {'Right': {}, 'Bottom': {}}

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        ## UPDATE SIGNAL BACKEND BASE MAP
        ########################################################################
        self.SigExeMap['PATH'].append(self.fileNameChange)
        self.SigExeMap['STATUS'].append(lambda *x: f"[STATUS]{x}")

        self.setupUi(self)
        ## ACTIONS BTN CONNECT
        ########################################################################
        self.btn_save.clicked.connect(self.actionSave)
        self.btn_copy.clicked.connect(self.actionCopy)
        self.btn_cut.clicked.connect(self.actionCut)
        self.btn_undo.clicked.connect(self.actionUndo)
        self.btn_redo.clicked.connect(self.actionRedo)
        self.btn_find.clicked.connect(self.actionFind)
        self.btn_zoomIn.clicked.connect(self.actionZoomIN)
        self.btn_zoomOut.clicked.connect(self.actionZoomOUT)
        self.btn_print.clicked.connect(self.actionPrint)

        ## Boutton Connect
        ########################################################################
        self.Btn_Toggle.clicked.connect(lambda: self.toggleMenu(250, True))   # TOGGLE/BURGUER MENU
        self.btn_new.clicked.connect(self.actionNew)                          # Boutton NEW
        self.btn_open.clicked.connect(self.actionOpen)                        # Boutton OPEN
        self.btn_save_as.clicked.connect(self.actionSaveAs)                   # Boutton SAVE AS
        self.btn_editor.clicked.connect(self.actionEditor)                    # Boutton EDITOR
        self.btn_setting.clicked.connect(self.actionSetting)                  # Boutton SETTING

        # RIGHT & BOTTOM WIDGET AREA PROTOCOL
        self.__RightSpacerAdd = True if len(self.ActiveWidget['Right']) < 1 else False

        # SIGNAL CONNECT
        self.SIGNAL_PATH.connect(lambda x : self.baseSignalHandler('PATH', x))
        self.SIGNAL_STATUS.connect(lambda x : self.baseSignalHandler('STATUS', x))

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

    def addActionBaseSignal(self, sigName: str, *act: Callable):
        try:
            self.SigExeMap[sigName].append(act)
        except KeyError as err:
            print(f"[ADD-ACTION-BASE-SIGNAL][{sigName}][{act}]|[ERROR][{err}]", file=sys.stderr, flush=True)
            self.SigExeMap[sigName] = [*act]
            print(f"[ADD-ACTION-BASE-SIGNAL][{sigName}][{act}][ADD-NEW-SIGNAME]", file=sys.stdout, flush=True)


    def baseSignalHandler(self, signalName: str, data: tuple):
        sps = f"[SIGNAL-NAME][{signalName}]:[DATA][{data}]"     # signal pattern show
        print(sps, file=sys.stdout, flush=True)
        try:
            FunMp = self.SigExeMap[signalName]
            for fun in FunMp:
                res = fun(data)
                print(f"{sps}[ACTION][{fun.__name__}]|[HNDLR-RESULT][{res}]", file=sys.stdout, flush=True)
        except KeyError as err:
            print(f"{sps}|[ERROR][{err}]", file=sys.stderr, flush=True)

    def fileNameChange(self, name: tuple = None):
        default = "NewFile"
        if name is None:
            self.lbl_fileName.setText(f"File :  {default}")
        else:
            self.lbl_fileName.setText(f"File :  {name[0]}")

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
        self.lbl_namePage.setText("Setting")

    def actionEditor(self):
        # action ShortCut Ctrl + E
        self.stackedWidget.setCurrentWidget(self.page_editor)
        self.SIGNAL_STATUS.emit(eFunc.talk("Editor", "Focus"))              # Signal Status
        self.lbl_namePage.setText("Editor")
    
    def actionSave(self):
        # action ShortCut Ctrl + S
        if self.WORKING_FILE is not None:
            with open(self.WORKING_FILE, 'wb') as fs:
                txt = self.textEdit.toPlainText().encode('utf-8')
                counter = fs.write(txt)
            fs.close
            self.SIGNAL_STATUS.emit(eFunc.talk("Save", f"{counter}", f"{self.WORKING_FILE}"))    # Signal Status
        
        elif self.WORKING_FILE is None and self.textEdit.toPlainText() != "":
             self.actionSaveAs()
        else:
            self.SIGNAL_STATUS.emit(eFunc.talk("Save", "None", f"{self.WORKING_FILE}"))    # Signal Status

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
    
    def actionZoomIN(self):
        # action ShortCut Ctrl + +
        tmp = self.textEdit.zoomIn()
        self.SIGNAL_STATUS.emit(eFunc.talk("Zoom_IN", f"{tmp}"))      # Signal Status

    def actionZoomOUT(self):
        # action ShortCut Ctrl + -
        tmp = self.textEdit.zoomOut()
        self.SIGNAL_STATUS.emit(eFunc.talk("Zoom_OUT", f"{tmp}"))      # Signal Status
    
    def actionPrint(self):
        # action ShortCut Ctrl + P
        preview = QPrintPreviewDialog()
        preview.paintRequested.connect(self.textEdit.print_)
        preview.exec_()
        self.SIGNAL_STATUS.emit(eFunc.talk("Print_Preview", f"{preview}")) # Signal Status
    
    # issue: Fix Position , Fix Signal , Fix bug
    def rightWidget(self, name:str ,widget: Callable, size:tuple = (300, 80)):
        RW = RightWidget()
        RW.uWidget(name, widget, size)
        self.ActiveWidget['Right'][name] = True
        self.lyt_eRight.addWidget(RW)
        RW.STATUS.connect(lambda x: self.RW_STATUS.emit(eFunc.talk(*x)))
        if self.__RightSpacerAdd and len(self.ActiveWidget['Right'].values()) is 1:
            self.lyt_eRight.addSpacing(1 * 1080)
            self.__RightSpacerAdd = False
    
    def bottomWidget(self, widget: Callable):
        ...

    # issue: Find Widget Ui need to be fix
    def actionFind(self, t: str = "Tooraj", CaseSensitively: bool = False):
        # action ShortCut Ctrl + F
        wFind = self.rightWidget("Search", FindWidget)
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

