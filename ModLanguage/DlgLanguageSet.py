__all__ = ['DlgLanguageSet']

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from LanguageSettings import LanguageSettings
import sys
import os

class DlgLanguageSet(QDialog):
    en_US = LanguageSettings.en_US
    zh_CN = LanguageSettings.zh_CN

    def __init__(self, parent=None):
        super(DlgLanguageSet, self).__init__(parent)
        tr = self.tr

        GrpBoxLang = QGroupBox("Language")
        lbLangSelect = QLabel(tr("Please select your preferred language,<br><b>Note:</b> this will only take effect after you restart pyCREME. "))

        self.cbLangSelect = QComboBox()
        self.cbLangSelect.insertItem(0, tr("English"), self.en_US)
        self.cbLangSelect.insertItem(1, tr("Simplified Chinese"), self.zh_CN)
        self.cbLangSelect.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.btOk = QDialogButtonBox(QDialogButtonBox.Ok)

        hLayout = QHBoxLayout()
        hLayout.addStretch(1)
        hLayout.addWidget(self.cbLangSelect)

        vLayout = QVBoxLayout()
        vLayout.addWidget(lbLangSelect)
        vLayout.addLayout(hLayout)

        GrpBoxLang.setLayout(vLayout)

        mainLayout = QGridLayout()
        mainLayout.addWidget(GrpBoxLang)
        mainLayout.addWidget(self.btOk)
        self.setLayout(mainLayout)

        self.connect(self.btOk, SIGNAL("accepted()"), self.setInstallLanguage)
        self.settings = LanguageSettings(self.en_US)

    def setInstallLanguage(self):
        index = self.cbLangSelect.currentIndex()
        if 0 == index:
            self.settings.setLanguage(self.en_US)
        elif 1 == index:
            self.settings.setLanguage(self.zh_CN)
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #translator = QTranslator()
    #a = translator.load("weibull_CN.qm")
    #app.installTranslator(translator)
    dlg = DlgLanguageSet()
    dlg.show()
    app.exec_()