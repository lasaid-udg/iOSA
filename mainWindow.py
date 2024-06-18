from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QTabWidget
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QPushButton
import pathlib

from searchWidget import SearchWidget
from apneaStudyWidget import ApneaStudyWidget
from registrationFormWidget import RegistrationFormWidget
from exportReports import PatientClinicData, MultimediaReferenceResources
from exportReports import PatientImagePointsReport, ExcelFile
from IntelligentAnalisys import IntelligentAnalisys

UI_PATH = "ui/mainWindow.ui"
EMPTY_PATH = ""


class MainWindow(QMainWindow):
    def __init__(self, doctor):
        super().__init__()
        self.doctor = doctor
        self.loadUiFile(pathlib.Path(__file__).parent)

        self.instantiate_widgets()
        self.define_widgets()
        self.add_widgets()
        self.define_buttons()
        self.stacked_widget.setCurrentIndex(1)

        self.show()

    def loadUiFile(self, path) -> None:
        uic.loadUi(path / UI_PATH, self)

    def define_widgets(self) -> None:
        self._full_patiente_report_button = self.findChild(QPushButton,
                                                           "full_patiente_report_button")
        self._patient_clinic_data_button = self.findChild(QPushButton,
                                                          "patient_clinic_data_button")
        self._multimedia_reference_button = self.findChild(QPushButton,
                                                           "multimedia_reference_button")
        self._patient_images_points_button = self.findChild(QPushButton,
                                                            "patient_images_points_button")
        self._tab_widget = self.findChild(QTabWidget, "tabWidget")

    def define_buttons(self) -> None:
        self.search_widget.new_patient_button.clicked.connect(
            self.previous_page)
        self.search_widget.table.doubleClicked.connect(
            self.open_patient_studies)
        self.apnea_study_widget.previous_page_button.clicked.connect(
            self.return_to_main_page)
        self.registration_form_widget.create_patient_button.clicked.connect(
            self.new_patient_created)
        self.registration_form_widget.cancel_registry_button.clicked.connect(
            self.cancel_registry)
        self._full_patiente_report_button.clicked.connect(self.generate_excel)
        self._patient_clinic_data_button.clicked.connect(
            self.__generate_patient_clinic_data)
        self._multimedia_reference_button.clicked.connect(
            self.__generate_multimedia_reference_resources)
        self._patient_images_points_button.clicked.connect(
            self.__generate_patient_image_points_report)

    def instantiate_widgets(self):
        self.stacked_widget = self.findChild(
            QStackedWidget, "main_stack_widget")
        self.search_widget = SearchWidget()
        self.apnea_study_widget = ApneaStudyWidget(self.doctor)
        self.registration_form_widget = RegistrationFormWidget(self.doctor)
        self._intelligent_analisys = IntelligentAnalisys()

    def add_widgets(self):
        self._tab_widget.addTab(self._intelligent_analisys, "ADAP")
        self.stacked_widget.addWidget(self.registration_form_widget)
        self.stacked_widget.addWidget(self.search_widget)
        self.stacked_widget.addWidget(self.apnea_study_widget)

    def open_patient_studies(self):
        idx = self.search_widget.table.currentIndex()
        patient_id = self.search_widget.table.model().index(idx.row(),1).data()
        if patient_id:
            self.apnea_study_widget.id_patient = patient_id
            self.next_page()

        # Load all the apnea studies of one patient
        self.apnea_study_widget.load_apnea_studies_to_table()

    def new_patient_created(self):
        if self.registration_form_widget.validate_fields():
            if self.registration_form_widget.nss_validated:
                self.registration_form_widget.clean_fields()
                self.search_widget.update_table()
                self.next_page()

    def cancel_registry(self):
        self.registration_form_widget.clean_fields()
        self.next_page()

    def return_to_main_page(self):
        self.apnea_study_widget.clean_table()
        self.previous_page()

    def next_page(self):
        self.current_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(self.current_index + 1)

    def previous_page(self):
        self.current_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(self.current_index - 1)

    def generate_excel(self):
        path = QFileDialog.getSaveFileName(self, "Destino a Exportar", str(
            pathlib.Path().absolute()), "Excel (*.xlsx *.xls)")

        if path[0] != EMPTY_PATH:
            excel = ExcelFile(path[0])
            excel.generate_excel()

    def __generate_patient_clinic_data(self) -> None:
        path = QFileDialog.getSaveFileName(self, "Destino a Exportar", str(
            pathlib.Path().absolute()), "CSV (*.csv)")
        if path[0] != EMPTY_PATH:
            csv = PatientClinicData(path[0])
            csv.generate_report()

    def __generate_multimedia_reference_resources(self) -> None:
        path = QFileDialog.getSaveFileName(self, "Destino a Exportar", str(
            pathlib.Path().absolute()), "CSV (*.csv)")
        if path[0] != EMPTY_PATH:
            csv = MultimediaReferenceResources(path[0])
            csv.generate_report()

    def __generate_patient_image_points_report(self) -> None:
        path = QFileDialog.getSaveFileName(self, "Destino a Exportar", str(
            pathlib.Path().absolute()), "CSV (*.csv)")
        if path[0] != EMPTY_PATH:
            csv = PatientImagePointsReport(path[0])
            csv.generate_report()

    # ---------------- QT NATIVE CLOSE EVENT CLASS ----------------

    def closeEvent(self, event):
        close_msg = QMessageBox.question(self,
                                         'Exit iOSA',
                                         'Close the iOSA system?',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)

        if close_msg == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
