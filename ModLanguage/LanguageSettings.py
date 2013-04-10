__all__=['LanguageSettings']

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os

class LanguageSettings(QObject):
    __slots__ = ["lang",]
    en_US = "en_US"
    zh_CN = "zh_CN"

    def __init__(self, lang="en_US"):
        self.lang = lang
        self.qSettings = QSettings("./QLanguageDemo.ini", QSettings.IniFormat)

    def setLanguage(self, lang):
        self.lang = lang
        if lang not in [self.en_US, self.zh_CN]:
            return
        self.qSettings.setValue("Language", self.lang)
        #print "%%%%%%%%%%%%  self.qSettings =",self.qSettings.fileName()

    def languageIsSetting(self):
        return self.qSettings.contains("Language")

    def getLanguage(self):
        language = self.qSettings.value("Language", self.lang).toString()
        return language


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = LanguageSettings()
    print "######### qSettings =",a.qSettings.fileName()
    #a.setLanguage("zh_CN")
    value = a.languageIsSetting()
    print "&&&&&& value =",value
    app.exec_()