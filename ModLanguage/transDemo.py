from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
from DlgLanguageSet import DlgLanguageSet
from LanguageSettings import LanguageSettings
class DlgDemo(QDialog):
    title = QT_TRANSLATE_NOOP("DlgDemo","demo")
    def __init__(self, parent=None):
        super(DlgDemo, self).__init__(parent)
        self.btlang = QPushButton(self.tr("language"))
        hBox = QHBoxLayout()
        hBox.addWidget(self.btlang)
        self.setLayout(hBox)
        self.setWindowTitle(self.tr(self.title))

        self.connect(self.btlang, SIGNAL("clicked()"), self.slotLang)

    def slotLang(self):
        _dlg = DlgLanguageSet(self)
        _dlg.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    settings = LanguageSettings()
    isSetting = settings.languageIsSetting()
    if not isSetting:
        _dlg = DlgLanguageSet()
        _dlg.exec_()

    lang = settings.getLanguage()
    if QString.compare(lang, LanguageSettings.zh_CN, Qt.CaseInsensitive) == 0:
        translator = QTranslator()
        a = translator.load("transDemo_zh_CN.qm")
        print "&&&& a =",a
        app.installTranslator(translator)
    dlg = DlgDemo()
    dlg.show()
    app.exec_()