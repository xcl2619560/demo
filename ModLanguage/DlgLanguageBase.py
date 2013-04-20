__all__ = ['DlgLanguageBase']
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
class DlgLanguageBase(QDialog):
    def __init__(self, parent=None):
        super(DlgLanguageBase, self).__init__(parent)
        self.label = QT_TRANSLATE_NOOP("DlgLanguageBase","hello World")
        