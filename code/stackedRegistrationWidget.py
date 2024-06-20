from PyQt5 import uic
from PyQt5.QtWidgets import QStackedWidget, QMainWindow

import pathlib

from medicalRecordWidget import MedicalRecordForm
from imageWidget import ImageWidget
from VideoConvert import VideoConvert
from reportWidget import ReportFormWidget

UI_PATH = "ui/stackedRegistrationWindow.ui"

IS_NOT_EDIT = False


class StackedRegistrationWidget(QMainWindow):
    def __init__(self, patient, doctor):
        super(StackedRegistrationWidget, self).__init__()
        self.isPatientRegistered = False
        self.patient = patient
        self.doctor = doctor

        self.__loadUiFile(pathlib.Path(__file__).parent)
        self.__instantiateWidgets()
        self.__addWidgets()
        self.__defineButtons()
        self.__personalize()

        self.show()

    def __loadUiFile(self, path):
        uic.loadUi(path / UI_PATH, self)

    def __instantiateWidgets(self):
        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.registration = MedicalRecordForm(self.patient, IS_NOT_EDIT)
        self.front_photo = ImageWidget(self.patient, IS_NOT_EDIT)
        self.lateral_photo = ImageWidget(self.patient, IS_NOT_EDIT)
        self.video = VideoConvert(self.patient, IS_NOT_EDIT)
        self.report = ReportFormWidget(self.patient, IS_NOT_EDIT)

    def __addWidgets(self):
        self.stackedWidget.addWidget(self.registration)
        self.stackedWidget.addWidget(self.front_photo)
        self.stackedWidget.addWidget(self.lateral_photo)
        # Add video widget to the stackwidget object. (Lineal flow)
        self.stackedWidget.addWidget(self.video)
        self.stackedWidget.addWidget(self.report)

    def __defineButtons(self):

        self.registration.nextPageButton.clicked.connect(self.formValidation)

        self.front_photo.nextPageButton.clicked.connect(self.nextPage)
        self.front_photo.previousPageButton.clicked.connect(self.previousPage)
        self.lateral_photo.nextPageButton.clicked.connect(self.nextPage)
        self.lateral_photo.previousPageButton.clicked.connect(self.previousPage)

        self.video.next_page_button.clicked.connect(self.nextPage)
        self.video.previous_page_button.clicked.connect(self.previousPage)

        self.report.saveReportButton.clicked.connect(
            self.close_apnea_study_window)

    def formValidation(self):
        if self.registration.validate_fields():
            if self.registration.validate_metrics():
                self.nextPage()

    def __personalize(self):
        self.front_photo.tag.setCurrentText("Front")
        self.front_photo.tag.setEnabled(False)
        self.lateral_photo.tag.setCurrentText("Lateral")
        self.lateral_photo.tag.setEnabled(False)

    def nextPage(self):
        self.isPatientRegistered = True
        self.currentIndex = self.stackedWidget.currentIndex()
        if self.currentIndex == 1 and self.front_photo.pixmap.isNull():
            self.front_photo.errorOnSaving()
        if self.currentIndex == 2 and self.lateral_photo.pixmap.isNull():
            self.lateral_photo.errorOnSaving()
        # Verify if the user skipped the load video page
        if self.currentIndex == 3 and self.video.path_dst == "":
            # Show video load error message
            self.video.error_on_saving()
        if self.currentIndex < self.stackedWidget.count():
            self.registration.clear()
            self.stackedWidget.setCurrentIndex(self.currentIndex+1)

    def previousPage(self):
        self.currentIndex = self.stackedWidget.currentIndex()
        if self.currentIndex > 0:
            self.stackedWidget.setCurrentIndex(self.currentIndex-1)

    def close_apnea_study_window(self):
        self.close()

    def clearAll(self):
        self.registration.deleteLater()
        self.front_photo.deleteLater()
        self.lateral_photo.deleteLater()
        self.video.deleteLater()
        self.report.deleteLater()
        self.stackedWidget.deleteLater()
