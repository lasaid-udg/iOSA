from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import QComboBox, QTableView, QAbstractItemView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import QSortFilterProxyModel

import pathlib

from editWindow import EditWindow
from stackedRegistrationWidget import StackedRegistrationWidget

from database import ControllDb, MultimediaDb
from database import DatabaseThread, insert_db_thread_event
from patient import Patient

BLANK = ''
IMAGE_STATUS = "Images Pending"
OSA_STATUS = "OSA Pending"
PDF_STATUS = "PDF Pending"
VIDEO_STATUS = "Pending Video"
COMPLETE_STATUS = "Complete"
FRONT_TAG = 0
LATERAL_TAG = 1

UI_PATH = "ui/apneaStudyWidget.ui"


class ApneaStudyWidget(QWidget):
    def __init__(self, doctor):
        super(ApneaStudyWidget, self).__init__()
        self.doctor = doctor
        # Selected patient ID
        self.id_patient = BLANK
        self.load_ui_file(pathlib.Path(__file__).parent)
        # Catch QtWidget objecto to python
        self.define_widgets()
        # Set the model for the table view
        self.set_model()
        # Filter option changed trigger
        self.filter_changed()
        # Create new study
        self.new_study_button.clicked.connect(self.create_new_study)
        # Open existing study
        self.table.doubleClicked.connect(self.open_existing_study)
        # Update studies table
        self.update_table_button.clicked.connect(self.update_studies_table)

    def load_ui_file(self, path):
        uic.loadUi(path / UI_PATH, self)

    def define_widgets(self):
        # Input components
        self.search_input = self.findChild(QLineEdit, "search_line_edit")
        self.filter_box = self.findChild(QComboBox, "filter_combo_box")
        # Table components
        self.table = self.findChild(QTableView, "apnea_study_table_view")
        self.model = QStandardItemModel()
        self.filterProxyModel = QSortFilterProxyModel()
        # Actions components (buttons)
        self.new_study_button = self.findChild(
            QPushButton, "create_new_study_push_button")
        self.previous_page_button = self.findChild(
            QPushButton, "previous_page_push_button")
        self.update_table_button = self.findChild(
            QPushButton, "update_table_push_button")

    def load_apnea_studies_to_table(self):
        # Retrive all the apnea studies of the patient
        controll_db = ControllDb()
        thread_db = DatabaseThread(
            target=controll_db.select_patient_apena_studies,
            args=(self.id_patient,)
        )
        thread_db.start()
        insert_db_thread_event(thread_db.native_id)
        pacient_info = thread_db.join()
        self.id_apnea_studies_list = []
        # Write all the apneas studies
        for i, row in enumerate(pacient_info):
            # print("ROW:", row)
            # Set the data for each cell
            # (1 = id apnea study, 2 = apnea study status, 3 = study date)
            self.id_apnea_studies_list.append(str(pacient_info[i][0]))
            # Set number of study
            study_number = str(i + 1)
            # Set study status
            status = self.__get_status(row[0])
            # Set study date
            study_date = str(pacient_info[i][2])
            # Write the number, status and study date on their respective column
            self.model.setItem(i, 0, QStandardItem(study_number))
            self.model.setItem(i, 1, QStandardItem(status))
            self.model.setItem(i, 2, QStandardItem(study_date))

    def set_model(self):
        self.model.setHorizontalHeaderLabels(
            ['# Study', 'Status', 'Study Date'])
        self.filterProxyModel.setSourceModel(self.model)
        self.filterProxyModel.setFilterCaseSensitivity(False)
        self.filterProxyModel.setFilterKeyColumn(2)
        self.table.verticalHeader().hide()
        self.table.setModel(self.filterProxyModel)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.filter_box.setCurrentIndex(1)

    def filter_changed(self):
        filter_text = self.filter_box.currentText()
        if filter_text == "Numero de Estudio":
            self.filterProxyModel.setFilterKeyColumn(0)
        if filter_text == "Estatus":
            self.filterProxyModel.setFilterKeyColumn(1)
        if filter_text == "Fecha del Estudio":
            self.filterProxyModel.setFilterKeyColumn(2)

    def create_new_study(self):
        # Create patient objets for future reference
        self.createPatientObject()
        self.stackWindow = StackedRegistrationWidget(self.patient, self.doctor)
        self.stackWindow.report.saveReportButton.clicked.connect(
            self.update_studies_table)

    def updateSearch(self):
        self.load_apnea_studies_to_table()

    def update_studies_table(self):
        self.clean_table()
        self.load_apnea_studies_to_table()

    def clean_table(self):
        self.model.removeRows(0, self.model.rowCount())

    def open_existing_study(self):
        self.createPatientObject()
        # Get index of the study
        apnea_study_index = self.table.currentIndex().row()
        if self.id_patient:
            self.loadPatientData(self.id_patient, apnea_study_index)
            self.loadPatientImage()
            self.load_video()
            self.loadReportData()
            self.load_osa_file()
            self.editWindow = EditWindow(self.patient)

        self.editWindow.imageForm.nextPageButton.clicked.connect(
            self.updateSearch)
        self.editWindow.imageForm2.nextPageButton.clicked.connect(
            self.updateSearch)
        self.editWindow.reportForm.saveReportButton.clicked.connect(
            self.updateSearch)

    def createPatientObject(self):
        self.patient = Patient()
        db_controll = ControllDb()
        db_thread = DatabaseThread(
            target=db_controll.selectAllFromPatient,
            args=(self.id_patient,)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        patient_data = db_thread.join()

        self.patient.doctor_id = self.doctor.id
        self.patient.nss = patient_data[0]
        self.patient.acronym = patient_data[2]
        self.patient.birth_date = patient_data[3]
        self.patient.sex = patient_data[4]
        self.patient.registration_date = patient_data[5]

    def loadPatientData(self, patient_id, apnea_study_index):
        db_controll = ControllDb()
        apnea_studies_thread = DatabaseThread(
            target=db_controll.selectAllApneaStudy,
            args=(self.id_apnea_studies_list[apnea_study_index],)
        )
        apnea_studies_thread.start()
        insert_db_thread_event(apnea_studies_thread.native_id)
        apnea_study = apnea_studies_thread.join()
        self.patient.apnea_study.set_apnea_study(apnea_study)

        # patient.apneaStudy.setApneaStudy(self.database.selectAllApneaStudy(
            # self.id_apnea_studies_list[apnea_study_index]))

        medical_record_thread = DatabaseThread(
            target=db_controll.selectAllFromMedicalRecord,
            args=(self.patient.apnea_study.id,)
        )
        medical_record_thread.start()
        insert_db_thread_event(medical_record_thread.native_id)
        medical_record = medical_record_thread.join()
        self.patient.medical_record.set_medical_record(medical_record)
        
        # patient.medicalRecord.setMedicalRecord(
            # self.database.selectAllFromMedicalRecord(patient.apneaStudy.id))
        
        metrics_thread = DatabaseThread(
            target=db_controll.selectAllFromMetrics,
            args=(self.patient.medical_record.metrics.id,)
        )
        metrics_thread.start()
        insert_db_thread_event(metrics_thread.native_id)
        metrics = metrics_thread.join()
        self.patient.medical_record.metrics.set_metrics(metrics)

        # patient.medicalRecord.metrics.setMetrics(
            # self.database.selectAllFromMetrics(patient.medicalRecord.metrics.id))
        
        vital_signs_thread = DatabaseThread(
            target=db_controll.selectAllFromVitalSigns,
            args=(self.patient.medical_record.vital_sign.id,)
        )
        vital_signs_thread.start()
        insert_db_thread_event(vital_signs_thread.native_id)
        vital_signs = vital_signs_thread.join()
        self.patient.medical_record.vital_sign.set_vital_sings(vital_signs)

        # patient.medicalRecord.vitalSign.setVitalSings(
            # self.database.selectAllFromVitalSigns(patient.medicalRecord.vitalSign.id))
        
        comorbidity_thread = DatabaseThread(
            target=db_controll.selectAllFromCharlsonComorbidity,
            args=(self.patient.medical_record.comorbility.id,)
        )
        comorbidity_thread.start()
        insert_db_thread_event(comorbidity_thread.native_id)
        comorbidity = comorbidity_thread.join()
        self.patient.medical_record.comorbility.set_comorbility(comorbidity)

        # patient.medicalRecord.comorbility.setComorbility(
            # self.database.selectAllFromCharlsonComorbidity(patient.medicalRecord.comorbility.id))
        
        record_thread = DatabaseThread(
            target=db_controll.selectAllFromHistory,
            args=(self.patient.medical_record.history.id,)
        )
        record_thread.start()
        insert_db_thread_event(record_thread.native_id)
        record = record_thread.join()
        self.patient.medical_record.history.set_history(record)

        # patient.medicalRecord.history.setHistory(
            # self.database.selectAllFromHistory(patient.medicalRecord.history.id))
        
        aids_thread = DatabaseThread(
            target=db_controll.selectAllFromAuxDiagnostic,
            args=(self.patient.medical_record.aux_diagnostics.id,)
        )
        aids_thread.start()
        insert_db_thread_event(aids_thread.native_id)
        aids = aids_thread.join()
        self.patient.medical_record.aux_diagnostics.set_auxiliary_diagnostic(aids)

        # patient.medicalRecord.auxDiagnostics.setAuxiliaryDiagnostic(
            # self.database.selectAllFromAuxDiagnostic(patient.medicalRecord.auxDiagnostics.id))

    def loadPatientImage(self):
        db_multimedia = MultimediaDb()
        front_photo_thread = DatabaseThread(
            target=db_multimedia.get_front_photo_data,
            args=(self.patient.apnea_study.id,)
        )
        front_photo_thread.start()
        insert_db_thread_event(front_photo_thread.native_id)
        front_photo = front_photo_thread.join()

        lateral_photo_thread = DatabaseThread(
            target=db_multimedia.get_lateral_photo_data,
            args=(self.patient.apnea_study.id,)
        )
        lateral_photo_thread.start()
        insert_db_thread_event(lateral_photo_thread.native_id)
        lateral_photo = lateral_photo_thread.join()

        # frontPic = self.database.selectTagPicture(patient.apneaStudy.id, 0)
        # sidePic = self.database.selectTagPicture(patient.apneaStudy.id, 1)
        if front_photo:
            self.patient.apnea_study.front_photo.set_picture(front_photo)
            # patient.apneaStudy.picture.setPicture(
                # self.database.selectTagPicture(patient.apneaStudy.id, 0))
            # patient.apneaStudy.picture.print()
        else:
            self.patient.apnea_study.front_photo.id = BLANK

        if lateral_photo:
            self.patient.apnea_study.lateral_photo.set_picture(lateral_photo)
            # patient.apneaStudy.profileImg.setPicture(
                # self.database.selectTagPicture(patient.apneaStudy.id, 1))
            # patient.apneaStudy.profileImg.print()
        else:
            self.patient.apnea_study.lateral_photo.id = BLANK
    
    def load_video(self):
        db_multimedia = MultimediaDb()
        video_thread = DatabaseThread(
            target=db_multimedia.get_video_data,
            args=(self.patient.apnea_study.id,)
        )
        video_thread.start()
        insert_db_thread_event(video_thread.native_id)
        video = video_thread.join()

        if video:
            self.patient.apnea_study.video.set_video(video)
        else:
            self.patient.apnea_study.video.id = BLANK

    def loadReportData(self):
        db_controll = ControllDb()
        pdf_thread = DatabaseThread(
            target=db_controll.selectAllReport,
            args=(self.patient.apnea_study.id,)
        )
        pdf_thread.start()
        insert_db_thread_event(pdf_thread.native_id)
        pdf = pdf_thread.join()

        if pdf:
            self.patient.apnea_study.report.set_report(pdf)
        else:
            self.patient.apnea_study.report.id = BLANK

    def load_osa_file(self):
        db_multimedia = MultimediaDb()
        osa_thread = DatabaseThread(
            target=db_multimedia.get_osa_data,
            args=(self.patient.apnea_study.id,)
        )
        osa_thread.start()
        insert_db_thread_event(osa_thread.native_id)
        osa = osa_thread.join()

        if osa:
            self.patient.apnea_study.edf.set_edf(osa)
        else:
            self.patient.apnea_study.edf.id = BLANK

    def __get_status(self, apnea_id: int) -> str:
        db_multimedia = MultimediaDb()
        db_controll = ControllDb()
        lateral_photo_thread = DatabaseThread(
            target=db_multimedia.get_front_photo_data,
            args=(apnea_id,)
        )
        front_photo_thread = DatabaseThread(
            target=db_multimedia.get_lateral_photo_data,
            args=(apnea_id,)
        )
        video_thread = DatabaseThread(
            target=db_multimedia.get_video_data,
            args=(apnea_id,)
        )
        osa_thread = DatabaseThread(
            target=db_multimedia.get_osa_data,
            args=(apnea_id,)
        )
        pdf_thread = DatabaseThread(
            target=db_controll.status_pdf_file,
            args=(apnea_id,)
        )
        front_photo_thread.start()
        lateral_photo_thread.start()
        video_thread.start()
        osa_thread.start()
        pdf_thread.start()

        insert_db_thread_event(front_photo_thread.native_id)
        insert_db_thread_event(lateral_photo_thread.native_id)
        insert_db_thread_event(video_thread.native_id)
        insert_db_thread_event(osa_thread.native_id)
        insert_db_thread_event(pdf_thread.native_id)

        front = front_photo_thread.join()
        profile = lateral_photo_thread.join()
        video_status = video_thread.join()
        osa_status = osa_thread.join()
        pdf_status = pdf_thread.join()

        # results = self.database.selectAllReport(apnea_id)
        status_list = list()
        # Images status
        if ((not front) or (not profile)):
            status_list.append(IMAGE_STATUS)
        # Video status
        if not video_status:
            status_list.append(VIDEO_STATUS)
        # PDF status
        if not pdf_status:
            status_list.append(PDF_STATUS)
        # OSA status
        if not osa_status:
            status_list.append(OSA_STATUS)

        status = BLANK
        if len(status_list) == 0:
            status = COMPLETE_STATUS + '#'
        else:
            for stat in status_list:
                status += stat + ','

        return status[:-1]
