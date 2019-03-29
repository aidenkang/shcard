import sys, time, datetime
import pandas as pd

from pandas import Series, DataFrame
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QListWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QTimer, QTime, QDate
from PyQt5 import uic

ui = uic.loadUiType("../UI/FileBrowser.ui")[0]

class MyMainDialog(QDialog, ui):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.show()

        self.pB_chooseFile.clicked.connect (self.fileSelectionClicked)
        self.pB_parseButton.clicked.connect (self.parseClicked)

    def fileSelectionClicked(self):
        fname = QFileDialog.getOpenFileName(self, caption='Excel file Loading', directory = '', filter="Excel Files (*.xls)" )
        self.shFileName = fname[0]
        print (self.shFileName)
        self.lineEdit.setText (self.shFileName)

        self.df = pd.read_excel (self.shFileName, sheet_name ='Sheet0')
        sort_of_card = set (self.df['카드종류'])

        self.lW_selectCards.clear()
        for s in sort_of_card:
            self.lW_selectCards.addItem(s)

        qdateEnd = QDate.currentDate()
        qdateStart = qdateEnd.addMonths(-1)

        qdateStart.setDate(qdateStart.year(), qdateStart.month(), 14)
        qdateEnd.setDate(qdateEnd.year(), qdateEnd.month(), 13)

        self.dE_start.setDate(qdateStart)
        self.dE_end.setDate(qdateEnd)

        print (qdateEnd, qdateStart)

    def parseClicked(self):
        sdate = self.dE_start.date()
        edate = self.dE_end.date()

        df2 = self.df.query('거래일자 > "{}" & 거래일자 < "{}"'.format (sdate.toString('yyyy.MM.dd'),edate.toString('yyyy.MM.dd')))
        sort_of_card = set (df2['카드종류'])

        self.lW_selectCards.clear()
        for s in sort_of_card:
            self.lW_selectCards.addItem(s)

        gr = df2.groupby(['카드종류'])['적립포인트'].sum()

        self.lW_cardPointSum.clear()
        for s in sort_of_card:
            if s in gr:
                self.lW_cardPointSum.addItem(' ' + str(gr[s]))
            else:
                self.lW_cardPointSum.addItem(' ')

if __name__ == "__main__":
    app = QApplication(sys.argv)

    fsDlg = MyMainDialog()

#    test = SetInputFile()
    """    Draw additional windows """
    sys.exit(app.exec_())
