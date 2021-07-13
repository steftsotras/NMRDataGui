import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui

from easygui import fileopenbox
import platform
import xml.etree.ElementTree as ET
import functools
import json

from MainWindow import Ui_MainWindow_NMR
from Driver_referenceMeasurement_createFile_importExcel import Driver_referenceMeasurement_createFile_importExcel



class TableModelData():
    

    def __init__(self):
        self.model = QtGui.QStandardItemModel(0,6)
        self.model.setHorizontalHeaderLabels(('Sample Name','T1 Value','T2 Value','Liquid Mass','Particle Mass', 'Position'))
        

    def DelRows(self, selectedRowsDEL):
        
        selectedRowsDEL.sort(reverse = True)

        for i in selectedRowsDEL:
            if(i >= 1 or i <= self.model.rowCount()):
                self.model.removeRow(i-1)
            

    def RemoveAllRows(self):
        
        for row in range(self.model.rowCount()):
            self.model.removeRow(0)

    def AddRows(self, num, group1, group2):
        
        i=0
        
        for row in range(self.model.rowCount(), self.model.rowCount() + num):
        
            self.model.insertRow(self.model.rowCount())
            
            #Data from excel
            item = QtGui.QStandardItem(group1[i][1])
            self.model.setItem(row, 0, item)
            #item = QtGui.QStandardItem("{0:.2f}, {0:.2f}, {0:.2f}".format( group1[i][3], group1[i+1][3], group1[i+2][3] ) )
            item = QtGui.QStandardItem('%.2f - %.2f - %.2f' % (group1[i][3], group1[i+1][3], group1[i+2][3]) ) 
            self.model.setItem(row, 1, item)
            item = QtGui.QStandardItem('%.2f -  %.2f - %.2f' % (group2[i][3], group2[i+1][3], group2[i+2][3]) )
            self.model.setItem(row, 2, item) 

            i+=3
            
            #Position
            item = QtGui.QStandardItem(str(row+1))
            self.model.setItem(row, 5, item)

        return self.model

class MainWindow:
    
    #Get UI components

    
    
    def __init__(self):
        self.main_win = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow_NMR()
        self.ui.setupUi(self.main_win)

        #Set Date to Current
        self.ui.dateTimeEdit_dateTime.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.dateTimeEdit_dateTime.setDisplayFormat("dd/MM/yyyy")



        #GUI Variables
        user = self.ui.plainTextEdit_user
        self.bulkName = self.ui.comboBox_bulkName
        dateTime = self.ui.dateTimeEdit_dateTime
        self.densityBulk = self.ui.plainTextEdit_densityBulk
        self.evaluation_double = self.ui.checkBox_evaluation_other
        self.evaluation_single = self.ui.checkBox_evaluation_single
        self.language_english = self.ui.checkBox_language_english
        self.language_german = self.ui.checkBox_language_german
        self.materialName = self.ui.comboBox_materialName
        self.particleDensity = self.ui.plainTextEdit_particleDensity
        remarks = self.ui.plainTextEdit_remarks
        self.surfaceArea_Argon = self.ui.plainTextEdit_surfaceArea_Argon
        temperature = self.ui.plainTextEdit_temperature

        user.setPlainText("Alexander Michalowski")
        #bulkName.addItems(["Milipore-Wasser_LFG", "Milipore-Wasser"])
        #densityBulk.setPlainText("1")
        #materialName.addItems(["80nmIV", "Test2"])
        #particleDensity.setPlainText("2.14")
        remarks.setPlainText("#76,#77,#79")
        #surfaceArea_Argon.setPlainText("47.0")
        temperature.setPlainText("25°C")

        material_bulk_file = open('Data/material_bulk_database.json', 'r')
        self.material_bulk_data = json.loads(material_bulk_file.read())
        material_bulk_file.close()

        self.MaterialBulkDataPreload()

        
        self.run_btn = self.ui.pushButton_run_MeasurementFile
        self.run_btn.clicked.connect(self.fetch_input)


        #ADD - DELETE FILES BUTTONS
        self.add_btn = self.ui.pushButton_AddMesurementFiles
        self.add_btn.clicked.connect(self.addFiles)

        self.remove_btn = self.ui.pushButton_RemoveAllMesurementFiles
        self.remove_btn.clicked.connect(self.removeFiles)
        
        self.removeSel_btn = self.ui.pushButton_RemoveSelectedMeasrementFiles
        self.removeSel_btn.clicked.connect(self.removeSelFiles)

        
        
        #COMBO BOXES
        self.comboMaterial = self.ui.comboBox_materialName
        self.comboMaterial.currentTextChanged.connect(self.setMaterialProperties)

        self.comboBulk = self.ui.comboBox_bulkName
        self.comboBulk.currentTextChanged.connect(self.setBulkProperties)

        
        #ADD - DELETE MAT/BULK BUTTONS
        
        self.addMaterial_btn = self.ui.pushButton_AddMaterial
        self.addMaterial_btn.clicked.connect(self.addMaterialData)

        self.addBulk_btn = self.ui.pushButton_AddBulk
        self.addBulk_btn.clicked.connect(self.addBulkData)

        self.removeMaterial_btn = self.ui.pushButton_RemoveMaterial
        self.removeMaterial_btn.clicked.connect(self.removeMaterialData)

        self.removeBulk_btn = self.ui.pushButton_RemoveBulk
        self.removeBulk_btn.clicked.connect(self.removeBulkData)

        self.tableModel = TableModelData()
        


    #def addMaterialData(self):
        #self.material_bulk_data.

    def MaterialBulkDataChange(self, e):
        print(e)
    
    def MaterialBulkDataPreload(self):

        material = []
        bulk = []

        for i in self.material_bulk_data['materials']:

            material.append(i['materialName'])

        for i in self.material_bulk_data['bulk']:

            bulk.append(i['bulkName'])

        self.bulkName.addItems(bulk)
        self.materialName.addItems(material)

        self.setMaterialProperties()
        self.setBulkProperties()


    def setMaterialProperties(self):
        
        matName = self.materialName.currentText()

        for i in self.material_bulk_data['materials']:

            if i['materialName'] == (matName):
                self.particleDensity.setPlainText(i['particleDensity'])
                self.surfaceArea_Argon.setPlainText(i['surfaceAreaArgon'])

    def setBulkProperties(self):
        
        bName = self.bulkName.currentText()

        for i in self.material_bulk_data['bulk']:

            if i['bulkName'] == (bName):
                self.densityBulk.setPlainText(i['densityBulk'])


    #Here we get info for each file
    def getNMRinfo(self, nmrfile):

        #load xml file
        tree = ET.parse(nmrfile)
        
        #Create a list that will contain the different worksheet items
        WorkSheets = list()
        
        #Add Worksheet-items to list 
        #[results, data, experiment, instrument, programmsettings, generator]
        for item in tree.iter("{urn:schemas-microsoft-com:office:spreadsheet}Worksheet"):
            WorkSheets.append(item)
            

        #Extract rows from the first worksheet <results>
        RowsInWorksheet = list()
        for item in WorkSheets[0].iter('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
            RowsInWorksheet.append(item)

        t_value = 0
        exp_name = ""
        sample_name = ""
        file_name = ""

        for row in range(0, len(RowsInWorksheet), 1):
            #print(str(RowsInWorksheet[row][0].text))
            if str(RowsInWorksheet[row][0].text)=='T1' or str(RowsInWorksheet[row][0].text)=='T2A':
                exp_name = str(RowsInWorksheet[row][0].text)
                t_value = float(str(RowsInWorksheet[row+1][0].text))
                #print(t_value)

        #Extract rows from the third worksheet <experiment>
        RowsInWorksheet = list()
        for item in WorkSheets[2].iter('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
            RowsInWorksheet.append(item)

        sample_name = str(RowsInWorksheet[70][0].text)
        file_name = str(RowsInWorksheet[34][0].text)

        results = [exp_name, sample_name, file_name, t_value  ]

        return results
            
        
    def CreateTable(self, num, group1, group2):
        
        
        
        
        #if table.():
        
        
        #   TABLE VIEW MODEL SOLUTION
        model = QtGui.QStandardItemModel(num,6)
        model.setHorizontalHeaderLabels(('Sample Name','T1 Value','T2 Value','Liquid Mass','Particle Mass', 'Position'))

        i=0
        
        for row in range(num):
            
            #Data from excel
            item = QtGui.QStandardItem(group1[i][1])
            model.setItem(row, 0, item)
            #item = QtGui.QStandardItem("{0:.2f}, {0:.2f}, {0:.2f}".format( group1[i][3], group1[i+1][3], group1[i+2][3] ) )
            item = QtGui.QStandardItem('%.2f - %.2f - %.2f' % (group1[i][3], group1[i+1][3], group1[i+2][3]) ) 
            model.setItem(row, 1, item)
            item = QtGui.QStandardItem('%.2f -  %.2f - %.2f' % (group2[i][3], group2[i+1][3], group2[i+2][3]) )
            model.setItem(row, 2, item) 

            i+=3
            
            #Position
            item = QtGui.QStandardItem(str(row+1))
            model.setItem(row, 5, item)


        table = self.ui.tableView_mesurementFiles
        table.setModel(model)
        table.horizontalHeader().resizeSection(0, 330)
        table.resizeColumnsToContents()

    #def addRowsTable(self, numOfRows, group1, group2):
        
    def removeSelFiles(self):

        #fetch selected
        plainText_selectedFiles = self.ui.plainTextEdit_RemoveSelectedFilesMeasrementFiles
        selectedRowsDEL = plainText_selectedFiles.toPlainText().split(",")

        selectedRowsDEL = [int(i) for i in selectedRowsDEL]
        

        self.tableModel.DelRows(selectedRowsDEL)
        
    #Grouping Files to cook them up for the script
    def groupFiles(self, files):

        fileInfo = list()
        #groupedfiles = []
        
        for f in files:
            results = self.getNMRinfo(f)
            results.append(f)
            fileInfo.append(results)

        #print(fileInfo)
        #Update UI

        #create groupedfiles for script input
        fileInfo.sort(key=lambda x: x[1])
        groupedBySampleName = functools.reduce(lambda l, x: (l.append([x]) if l[-1][0][1] != x[1] else l[-1].append(x)) or l, fileInfo[1:], [[fileInfo[0]]]) if fileInfo else []
        
        self.numberOfConcentrations = 0

        self.groupedT1 = list()
        self.groupedT2 = list()

        for groupRow in groupedBySampleName:

            self.numberOfConcentrations += 1
            #print("GROUP")    
            #print(groupRow)

            if len(groupRow) != 6:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText("Wrong Input!!")
                msgBox.setWindowTitle("Eisai malakas")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                returnValue = msgBox.exec()
                return 0
            

            for groupT in groupRow:

                if str(groupT[0]) == "T2A":
                    self.groupedT2.append(groupT)
                elif str(groupT[0]) == "T1":
                    self.groupedT1.append(groupT)
                else:
                    return 0
        
        print(self.groupedT1)
        print(self.groupedT2)
        #self.CreateTable(self.numberOfConcentrations, self.groupedT1, self.groupedT2)
        model = self.tableModel.AddRows(self.numberOfConcentrations, self.groupedT1, self.groupedT2)
        
        table = self.ui.tableView_mesurementFiles
        table.setModel(model)
        table.horizontalHeader().resizeSection(0, 330)
        table.resizeColumnsToContents()    


    


    #ADD REMOVE FILES LOGIC
    def addFiles(self):
        textForOpeningFiles = "Please select Files for Concentration"
        files = fileopenbox(textForOpeningFiles, "Dunno", default = "", filetypes= "*.txt", multiple=True)
        if files:
            #print(files)
            self.groupFiles(files)
            


        else:
            #print("exit")
            pass
        
    def removeFiles(self):
        self.tableModel.RemoveAllRows()

    


    #RUN BUTTON
    def fetch_input(self):
        
        user = self.ui.plainTextEdit_user
        bulkName = self.ui.comboBox_bulkName
        dateTime = self.ui.dateTimeEdit_dateTime
        densityBulk = self.ui.plainTextEdit_densityBulk
        evaluation_double = self.ui.checkBox_evaluation_other
        evaluation_single = self.ui.checkBox_evaluation_single
        language_english = self.ui.checkBox_language_english
        language_german = self.ui.checkBox_language_german
        materialName = self.ui.comboBox_materialName
        particleDensity = self.ui.plainTextEdit_particleDensity
        remarks = self.ui.plainTextEdit_remarks
        surfaceArea_Argon = self.ui.plainTextEdit_surfaceArea_Argon
        temperature = self.ui.plainTextEdit_temperature

        #print(dateTime.dateTime().toString(self.ui.dateTimeEdit_dateTime.displayFormat()))

        model = self.ui.tableView_mesurementFiles.model()
        print("aaaa "+str(self.numberOfConcentrations))
        data = [[0 for x in range(model.columnCount())] for y in range(self.numberOfConcentrations)]
        
        files_T1 = [[0 for x in range(3)] for y in range(self.numberOfConcentrations)]
        files_T2 = [[0 for x in range(3)] for y in range(self.numberOfConcentrations)]
        filespath_T1 = [[0 for x in range(3)] for y in range(self.numberOfConcentrations)]
        filespath_T2 = [[0 for x in range(3)] for y in range(self.numberOfConcentrations)]
        
        liquidmassfromTable = list()
        particlemassfromTable = list()
        print(particlemassfromTable)
        group_row = 0

        for row in range(model.rowCount()):
            #data.append([])

            pos = int(model.data( model.index(row, 5)))
            print(pos)
            if pos < 1 or pos > self.numberOfConcentrations:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText("Wrong position given")
                msgBox.setWindowTitle("Eisai malakas")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                returnValue = msgBox.exec()
                return 0

            #Populate filenames in the correct order
            
            for i in range(3):
                files_T1[pos-1][i] = self.groupedT1[group_row][2]
                files_T2[pos-1][i] = self.groupedT2[group_row][2]
                filespath_T1[pos-1][i] = self.groupedT1[group_row][4]
                filespath_T2[pos-1][i] = self.groupedT2[group_row][4]
                group_row += 1

            for column in range(model.columnCount()):
                print("ooooo "+str(column))
                index = model.index(row, column)
                # We suppose data are strings
                data[pos-1][column] = str(model.data(index)) 

        for j in range(self.numberOfConcentrations) :
            liquidmassfromTable.append(float(data[j][3]))
            particlemassfromTable.append(float(data[j][4]))


        allFiles = files_T1 + files_T2

        print(liquidmassfromTable)
        print(particlemassfromTable)
        print(allFiles)
        print(data)
        
        if evaluation_single.isChecked() == True and evaluation_double.isChecked() == False:
            evaluation = "single"
        elif evaluation_single.isChecked() == False and evaluation_double.isChecked() == True:
            evaluation = "????"
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText("both checked evaluation")
            msgBox.setWindowTitle("Eisai malakas")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            returnValue = msgBox.exec()
            return 0
        
        if language_english.isChecked() == True and language_german.isChecked() == False:
            language = "english"
        elif language_english.isChecked() == False and language_german.isChecked() == True:
            language = "german"
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText("double checked language")
            msgBox.setWindowTitle("Eisai malakas")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            returnValue = msgBox.exec()
            return 0
        driver = Driver_referenceMeasurement_createFile_importExcel()
        driver.runDriver(materialName.currentText(), evaluation, bulkName.currentText(), user.toPlainText(), language, remarks.toPlainText(), temperature.toPlainText(), float(surfaceArea_Argon.toPlainText()), float(densityBulk.toPlainText()), float(particleDensity.toPlainText()), dateTime.dateTime().toString("yyyyMMdd"), self.numberOfConcentrations, files_T1, files_T2, filespath_T1, filespath_T2, liquidmassfromTable, particlemassfromTable )
        

    


    def show(self):
        self.main_win.show()
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
