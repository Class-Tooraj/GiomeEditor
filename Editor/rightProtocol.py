__author__ = "Tooraj_Jahangiri"
__email__ = "toorajjahangiri@gmail.com"


from PySide6.QtCore import Signal
from PySide6.QtUiTools import loadUiType
from os import path as ipath
from typing import Callable

import time

# IMPORT FUNCTION
from eFunc import talk
from eFunc import hshTrans

UI_RightWidget, Baseclass = loadUiType(ipath.join(ipath.dirname(__file__), "widget_ui/ui_right.ui"))
print(f"{UI_RightWidget= }\n{Baseclass= }")


class RightWidget(Baseclass, UI_RightWidget):
    STATUS = Signal(tuple)

    def __init__(self, *args, **kwargs):
        self.startTime = time.monotonic()
        super(RightWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.btn_tools.setVisible(False)
        self.WIDGET: object = None
        self.STATUS.connect(self.__handler)
        self.btn_exit.clicked.connect(self.wExit)
        self.btn_tools.clicked.connect(self.wTool)
        self.wName: str = None
        self.WID: str = None
    
    def __handler(self, data: tuple):
        if data[0] == '<SET>':
            self.widgets(*data[1:])
        
        elif data[0] == '<START>':
            print(f"[WIDGET_ACTIVE]",*data[1:])
        
        elif data[0] == '<EXIT>':
            tEx = data[1]
            toTime = tEx - self.startTime
            #print(f"<Time>[{toTime}]", *data[2:])
            self.WIDGET.exitSignal()
        
        else:
            print(data)
            pass
    
    def widgets(self, name: str, widget: Callable, wight: int, hight: int):
        self.resize(wight, hight)
        self.lbl_name.setText(name)
        self.WIDGET = widget()
        self.lyt_center.addWidget(self.WIDGET)
        self.WID = hshTrans(f"{hash(self.WIDGET)}")
        self.STATUS.emit(talk('<START>',self.startTime, name, self.WID, True))
        self.WIDGET.startSignal()
        self.wName = name
        self.WIDGET.STATUS.connect(lambda *x: self.STATUS.emit(talk(*x)))
    
    def uWidget(self, name: str, widget_cls: Callable, size: tuple = (250, 70)):
        self.STATUS.emit(talk("<SET>", name, widget_cls, *size))
    
    def wExit(self):
        self.STATUS.emit(talk("<EXIT>", time.monotonic(), self.wName, self.WID, False))
        return 0
    
    # issue: wTool method action active
    def wTool(self, *arg):
        del (arg)
        print("NOT ACTIVE NOW")


# test In develop Now 
"""
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from findmain import FindWidget
    import sys

    app = QApplication(sys.argv)
    win = RightWidget()
    win.uWidget('Search',FindWidget)
    win.show()
    sys.exit(app.exec_())
"""
