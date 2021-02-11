__author__ = "Tooraj_Jahangiri"
__email__ = "toorajjahangiri@gmail.com"


from PySide6.QtCore import Signal
from PySide6.QtUiTools import loadUiType
from os import path as ipath

# IMPORT FUNCTION
from eFunc import talk
from eFunc import hshTrans

UI_RightWidget, Baseclass = loadUiType(ipath.join(ipath.dirname(__file__), "widget_ui/ui_right.ui"))
print(f"{UI_RightWidget= }\n{Baseclass= }")


class RightWidget(Baseclass, UI_RightWidget):
    STATUS = Signal(tuple)  # (actName, reserve)

    def __init__(self, *args, **kwargs):
        super(RightWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.STATUS.connect(self.__handler)
        self.btn_exit.clicked.connect(self.wExit)
        self.btn_tools.clicked.connect(self.wTool)
        self.wName: str = None
    
    def __handler(self, data: tuple):
        if data[0] == 'NEW':
            self.widgets(*data[1:])
        else:
            print(data)
            pass
    
    def widgets(self, name: str, widget):
        self.lbl_name.setText(name)
        w = widget()
        self.lyt_center.addWidget(w)
        self.STATUS.emit(talk(f"{hash(w)}", "ADD", True))
        self.wName = f"{name}"
        print(name)
    
    def uWidget(self, name: str, widget_cls):
        self.STATUS.emit(talk("NEW", name, widget_cls))
    
    # need to work ...
    def wExit(self):
        self.STATUS.emit(talk("Exit", self.wName, False))
        exit(self)
    
    def wTool(self):
        ...

"""
# test In develop Now 

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