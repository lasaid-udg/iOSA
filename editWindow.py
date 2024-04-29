from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QAction

import pathlib
import pandas as pd

from medicalRecordWidget import MedicalRecordForm
from imageWidget import ImageWidget
from VideoConvert import VideoConvert
from reportWidget import ReportFormWidget

UI_PATH = "ui/editWindow.ui"


class EditWindow(QMainWindow):
    def __init__(self, patient):
        super().__init__()

        self.loadUiFile(pathlib.Path(__file__).parent)
        self.patient = patient

        self.tabWidget = self.findChild(QTabWidget, "tabWidget")
        self.actionExit = self.findChild(QAction, "actionExit")

        self.registrationForm = MedicalRecordForm(self.patient, True)
        self.imageForm = ImageWidget(self.patient, True)
        self.imageForm2 = ImageWidget(self.patient, True)
        self.video = VideoConvert(self.patient, True)
        self.reportForm = ReportFormWidget(self.patient, True)

        self.addTabs()
        self.changeUi()
        self.loadDataToWindows()
        self.show()

    def loadUiFile(self, path):
        uic.loadUi(path / UI_PATH, self)

    def addTabs(self):
        self.tabWidget.addTab(self.registrationForm, "Medical Record")
        self.tabWidget.addTab(self.imageForm, "Frontal Image")
        self.tabWidget.addTab(self.imageForm2, "Lateral Image")
        self.tabWidget.addTab(self.video, "Video")
        self.tabWidget.addTab(self.reportForm, "Polygraphy")

    def changeUi(self):
        self.registrationForm.nextPageButton.setText("Save")
        self.imageForm.previousPageButton.hide()
        self.imageForm.nextPageButton.setText("Save")
        self.imageForm2.previousPageButton.hide()
        self.imageForm2.nextPageButton.setText("Save")
        # self.video.previous_page_button.hide()
        # self.video.next_page_button.setText("Guardar")

    def loadDataToWindows(self):
        self.registrationForm.fillData()
        self.loadImage("Front")
        self.loadImage("Lateral")
        self.load_video()
        self.reportForm.fillData()

    def loadImage(self, tag):
        if tag == "Front":
            self.loadImageInformation(self.patient.apnea_study.front_photo,
                                      self.imageForm, tag)
        else:
            self.loadImageInformation(self.patient.apnea_study.lateral_photo,
                                      self.imageForm2, tag)

    def loadImageInformation(self, picture, form, tagText):
        form.tag.setCurrentText(tagText)
        form.tag.setEnabled(False)
        if not picture.id == "":
            # print("---------- edit window ----------")
            form.path = str(picture.path)
            form.coordinates = self.jsonToList(picture.picture_json)
            form.setPixmap()
            form.drawPointsOnScene()
            form.getMeasurements()

    def jsonToList(self, json):
        # print(json)
        df = pd.DataFrame.from_dict(json)
        # print(df)
        coord = []
        for index, row in df.iterrows():
            r = [row['X'], row['Y'], 0, index]
            coord.append(r)
        return coord

    def load_video(self):
        if self.patient.apnea_study.video.id != "":
            self.video.edit_flag = True
            self.video.path_video = [self.patient.apnea_study.video.path, ""]
            self.video.start_video_convertion()


if __name__ == '__main__':
    app = QApplication([])
    window = EditWindow()
    window.show()
    app.exec_()
