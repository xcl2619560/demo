__all__ = ['DlgHelloBase']

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os

#def tr(context, text):
    #print '&&&&&&&&&&&  6666666'
    #return QApplication.translate(context, text, None,
                                        #QApplication.UnicodeUTF8)
class DlgHelloBase(QDialog):
    tr = lambda _, s: QApplication.translate('DlgHelloBase', s)
    #def tr(self, s):
        #return QApplication.translate('DlgHelloBase', s)

    def __init__(self, parent=None):
        super(DlgHelloBase, self).__init__(parent)

        #tr = lambda s: QApplication.translate("DlgHelloBase", s)
        #self.qtr = lambda s: QApplication.translate('DlgHelloBase', s)

        self.title = self.tr('china')
        #self.title = self.trUtf8('china')

        #self.title = tr('DlgHelloBase',u'china')

        #print "&&&&&&&& title =", self.title


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    a = translator.load("hello_zh_CN.qm")
    print "&&&& a =",a
    app.installTranslator(translator)
    dlg = DlgHelloBase()
    dlg.show()
    app.exec_()