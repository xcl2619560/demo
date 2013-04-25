from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
import numpy as np
from MCMCSettings import MCMCSettings
from DlgConvergence import DlgConvergence
from DlgHistogram import DlgHistogram
from DlgCorrelation import DlgCorrelation
from DlgBestFit import DlgBestFit
from MCMCDriver import MCMCDriver
from MCMCHistory import MCMCHistory
from DocEngine import DocEngine

class DlgWeibullMCMC(QDialog):
    facConv = {'K2b':1024,'M2b':pow(1024,2),'T2b':pow(1024,4)}
    nbitUnit = ('bit','Kb','Mb','Tb')
    @classmethod
    def convertNbit(cls, nbit, unit):
        bit, Kb, Mb, Tb = cls.nbitUnit
        if unit == bit:
            cnvtedNsram = nbit
        elif unit == Kb:
            cnvtedNsram = nbit*cls.facConv['K2b']
        elif unit == Mb:
            cnvtedNsram = nbit*cls.facConv['M2b']
        elif unit == Tb:
            cnvtedNsram = nbit*cls.facConv['T2b']
        return cnvtedNsram

    def __init__(self, parent = None):
        super(DlgWeibullMCMC, self).__init__(parent)
        self.msgboxState = False

        def topForm():
            #lay out data group
            dataGroup = QGroupBox()
            dataGroup.setTitle(self.tr('Data'))
            totalVlayout = QVBoxLayout()

            hLayout = QHBoxLayout()
            validate = QIntValidator()
            self.leNbit = QLineEdit()
            self.leNbit.setMaximumWidth(90)
            self.leNbit.setValidator(validate)
            unit = [(self.tr('Mb'),   'Mb' ),
                    (self.tr('bit'),  'bit'),
                    (self.tr('Kb'),   'Kb' ),
                    (self.tr('Tb'),   'Tb' )]
            self.cbUnit = QComboBox()
            self.cbUnit.setMaximumSize(QSize(70, 20))
            for txt,val in unit:
                self.cbUnit.addItem(txt, userData = val)

            lbNbit = QLabel(self.tr("Nbit :"))
            lbNbit.setMaximumWidth(50)
            hLayout.addWidget(lbNbit,      Qt.AlignLeft)
            hLayout.addWidget(self.leNbit, Qt.AlignLeft)
            hLayout.addWidget(self.cbUnit, Qt.AlignLeft)
            hLayout.addStretch(3)
            totalVlayout.addLayout(hLayout)

            hLayout = QHBoxLayout()
            self.tabData = QTableWidget()
            self.tabData.setMinimumSize(350, 250)
            self.tabData.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.tabData.setAlternatingRowColors(True)
            self.tabData.resizeColumnsToContents()
            self.tabData.setColumnCount(3)
            self.tabData.setHorizontalHeaderLabels(['LET' , unichr(0x03A6), 'k'])
            self.tabData.verticalHeader().setResizeMode(QHeaderView.Fixed)
            self.tabData.horizontalHeader().setResizeMode(QHeaderView.Stretch)
            for i in range(3):
                if 0 == i:
                    self.tabData.setColumnWidth(i,70)
                    self.tabData.horizontalHeaderItem(i).setToolTip(self.tr('unit:MeV*cm%1/mg').arg(unichr(0x00B2)))
                elif 1 == i:
                    self.tabData.setColumnWidth(i,160)
                    self.tabData.horizontalHeaderItem(i).setToolTip(self.tr('unit:#/cm%1').arg(unichr(0x00B2)))
                else:
                    self.tabData.setColumnWidth(i,100)
                    self.tabData.horizontalHeaderItem(i).setToolTip(self.tr('unit:bit'))
            hLayout.addWidget(self.tabData)

            vLayout = QVBoxLayout()
            self.btLoad = QPushButton(self.tr("&Load"))
            self.btLoad.setToolTip(self.tr('Import Datas'))
            self.btAdd = QPushButton(self.tr("&Add"))
            self.btAdd.setToolTip(self.tr("Add an empty row to the table"))
            self.btRemv = QPushButton(self.tr("Re&move"))
            self.btRemv.setToolTip(self.tr("Remove selected rows from the table"))
            self.btClear = QPushButton(self.tr("&Clear"))
            self.btClear.setToolTip(self.tr("Clear all datas of the table"))
            vLayout.addWidget(self.btLoad,  0, Qt.AlignLeft)
            vLayout.addWidget(self.btAdd,   0, Qt.AlignLeft)
            vLayout.addWidget(self.btRemv,  0, Qt.AlignLeft)
            vLayout.addWidget(self.btClear, 0, Qt.AlignLeft)
            vLayout.addStretch(2)
            hLayout.addLayout(vLayout)
            totalVlayout.addLayout(hLayout)
            dataGroup.setLayout(totalVlayout)

            #lay out MCMCParams group
            mcmcGroup = QGroupBox()
            mcmcGroup.setTitle(self.tr('MCMCParams'))
            formLayout = QFormLayout()

            self.leNburnin = QLineEdit()
            self.leNkeep   = QLineEdit()
            self.leNskip   = QLineEdit()
            self.leLogstep = QLineEdit()
            self.leFactor  = QLineEdit()
            self.leSeed    = QLineEdit()

            nvalidate = QIntValidator()
            self.leNburnin.setValidator(nvalidate)
            self.leNkeep.setValidator(nvalidate)
            self.leNskip.setValidator(nvalidate)
            self.leSeed.setValidator(nvalidate)

            fvalidate = QDoubleValidator()
            fvalidate.setNotation(QDoubleValidator.StandardNotation|
                                  QDoubleValidator.ScientificNotation)
            self.leLogstep.setValidator(fvalidate)
            self.leFactor.setValidator(fvalidate)

            self.leNburnin.setMaximumWidth(90)
            self.leNkeep.setMaximumWidth(90)
            self.leNskip.setMaximumWidth(90)
            self.leLogstep.setMaximumWidth(90)
            self.leFactor.setMaximumWidth(90)
            self.leSeed.setMaximumWidth(90)

            formLayout.addRow(QLabel(self.tr('Nburn-in :')), self.leNburnin)
            formLayout.addRow(QLabel(self.tr('Nkeep :')),    self.leNkeep  )
            formLayout.addRow(QLabel(self.tr('Nskip :')),    self.leNskip  )
            formLayout.addRow(QLabel(self.tr('logstep :')),  self.leLogstep)
            formLayout.addRow(QLabel(self.tr('factor :')),   self.leFactor )
            formLayout.addRow(QLabel(self.tr('seed :')),     self.leSeed   )
            formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
            formLayout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
            formLayout.setLabelAlignment(Qt.AlignLeft)
            mcmcGroup.setLayout(formLayout)

            return dataGroup, mcmcGroup

        def buttomForm():
            #lay out result group
            totalVlayout = QVBoxLayout()
            resultGroup = QGroupBox()
            resultGroup.setTitle(self.tr('Result'))

            self.btRun = QPushButton(self.tr('&Run'))
            self.btConverg = QPushButton(self.tr('Con&verg'))
            lbAcceptRate = QLabel(self.tr("acceptance rate:"))
            self.leAcceptRate = QLineEdit("")
            self.leAcceptRate.setReadOnly(True)
            self.btHistogram = QPushButton(self.tr("&Histogram"))
            self.btCorrelation = QPushButton(self.tr("C&orrelation"))
            self.btBestFit = QPushButton(self.tr("&BestFit"))
            self.btRun.setMaximumWidth(100)
            self.btConverg.setMaximumWidth(100)
            lbAcceptRate.setMaximumWidth(110)
            self.leAcceptRate.setMaximumWidth(80)
            self.btHistogram.setMaximumWidth(100)
            self.btCorrelation.setMaximumWidth(100)
            self.btBestFit.setMaximumWidth(100)

            self.btConverg.setEnabled(False)
            self.btHistogram.setEnabled(False)
            self.btCorrelation.setEnabled(False)
            self.btBestFit.setEnabled(False)

            hLayout = QHBoxLayout()
            hLayout.addWidget(self.btRun, Qt.AlignLeft)
            hLayout.addWidget(self.btConverg, Qt.AlignLeft)
            hLayout.addWidget(lbAcceptRate, Qt.AlignLeft)
            hLayout.addWidget(self.leAcceptRate, Qt.AlignLeft)
            hLayout.addStretch(1)
            totalVlayout.addLayout(hLayout)

            hLayout = QHBoxLayout()
            hLayout.addWidget(self.btHistogram, Qt.AlignLeft)
            hLayout.addWidget(self.btCorrelation, Qt.AlignLeft)
            hLayout.addWidget(self.btBestFit, Qt.AlignLeft)
            hLayout.addStretch(1)
            totalVlayout.addLayout(hLayout)

            resultGroup.setLayout(totalVlayout)
            return resultGroup

        self.btSave = QPushButton(self.tr("&Save"))
        self.btQuit = QPushButton(self.tr("&Quit"))
        self.btSave.setMaximumWidth(75)
        self.btQuit.setMaximumWidth(75)
        self.btSave.setEnabled(False)

        vlayout = QVBoxLayout()
        dataGroup, mcmcGroup = topForm()
        hlayout = QHBoxLayout()
        hlayout.addWidget(dataGroup,2)
        hlayout.addWidget(mcmcGroup)
        vlayout.addLayout(hlayout, 2)
        vlayout.addWidget(buttomForm())
        hlayout = QHBoxLayout()
        hlayout.addStretch(1)
        hlayout.addWidget(self.btSave, Qt.AlignRight)
        hlayout.addWidget(self.btQuit, Qt.AlignRight)
        vlayout.addLayout(hlayout)

        self.setLayout(vlayout)
        self.setWindowTitle(self.tr('WeibullMCMC'))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setMinimumSize(650, 480)

        self.connect(self.btAdd,         SIGNAL('clicked()'), self.onAddClicked)
        self.connect(self.btRemv,        SIGNAL('clicked()'), self.onRemvClicked)
        self.connect(self.btClear,       SIGNAL('clicked()'), self.onClearClicked)
        self.connect(self.btLoad,        SIGNAL('clicked()'), self.onLoadClicked)
        self.connect(self.btSave,        SIGNAL('clicked()'), self.onSaveClicked)
        self.connect(self.btRun,         SIGNAL('clicked()'), self.onRunClicked)
        self.connect(self.btConverg,     SIGNAL('clicked()'), self.onConvergClicked)
        self.connect(self.btHistogram,   SIGNAL('clicked()'), self.onHistClicked)
        self.connect(self.btCorrelation, SIGNAL('clicked()'), self.onCorrClicked)
        self.connect(self.btBestFit,     SIGNAL('clicked()'), self.onBestFitClicked)
        self.connect(self.btQuit,        SIGNAL('clicked()'), self.reject)

        #set some buttons that used to look up results enable is or not
        self.connect(self,           SIGNAL(  'runStateChanged'  ),  self.setEnableButton  )
        self.connect(self.leNbit,    SIGNAL('textEdited(QString)'),  self.setUnenableButton)
        self.connect(self.leNburnin, SIGNAL('textEdited(QString)'),  self.setUnenableButton)
        self.connect(self.leNkeep,   SIGNAL('textEdited(QString)'),  self.setUnenableButton)
        self.connect(self.leNskip,   SIGNAL('textEdited(QString)'),  self.setUnenableButton)
        self.connect(self.leLogstep, SIGNAL('textEdited(QString)'),  self.setUnenableButton)
        self.connect(self.leFactor,  SIGNAL('textEdited(QString)'),  self.setUnenableButton)
        self.connect(self.leSeed,    SIGNAL('textEdited(QString)'),  self.setUnenableButton)
        self.connect(self.cbUnit,    SIGNAL('currentIndexChanged(int)'),  self.setUnenableButton)
        self.connect(self.tabData,   SIGNAL('cellChanged(int,int)'), self.setUnenableButton)

        #set default settings
        _mcmcSettings = MCMCSettings()
        self.fromData(_mcmcSettings)

    def onLoadClicked(self):
        '''
        :when load-button clicked,the slot function will open the data file
        '''
        homepath = QDir.homePath()
        path = str( QFileDialog.getOpenFileName(self, self.tr("Open File"),\
                                                homepath, self.tr("Data file(*.dat)")) )
        _docEngine = DocEngine(fname=path)
        data = _docEngine.getRecords()
        if not data: return
        self.updateDataTable(data)

    def updateDataTable(self, data):
        '''
        :param  data:[{'let':let,'phi':phi,'k':k}, ...]
        :update the table based on row by using data of data
        '''
        rowCount = len(data)
        for i in range(rowCount):
            if 0 == len(data[i]): return

        self.tabData.clearSpans()
        self.tabData.setUpdatesEnabled(False)
        self.tabData.setRowCount(rowCount)
        for i in range(rowCount):
            self.tabData.setRowHeight(i, 25)
            #params = ['let','phi','k']
            newItem = []
            for j in range(3):
                newItem.append(QTableWidgetItem(""))
                newItem[j].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                newItem[j].setFlags( Qt.ItemIsEnabled| Qt.ItemIsSelectable | Qt.ItemIsEditable)
                txt = data[i][j]
                newItem[j].setText(txt)
                self.tabData.setItem(i, j, newItem[j])
        self.tabData.setUpdatesEnabled(True)

    def onAddClicked(self):
        '''
        :when Add-button clicked,the slot function will add a row including three columns
        '''
        twRow = self.tabData.rowCount()
        self.tabData.setRowCount(twRow+1)
        self.tabData.setRowHeight(twRow, 20)
        for i in range(3):
            newItem = QTableWidgetItem("")
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            newItem.setFlags( Qt.ItemIsEnabled| Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.tabData.setItem(twRow, i, newItem)
            self.tabData.setCurrentItem(newItem, QItemSelectionModel.Clear)

    def onRemvClicked(self):
        '''
        :when Remove-button clicked,the slot function will remove the selected rows
        '''
        select = self.tabData.selectionModel()
        indexlist = select.selectedIndexes()
        if len(indexlist) != 0:
            dic = {}
            rowlist = []
            for index in indexlist:
                dic[index] = index.row()
                if dic[index] not in rowlist:
                    rowlist.append(dic[index])
            rowlist.sort()
            rowlist.reverse()
            for i in range(len(rowlist)):
                self.tabData.removeRow(rowlist[i])

    def onClearClicked(self):
        '''
        :when Clear-button clicked,the slot function will clear all the contents of the table
        '''
        self.tabData.clearContents()

    def onSaveClicked(self):
        '''
        :when Save-button clicked,the slot function will save the data like sigma_sat,let0,lam,k,logp
        '''
        homepath = QDir.homePath()
        nburnin = self._mcmcSettings.nburnin
        nkeep = self._mcmcSettings.nkeep
        path = str( QFileDialog.getSaveFileName(self, self.tr("Save File"),
                                                homepath, self.tr("Data file(*.dat)")) )
        self.mcmcHistory.saveDataFile(fname=path)

    def onRunClicked(self):
        self._mcmcSettings = None
        self.coordinates = []
        self.mcmcHistory =None

        self.leAcceptRate.clear()
        pDict = self.loadData()
        if pDict is not None:
            self._mcmcSettings = MCMCSettings( pDict[ 'data'  ], pDict[ 'nbit' ],
                                               pDict['nburnin'], pDict[ 'nkeep'],
                                               pDict[ 'nskip' ], pDict[ 'seed' ],
                                               pDict['logstep'], pDict['factor'])

            _mcmcDriver = MCMCDriver(self._mcmcSettings)
            if not isinstance(_mcmcDriver, MCMCDriver): raise ValueError

            self.mcmcHistory, self.bestFit, acceptRate = _mcmcDriver.run()

            palette = QPalette()
            if acceptRate >= 0.1 and acceptRate <= 0.4:
                palette.setColor(QPalette.Text,Qt.darkGreen)
            else:
                palette.setColor(QPalette.Text,Qt.red)
            self.leAcceptRate.setPalette(palette)
            self.leAcceptRate.setText(str(acceptRate))

            _convergDlg = DlgConvergence( self.mcmcHistory, self)
            _convergDlg.show()

            self.emit(SIGNAL('runStateChanged'))
        elif False == self.msgboxState:
            msg = self.tr("Sufficient to obtain the required datas or MCMCParams first.")
            QMessageBox.information(self, self.tr('information'), msg)

    def onConvergClicked(self):
        _convergDlg = DlgConvergence(self.mcmcHistory, self)
        _convergDlg.show()

    def onHistClicked(self):
        data = []
        _histDlg = DlgHistogram(self.mcmcHistory, self)
        _histDlg.show()

    def onCorrClicked(self):
        _corrDlg = DlgCorrelation(self.mcmcHistory, self)
        _corrDlg.showFullScreen()

    def onBestFitClicked(self):
        _bestfitDlg = DlgBestFit(self.bestFit, self)
        _bestfitDlg.show()

    def readTableData(self):
        currentRow, rowCnt, colCnt = 0, self.tabData.rowCount(),self.tabData.columnCount()
        tabData = np.zeros((rowCnt, colCnt))
        if rowCnt == 0: return
        emptyRows = []
        while currentRow < rowCnt:
            lst = []
            emptyCount = 0
            for col in range(colCnt):
                itemCell = QTableWidgetItem()
                itemCell = self.tabData.item(currentRow, col)
                if itemCell is None: return
                txt = itemCell.text()
                if len(txt) == 0:
                    emptyCount += 1
                    continue
                try:
                    lst.append(float(txt))
                except ValueError:
                    msg = self.tr("Unable to convert cell (%1,%2) to numeric value. Please check.").\
                        arg(currentRow+1).arg(col+1)
                    QMessageBox.information(self,self.tr('information'),msg)
                    self.msgboxState = True
                    return

            if colCnt == emptyCount:  #If a row has three empty cells,it will filter the entire row
                emptyRows.append(currentRow)
                currentRow += 1
                continue
            elif 0 == emptyCount:  #If a row has complete data, it is normal
                tabData[currentRow] =lst
                currentRow += 1

            else:  #If a row of data lack of one or two, it comes a messageBox
                msg = self.tr("There is empty cell in table. Please check.")
                QMessageBox.information(self, self.tr('information'), msg)
                self.msgboxState = True
                return
        else:
            return np.delete(tabData, emptyRows, 0)

    def loadData(self):
        '''
        :the function will get settings data from these widgets in QDialog
        :return :a dict including all the settings,having keys including data,nbit,nburnin,nkeep,nskip,seed,logstep,factor
        '''
        pDict   = {}
        datalist= self.readTableData()
        if datalist is  None or 0 == len(datalist): return
        try:
            nbit    = int(self.leNbit.text())
            nburnin = int(self.leNburnin.text())
            nkeep   = int(self.leNkeep.text())
            nskip   = int(self.leNskip.text())
            seed    = float(self.leSeed.text())
            logstep = float(self.leLogstep.text())
            factor  = float(self.leFactor.text())
        except ValueError:
            self.msgboxState = False
            return
        unit = self.cbUnit.itemData(self.cbUnit.currentIndex())
        nbit   = self.convertNbit(nbit, unit)
        pDict[ 'data'  ]  = datalist
        pDict[ 'nbit'  ]  = nbit
        pDict['nburnin']  = nburnin
        pDict[ 'nkeep' ]  = nkeep
        pDict[ 'nskip' ]  = nskip
        pDict[ 'seed'  ]  = seed
        pDict['logstep']  = logstep
        pDict['factor' ]  = factor
        return pDict

    def setEnableButton(self):
        self.btConverg.setEnabled(True)
        self.btHistogram.setEnabled(True)
        self.btCorrelation.setEnabled(True)
        self.btBestFit.setEnabled(True)
        self.btSave.setEnabled(True)

    def setUnenableButton(self):
        self.btConverg.setEnabled(False)
        self.btHistogram.setEnabled(False)
        self.btCorrelation.setEnabled(False)
        self.btBestFit.setEnabled(False)
        self.btSave.setEnabled(False)
        self.leAcceptRate.clear()

    def fromData(self, settings):
        '''
        :param settings: a MCMCSettings object
        '''
        if not isinstance(settings, MCMCSettings): raise TypeError
        self.data = settings

        #bit value
        self.leNbit.setText(str(settings.nbit))

        #bit selection
        found = False
        for i in xrange(self.cbUnit.count()):
            if settings.bitUnit==self.cbUnit.itemData(i):
                self.cbUnit.setCurrentIndex(i)
                found = True
                break
        if not found: raise ValueError

        #mcmcParams
        self.leNburnin.setText(str(settings.nburnin))
        self.leNkeep.setText(str(settings.nkeep))
        self.leNskip.setText(str(settings.nskip))
        self.leLogstep.setText(str(settings.logstep))
        self.leFactor.setText(str(settings.factor))
        self.leSeed.setText(str(settings.seed))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    a = translator.load("weibull_CN.qm")
    app.installTranslator(translator)
    dlg = DlgWeibullMCMC()
    dlg.show()
    app.exec_()