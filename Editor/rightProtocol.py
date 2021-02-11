__author__ = "Tooraj_Jahangiri"
__email__ = "toorajjahangiri@gmail.com"


from PySide6.QtCore import Signal
from PySide6.QtUiTools import loadUiType
from os import path as ipath

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
        if data[0] == 'Set':
            self.widgets(*data[1:])
        
        elif data[0] == "Start":
            print(*data[1:])
        
        elif data[0] == 'Exit':
            tEx = data[1]
            toTime = tEx - self.startTime
            print(f"Time[{toTime}]", *data[2:])
            exit(self)
        
        else:
            print(data)
            pass
    
    def widgets(self, name: str, widget):
        self.lbl_name.setText(name)
        self.WIDGET = widget()
        self.lyt_center.addWidget(self.WIDGET)
        self.WID = hshTrans(f"{hash(self.WIDGET)}")
        self.STATUS.emit(talk("Start",self.startTime, name, self.WID, True))
        self.wName = name
    
    def uWidget(self, name: str, widget_cls):
        self.STATUS.emit(talk("Set", name, widget_cls))
    
    def wExit(self):
        self.STATUS.emit(talk("Exit", time.monotonic(), self.wName, self.WID, False))
    
    # issue: wTool method action active
    def wTool(self, *arg):
        del (arg)
        print("NOT ACTIVE NOW")


# test In develop Now 
'''
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from findmain import FindWidget
    import sys

    app = QApplication(sys.argv)
    win = RightWidget()
    win.uWidget('Search',FindWidget)
    win.show()
    sys.exit(app.exec_())

'''