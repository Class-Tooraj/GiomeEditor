__author__ = "Tooraj_Jahangiri"
__email__ = "toorajjahangiri@gmail.com"

from os import path as ipath

from PySide6.QtCore import Signal, Slot
from PySide6.QtUiTools import loadUiType

# IMPORT UI FILE
UI_MainWindow, Baseclass = loadUiType(ipath.join(ipath.dirname(__file__), "widget_ui/findWidget.ui"))
__file_name = ipath.basename(__file__)
print(f"{__file_name= }\n\t/{UI_MainWindow= }/\n\t/{Baseclass= }/")


class FindWidget(Baseclass, UI_MainWindow):

    STATUS = Signal(tuple)      # ("msg", bool)

    def __init__(self, *args, **kwargs):
        super(FindWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.msgStatus("")
        # Action Button Connect
        self.btn_find.clicked.connect(self.actFind)
        # Signal Connect
        self.STATUS.connect(self.sigStatusHandle)

    def actFind(self):
        getTxt = self.lineEdit.text()
        self.msgStatus("")
        if getTxt != "":
            if self.rbtn_case.isChecked():
                self.STATUS.emit(self.sendSignal("<SEARCH>", getTxt, True))
            else:
                self.STATUS.emit(self.sendSignal("<SEARCH>", getTxt, False))

    def sigStatusHandle(self, sig: tuple):
        com, *var = sig
        ignore = ('<START>', '<EXIT>', '<SEARCH>')
        if com not in ignore:
            if com == 'msg':
                self.msgStatus(var)
            elif com == 'cls':
                self.clearStatus()
            elif com == '/ST':
                self.STATUS.emit(self.sendSignal('<START>', True))
            elif com == '/EX':
                self.STATUS.emit(self.sendSignal('<EXIT>', False))
            else:
                self.lineEdit.setText("")
        else:
            print(f"[STATUS_FIND] {com} {var}")

    def msgStatus(self, msg: str):
        self.lbl_status.setText(msg)
    
    def clearStatus(self):
        self.lbl_status.setText("")

    @ Slot(tuple)
    @ staticmethod
    def sendSignal(*args) -> tuple:
        return args
    
    def exitSignal(self):
        self.sigStatusHandle(('/EX', False))
        del self
        return 0
    
    def startSignal(self):
        self.sigStatusHandle(('/ST', True))
        self.show()
        return 1

# test
"""
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    try:
        app = QApplication(sys.argv)
        win = FindWidget()
        #win.show()
        win.startSignal()
        sys.exit(app.exec_())
    except BaseException as e:
        raise e
    finally:
        exit(win.exitSignal())
"""