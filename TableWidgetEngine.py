__all__ = ['TableWidgetEngine']

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
import numpy as np


class TableWidgetEngine(QObject):
    def __init__(self, tabWidget, data=None):
        if not isinstance(tabWidget, QTableWidget): raise TypeError
        self.data = data
        self.tabWidget = tabWidget
        self.rowCnt = tabWidget.rowCount()
        self.colCnt = tabWidget.columnCount()

    def updateTable(self):
        rowCnt, _ = np.shape(self.data)
        self.tabWidget.clearSpans()
        self.tabWidget.setUpdatesEnabled(False)
        self.tabWidget.setRowCount(rowCnt)
        for row in range(rowCnt):
            self.tabWidget.setRowHeight(row, 25)
            newItem = []
            for col in range(self.colCnt):
                newItem.append(QTableWidgetItem(""))
                newItem[col].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                newItem[col].setFlags( Qt.ItemIsEnabled| Qt.ItemIsSelectable | Qt.ItemIsEditable)
                txt = str(self.data[row][col])
                newItem[col].setText(txt)
                self.tabWidget.setItem(row, col, newItem[col])
        self.tabWidget.setUpdatesEnabled(True)

    def removeSelectedRows(self):
        select = self.tabWidget.selectionModel()
        indexlist = select.selectedIndexes()
        if len(indexlist) !=0:
            dic = {}
            rowlist = []
            for index in indexlist:
                dic[index] = index.row()
                if dic[index] not in rowlist:
                    rowlist.append(dic[index])
            rowlist.sort()
            rowlist.reverse()
            for i in range(len(rowlist)):
                self.tabWidget.removeRow(rowlist[i])

    def addRow(self):
        self.tabWidget.setRowCount(self.rowCnt+1)
        self.tabWidget.setRowHeight(self.rowCnt, 25)
        for col in range(self.colCnt):
            newItem = QTableWidgetItem("")
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            newItem.setFlags( Qt.ItemIsEnabled| Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.tabWidget.setItem(self.rowCnt, col, newItem)
            self.tabWidget.setCurrentItem(newItem, QItemSelectionModel.Clear)

    def fromTableData(self):
        currentRow, rowCnt, colCnt = 0, self.rowCnt, self.colCnt
        if rowCnt == 0: return
        tabData = np.zeros((rowCnt, colCnt))
        emptyRows = []
        while currentRow < rowCnt:
            rowData = np.zeros((1,colCnt))
            emptyCount = 0
            for col in range(colCnt):
                itemCell = QTableWidgetItem()
                itemCell = self.tabWidget.item(currentRow, col)
                if itemCell is None: return
                txt = itemCell.text()
                if len(txt) == 0:
                    emptyCount += 1
                    continue
                try:
                    rowData[0, col] = float(txt)
                except ValueError:
                    msg = QApplication.translate("TableWidgetEngine","Unable to convert cell (%1,%2) to numeric value. Please check.").\
                        arg(currentRow+1).arg(col+1)
                    QMessageBox.information(None, QApplication.translate("TableWidgetEngine",'information'), msg)
                    self.msgboxState = True
                    return

            if colCnt == emptyCount:  #If a row has three empty cells,it will filter the entire row
                emptyRows.append(currentRow)
                currentRow += 1
                continue
            elif 0 == emptyCount:  #If a row has complete data, it is normal
                tabData[currentRow] = rowData
                currentRow += 1

            else:  #If a row of data lack of one or two, it comes a messageBox
                msg = QApplication.translate("TableWidgetEngine","There is empty cell in table. Please check.")
                QMessageBox.information(None, QApplication.translate('TableWidgetEngine','information'), msg)
                self.msgboxState = True
                return
        else:
            return np.delete(tabData, emptyRows, 0)
