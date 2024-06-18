from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QSpinBox, QMessageBox
from PyQt5.QtWidgets import QRadioButton

import pathlib
from datetime import date
from threading import Thread

from database import ControllDb, DatabaseThread, insert_db_thread_event

UI_PATH = "ui/registrationFormWidget.ui"


class RegistrationFormWidget(QWidget):
    def __init__(self, doctor):
        super(RegistrationFormWidget, self).__init__()
        self.doctor = doctor
        self.__loadUiFile(pathlib.Path(__file__).parent)
        self.__defineWidgets()
        # self.lazyFill()
        self.create_patient_button.clicked.connect(self.__save)

    def __loadUiFile(self, path) -> None:
        uic.loadUi(path / UI_PATH, self)

    def __defineWidgets(self) -> None:
        self.create_patient_button = self.findChild(
            QPushButton, "create_new_patient_push_button")
        self.cancel_registry_button = self.findChild(
            QPushButton, "cancel_registry_push_button")
        # Acronym
        # First letters of a name: Geravid Divgar = GD
        self.acronym = self.findChild(QLineEdit, "acronym_line_edit")

        # NSS
        self.nss = self.findChild(QLineEdit, "NSSLineEdit")
        self.nssCode = self.findChild(QLineEdit, "NSSCodeLineEdit")

        # Birth Date
        self.birthDay = self.findChild(QSpinBox, "birthDaySpinBox")
        self.birthMonth = self.findChild(QSpinBox, "birthMonthSpinBox")
        self.birthYear = self.findChild(QSpinBox, "birthYearSpinBox")

        # Sex/Gender
        self.genderMale = self.findChild(QRadioButton, "genderMaleRadioButton")
        self.genderFemale = self.findChild(
            QRadioButton, "genderFemaleRadioButton")
        self.genderOther = self.findChild(
            QRadioButton, "genderOtherRadioButton")

    def __save(self) -> None:
        self.__catchData()
        # clean data?
        # lock button?

    def __catchData(self) -> None:
        today = date.today()
        # Get the gender selected in the RadiusBoxes
        if self.genderMale.isChecked():
            self.sex = 1    # Male
        elif self.genderFemale.isChecked():
            self.sex = 2    # Female
        else:
            self.sex = 0    # Other

        year = str(self.birthYear.value())
        month = str(self.birthMonth.value())
        day = str(self.birthDay.value())

        self.birthDate = year + '/' + month + '/' + day
        current_date = str(today.year) + '/' + \
            str(today.month) + '/' + str(today.day)

        # Data for Patient table
        self.patientData = [
            self.acronym.text().upper(),
            self.birthDate,
            self.sex,
            current_date
        ]
        # Insert new patient
        if self.validate_fields():
            if self.__validate_existing_nss():
                self.__insert_into_controller_database()
            else:
                self.__nss_already_exist_alert()
        else:
            self.__missing_fields_pup_up()

    def __insert_into_controller_database(self) -> None:
        # Insert medical record and user
        # self.patientData.insert(0, self.id_medical_record)
        self.patientData.insert(0, self.doctor.id)
        self.completeNss = self.nss.text() + self.nssCode.text()
        self.patientData.insert(0, self.completeNss)
        controll_db = ControllDb()
        db_thread = Thread(
            target=controll_db.insertIntoPatient,
            args=(tuple(self.patientData),)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        db_thread.join()

    def validate_fields(self) -> bool:
        self.emptyFields = ""
        valid_data = False

        # print("--- VALIDATION ---")
        if self.nss.text() == '' or self.nssCode.text() == '':
            self.emptyFields += "\n* --> NSS"

        if self.validate_birthdate():
            self.emptyFields += "\n --> Fecha Nacimiento"

        # print(self.emptyFields, len(self.emptyFields))

        if len(self.emptyFields) == 0:
            # print("Data OK")
            valid_data = True
        else:
            # print("Data WRONG")
            valid_data = False
        
        return valid_data

    def __validate_existing_nss(self) -> bool:
        # Validate if the NSS already exist on patient table
        # (False = Not exist, True = Exist)
        controll_db = ControllDb()
        valid_nss = False
        db_thread = DatabaseThread(
            target=controll_db.validate_existing_nss,
            args=(self.nss.text() + self.nssCode.text(),)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        if db_thread.join():
            self.nss_validated = False
            valid_nss = False
        else:
            # Flag for the second validation from stackedRegistrationWidget class
            self.nss_validated = True
            valid_nss = True
        return valid_nss

    def validate_birthdate(self) -> bool:
        valid_birthdate = False
        try:
            birthdate = date(self.birthYear.value(),
                             self.birthMonth.value(), self.birthDay.value())
            if birthdate > date.today():
                valid_birthdate = True
            valid_birthdate = False
        except ValueError:
            valid_birthdate = True
        
        return valid_birthdate

    def clean_fields(self) -> None:
        # Data for Patient table
        self.acronym.clear()
        self.nss.clear()
        self.nssCode.clear()
        self.birthDay.cleanText()
        self.birthMonth.cleanText()
        self.birthYear.cleanText()

        # self.genderFemale.setChecked(False)
        # self.genderMale.setChecked(False)
        # self.genderOther.setChecked(False)

    def __missing_fields_pup_up(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("Campos Erroneos")

        msg.setText("Error en los siguientes campos:\n" + self.emptyFields)

        msg.exec_()

    def __nss_already_exist_alert(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("Duplicated NSS")

        msg.setText("The provided NSS already exists:\n" +
                    self.nss.text() + self.nssCode.text())

        msg.exec_()
