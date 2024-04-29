from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QTextEdit, QFileDialog

import sys
import pathlib
from patient import Patient
from pdftotextwithimages import ExtractPDFData
import re
import os
import shutil

UI_PATH = "ui/reportWidget.ui"
OSA_PATH = "multimedia\osa"
OSA_EXTENCION = ".osa"

class OsaFile(QWidget):
    def __init__(self, database, isEdit):
        super(OsaFile, self).__init__()
        self.database = database
        self.isEdit = isEdit
        self.edf_path = ""
        self.path_edf = ["",""]

        self.loadUiFile(pathlib.Path(__file__).parent)
        self.defineWidgets()
        self.defineButton()
        self.saveReportButton.clicked.connect(self.insertOrUpdate)

        
    def loadUiFile(self, path):
        uic.loadUi(path / UI_PATH, self)

    def defineButton(self):
        self.loadReportButton.clicked.connect(self.selectReport)
        self.loadEDFFileButton.clicked.connect(self.select_edf)

    def select_edf(self):
        self.path_edf = QFileDialog.getOpenFileName(self,
                                        "Seleccionar Video",
                                        str(pathlib.Path().absolute()),
                                        "EDF/OSA (*.edf *.osa)")

        if self.path_edf[0] != "":
            # print("File Selected: " + self.path_edf[0])

            self.osa_file_loaded()
        else:
            pass


    def insertOrUpdate(self):
        if self.isEdit:
            from global_ import selectedPatient as patient
            if patient.apneaStudy.report.id != "":
                self.packData()
                self.updateReport()
            else:
                self.insertReport()
            
            if patient.apneaStudy.edf.id != "":
                # self.update_osa()
                pass
            else:
                self.insert_osa()

        else:
            self.insertReport()
            self.insert_osa()
        
        if self.path_edf[0] != "":
            self.copy_osa_file()

    def insert_osa(self):
        if self.isEdit:
            from global_ import selectedPatient as patient

            tuple_data = [patient.apneaStudy.id, self.edf_path]
            self.edf_path = OSA_PATH + r"\\"
            + str(patient.apneaStudy.id) + OSA_EXTENCION

            self.database.insert_edf_file(tuple(tuple_data))
        else:
            from global_ import registeredPatient as patient

            self.edf_path = OSA_PATH + r"\\"
            + str(patient.apneaStudy.id) + OSA_EXTENCION

            if self.check_loaded_osa_file():
                tuple_data = [patient.apneaStudy.id, self.edf_path]
                self.database.insert_edf_file(tuple(tuple_data))
    
    def update_osa(self):
        from global_ import selectedPatient as patient

        self.edf_path = OSA_PATH + r"\\" + str(patient.apneaStudy.id)
        + OSA_EXTENCION

        tuple_data = [patient.apneaStudy.edf.id, self.edf_path]
        self.database.update_edf_file(tuple(tuple_data))

    def copy_osa_file(self):
        home_path = str(pathlib.Path().absolute())
        if self.isEdit:
            from global_ import selectedPatient as patient

            fname = home_path + "\\" + OSA_PATH + "\\" + str(patient.apneaStudy.id) + OSA_EXTENCION
            # print(self.path_edf[0])

            try:
                # os.system(f"copy {str(self.path_edf[0])} {fname}")
                shutil.copyfile(str(self.path_edf[0]), fname)
            except shutil.SameFileError:
                pass

        else:
            from global_ import registeredPatient as patiente

            fname = home_path + "\\" + OSA_PATH + "\\" + str(patiente.apneaStudy.id) + OSA_EXTENCION
            # print(self.path_edf[0])

            try:
                # os.system(f"copy {str(self.path_edf[0])} {fname}")
                shutil.copyfile(str(self.path_edf[0]), fname)
            except shutil.SameFileError:
                pass

    def osa_file_loaded(self):
        self.editEDFFileButton.setStyleSheet("background-color: rgb(0,255,0);")
        self.editEDFFileButton.setText("Archivo OSA Cargado")


    def check_loaded_osa_file(self):
        if self.path_edf[0] == "":
            return False
        else:
            return True
