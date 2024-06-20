from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import QComboBox, QTableView, QAbstractItemView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import QSortFilterProxyModel

import pathlib
from datetime import date

from database import ControllDb

UI_PATH = "ui/searchWidget.ui"


class SearchWidget(QWidget):
    def __init__(self):
        super(SearchWidget, self).__init__()
        self.loadUiFile(pathlib.Path(__file__).parent)

        self.defineWidgets()

        self.load_table_from_db()
        self.setModel()
        self.filterChanged()

        self.searchField.textChanged.connect(
            self.filterProxyModel.setFilterRegExp)
        self.filterBox.currentIndexChanged.connect(self.filterChanged)

    def loadUiFile(self, path):
        uic.loadUi(path / UI_PATH, self)

    def defineWidgets(self):
        self.searchField = self.findChild(QLineEdit, "searchLineEdit")
        self.filterBox = self.findChild(QComboBox, "filterComboBox")
        self.table = self.findChild(QTableView, "tableView")
        self.model = QStandardItemModel()
        self.filterProxyModel = QSortFilterProxyModel()
        self.new_patient_button = self.findChild(
            QPushButton, "new_patient_push_button")

    def setModel(self):
        self.model.setHorizontalHeaderLabels(
            ['Doctor', 'NSS', 'Acronym', 'Age', 'Registration Date'])
        self.filterProxyModel.setSourceModel(self.model)
        self.filterProxyModel.setFilterCaseSensitivity(False)
        self.filterProxyModel.setFilterKeyColumn(2)
        self.table.verticalHeader().hide()
        self.table.setModel(self.filterProxyModel)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.filterBox.setCurrentIndex(1)

    def filterChanged(self):
        filterText = self.filterBox.currentText()
        if filterText == "Doctor":
            self.filterProxyModel.setFilterKeyColumn(0)
        if filterText == "NSS":
            self.filterProxyModel.setFilterKeyColumn(1)
        if filterText == "Acrónimo":
            self.filterProxyModel.setFilterKeyColumn(2)
        if filterText == "Edad":
            self.filterProxyModel.setFilterKeyColumn(3)
        if filterText == "Fecha Registro":
            self.filterProxyModel.setFilterKeyColumn(4)

    def load_table_from_db(self):
        controll_db = ControllDb()
        pacientInformation = controll_db.select_all_patients()

        for i, row in enumerate(pacientInformation):
            docId = self.get_doctor_name(str(pacientInformation[i][0]), controll_db)

            pacientId = str(pacientInformation[i][1])
            acronym = str(pacientInformation[i][2])
            birthdate = str(self.calculate_age(pacientInformation[i][3]))
            registrationDate = str(pacientInformation[i][4])

            self.model.setItem(i, 0, QStandardItem(docId))
            self.model.setItem(i, 1, QStandardItem(pacientId))
            self.model.setItem(i, 2, QStandardItem(acronym))
            self.model.setItem(i, 3, QStandardItem(birthdate))
            self.model.setItem(i, 4, QStandardItem(registrationDate))

    def update_table(self):
        self.model.removeRows(0, self.model.rowCount())
        self.load_table_from_db()

    def get_doctor_name(self, id_doctor, controll_db):
        doctor = controll_db.getDoctorName(id_doctor)
        return str(doctor[0] + " " + doctor[1])

    def calculate_age(self, born):
        today = date.today()
        try:
            birthday = born.replace(year=today.year)

        except ValueError:
            birthday = born.replace(year=today.year,
                                    month=born.month + 1, day=1)

        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year
