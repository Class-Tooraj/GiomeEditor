#!user/bin/env python3


__author__ = "Tooraj_Jahangiri"
__email__ = "toorajjahangiri@gmail.com"

# GUI SOURCE :: 'WANDERSON M.PIMENTA' Made With QtDesigner and PySide2 - PROJECT VERSION 1.0.0 -
# Converted to PySide6

import sys
import os

from PySide6 import QtCore
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import *


# IMPORT UI FILE
UI_MainWindow, Baseclass = loadUiType(os.path.join(os.path.dirname(__file__), "widget_ui/ui_main.ui"))
print(f"{UI_MainWindow= }\n{Baseclass= }")

class MainWindow(Baseclass, UI_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

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
            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def actionNew(self):
        # action ShortCut Ctrl + N
        self.stackedWidget.setCurrentWidget(self.page_new)
    
    def actionOpen(self):
        self.stackedWidget.setCurrentWidget(self.page_open)
    
    def actionSave(self):
        # action ShortCut Ctrl + S
        ...
    
    def actionSaveAs(self):
        # action ShortCut Ctrl + Shift + S
        self.stackedWidget.setCurrentWidget(self.page_save_as)
    
    def actionSetting(self):
        # action ShortCut None
        self.stackedWidget.setCurrentWidget(self.page_setting)

    def actionEditor(self):
        # action ShortCut Ctrl + E
        self.stackedWidget.setCurrentWidget(self.page_editor)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

