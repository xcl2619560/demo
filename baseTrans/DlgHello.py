from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
import sys
from DlgHelloBase import DlgHelloBase

class DlgHello(DlgHelloBase):
    def tr(self, s):
        return QApplication.translate('DlgHello', s)
    def __init__(self):
        #super(DlgHello, self).__init__(parent)
        DlgHelloBase.__init__(self)
        self.createMain()

    def createMain(self):
        self.lbHello = QLabel(self.tr('Hello china'))
        hBox = QHBoxLayout()
        hBox.addWidget(self.lbHello)
        self.setLayout(hBox)
        self.setWindowTitle(self.title)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    a = translator.load("hello_zh_CN.qm")
    print "&&&& a =",a
    app.installTranslator(translator)
    dlg = DlgHello()
    dlg.show()
    app.exec_()
