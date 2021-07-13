
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui

from easygui import fileopenbox
import platform
import xml.etree.ElementTree as ET
import functools
import json

from MainWindow import Ui_MainWindow_NMR
from GUI_Toolbox import TableModelData
from GUI_Toolbox import NMRData
from Driver_referenceMeasurement_createFile_importExcel import Driver_referenceMeasurement_createFile_importExcel




class GUI_MainWindow:
    
    #Get UI components

    
    
    def __init__(self):
        self.main_win = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow_NMR()
        self.ui.setupUi(self.main_win)


        #READ JSON DATABASE OF MATERIAL/BULK
        material_bulk_file = open('Data/material_bulk_database.json', 'r')
        self.material_bulk_data = json.loads(material_bulk_file.read())
        material_bulk_file.close()

        self.nmrDataTools = NMRData()
        
        self.CalibrationLine_AcomArea()





    #************************************************************************#
    ######################    TAB 1    #######################################
    #************************************************************************#


    def CalibrationLine_AcomArea(self):

        self.ui.dateTimeEdit_dateTime.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.dateTimeEdit_dateTime.setDisplayFormat("dd/MM/yyyy")

        #GUI Variables
        self.user = self.ui.plainTextEdit_user
        self.bulkName = self.ui.comboBox_bulkName
        self.dateTime = self.ui.dateTimeEdit_dateTime
        self.densityBulk = self.ui.plainTextEdit_densityBulk
        self.evaluation_double = self.ui.checkBox_evaluation_other
        self.evaluation_single = self.ui.checkBox_evaluation_single
        self.language_english = self.ui.checkBox_language_english
        self.language_german = self.ui.checkBox_language_german
        self.materialName = self.ui.comboBox_materialName
        self.particleDensity = self.ui.plainTextEdit_particleDensity
        self.remarks = self.ui.plainTextEdit_remarks
        self.surfaceArea_Argon = self.ui.plainTextEdit_surfaceArea_Argon
        self.temperature = self.ui.plainTextEdit_temperature

        self.user.setPlainText("Alexander Michalowski")
        #bulkName.addItems(["Milipore-Wasser_LFG", "Milipore-Wasser"])
        #densityBulk.setPlainText("1")
        #materialName.addItems(["80nmIV", "Test2"])
        #particleDensity.setPlainText("2.14")
        self.remarks.setPlainText("#76,#77,#79")
        #surfaceArea_Argon.setPlainText("47.0")
        self.temperature.setPlainText("25°C")

        self.MaterialDataLoad("start")
        self.BulkDataLoad("start")

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
        self.addMaterial_btn.clicked.connect(lambda:self.addMaterialData(self.ui.comboBox_materialName.currentText(), self.ui.plainTextEdit_surfaceArea_Argon.toPlainText(), self.ui.plainTextEdit_particleDensity.toPlainText()))

        self.addBulk_btn = self.ui.pushButton_AddBulk
        self.addBulk_btn.clicked.connect(lambda:self.addBulkData(self.ui.comboBox_bulkName.currentText(), self.ui.plainTextEdit_densityBulk.toPlainText()))

        self.removeMaterial_btn = self.ui.pushButton_RemoveMaterial
        self.removeMaterial_btn.clicked.connect(lambda:self.removeMaterialData(self.ui.comboBox_materialName.currentText()))

        self.removeBulk_btn = self.ui.pushButton_RemoveBulk
        self.removeBulk_btn.clicked.connect(lambda:self.removeBulkData(self.ui.comboBox_bulkName.currentText()))

        self.tableModel = TableModelData()


    def addMaterialData(self, materialName, surfaceAreaArgon, particleDensity):

        for i in self.material_bulk_data['materials']:
            if i['materialName'] == materialName:
                i['surfaceAreaArgon'] = surfaceAreaArgon
                i['particleDensity'] = particleDensity

                return 0
        
        new_entry = [{
            "materialName": materialName,
            "surfaceAreaArgon": surfaceAreaArgon,
            "particleDensity": particleDensity
        }]
        materiallist = self.material_bulk_data['materials']
        self.material_bulk_data['materials'].extend(new_entry)
        
        self.MaterialDataLoad("add")
        self.updateJsonDatabase()



    def addBulkData(self, bulkName, densityBulk):
        
        for i in self.material_bulk_data['bulk']:
            if i['bulkName'] == bulkName:
                i['densityBulk'] = densityBulk

                return 0
        
        new_entry = [{
            "bulkName": bulkName,
            "densityBulk": densityBulk,
        }]
        bulklist = self.material_bulk_data['bulk']
        self.material_bulk_data['bulk'].extend(new_entry)
        
        self.BulkDataLoad("add")
        self.updateJsonDatabase()

    def removeMaterialData(self, materialName):
        
        j=0
        for i in self.material_bulk_data['materials']:
            if i['materialName'] == materialName:
                self.material_bulk_data['materials'].pop(j)
            j += 1
        
        self.MaterialDataLoad("delete")
        self.updateJsonDatabase()


    def removeBulkData(self, bulkName):
        
        j=0
        for i in self.material_bulk_data['bulk']:
            if i['bulkName'] == bulkName:
                self.material_bulk_data['bulk'].pop(j)
            j += 1
        
        self.BulkDataLoad("delete")
        self.updateJsonDatabase()
    

    def updateJsonDatabase(self):
        
        jsonData = json.dumps(self.material_bulk_data)

        material_bulk_file = open('Data/material_bulk_database.json', 'w')
        material_bulk_file.write(jsonData)
        material_bulk_file.close()

    def MaterialDataLoad(self,state):

        material = []

        for i in self.material_bulk_data['materials']:

            material.append(i['materialName'])

        
        self.updateMaterialComboBoxes(material,state)
        

        self.setMaterialProperties()
        

    def BulkDataLoad(self,state):

        bulk = []

        for i in self.material_bulk_data['bulk']:

            bulk.append(i['bulkName'])

        self.updateBulkComboBoxes(bulk,state)
        self.setBulkProperties()

    def updateMaterialComboBoxes(self,material,state):
        
        matindex = 0

        if state == "add":
            matindex = self.materialName.count()

        self.materialName.clear()

        self.materialName.addItems(material)
        self.materialName.setCurrentIndex(matindex)
        self.setMaterialProperties()

    def updateBulkComboBoxes(self, bulk, state):

        bulkindex = 0

        if state == "add":
            bulkindex = self.bulkName.count()

        self.bulkName.clear()

        self.bulkName.addItems(bulk)
        self.bulkName.setCurrentIndex(bulkindex)
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
            results = self.nmrDataTools.getNMRinfo(f)
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
    main_win = GUI_MainWindow()
    main_win.show()
    sys.exit(app.exec())
