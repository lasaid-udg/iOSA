from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QTextEdit, QFileDialog

import pathlib
import re
import os
import shutil

from pdf_data_extraction import ExtractPdfData
from log import Log
from database import ControllDb, MultimediaDb, DatabaseThread
from database import insert_db_thread_event

UI_PATH = "ui/reportWidget.ui"
OSA_PATH = "multimedia\osa"
OSA_EXTENCION = ".osa"
EVENT_PDF = "PDF Data Extracted"
BLANK = ''
NUMBER_RGX = "\d*"
PERCENTAGE_RGX = "\d*%$"


class ReportFormWidget(QWidget):
    def __init__(self, patient, is_edit):
        super(ReportFormWidget, self).__init__()
        self._is_edit = is_edit
        self._patient = patient
        self.edf_path = BLANK
        self.path_edf = [BLANK, BLANK]

        self.__loadUiFile(pathlib.Path(__file__).parent)
        self.__os_dir()
        self.__defineWidgets()
        self.__defineButton()

    def __loadUiFile(self, path):
        uic.loadUi(path / UI_PATH, self)

    def __defineWidgets(self):
        # Buttons
        self.loadReportButton = self.findChild(
            QPushButton, "loadReportPushButton")
        self.saveReportButton = self.findChild(QPushButton, "updatePushButton")
        self.loadEDFFileButton = self.findChild(
            QPushButton, "loadEDFFilePushButton")
        self.editEDFFileButton = self.findChild(
            QPushButton, "editEDFFilepushButton")

        # QLineEdits fields
        self.IAH = self.findChild(QLineEdit, "IAHLineEdit")
        self.rpm = self.findChild(QLineEdit, "rpmLineEdit")
        self.IR = self.findChild(QLineEdit, "IRLineEdit")
        self.respirations = self.findChild(QLineEdit, "respirationsLineEdit")
        self.apneasIndex = self.findChild(QLineEdit, "apneasIndexLineEdit")
        self.apneas = self.findChild(QLineEdit, "apneasLineEdit")
        self.IAI = self.findChild(QLineEdit, "IAILineEdit")
        self.indeterminatedApneas = self.findChild(
            QLineEdit, "indeterminatedApneasLineEdit")
        self.IAO = self.findChild(QLineEdit, "IAOLineEdit")
        self.obstructiveApneas = self.findChild(
            QLineEdit, "obstructiveApneasLineEdit")
        self.IAC = self.findChild(QLineEdit, "IACLineEdit")
        self.centralApneas = self.findChild(QLineEdit, "centralApneasLineEdit")
        self.IAM = self.findChild(QLineEdit, "IAMLineEdit")
        self.mixedApneas = self.findChild(QLineEdit, "mixedApneasLineEdit")
        self.hypopneaIndex = self.findChild(QLineEdit, "hypopneaIndexLineEdit")
        self.hypoapneas = self.findChild(QLineEdit, "hypoapneasLineEdit")
        self.lfPercentage = self.findChild(QLineEdit, "lfPercentageLineEdit")
        self.lf = self.findChild(QLineEdit, "lfLineEdit")
        self.lrPercentage = self.findChild(QLineEdit, "lrPercentageLineEdit")
        self.lr = self.findChild(QLineEdit, "lrLineEdit")
        self.snoringEvents = self.findChild(QLineEdit, "snoringEventsLineEdit")
        self.IDO = self.findChild(QLineEdit, "IDOLineEdit")
        self.desaturationsNumber = self.findChild(
            QLineEdit, "desaturationsNumberLineEdit")
        self.averageSaturation = self.findChild(
            QLineEdit, "averageSaturationLineEdit")
        self.saturation90Min = self.findChild(
            QLineEdit, "saturation90MinLineEdit")
        self.saturation90Per = self.findChild(
            QLineEdit, "saturation90PerLineEdit")
        self.minorDesaturation = self.findChild(
            QLineEdit, "minorDesaturationLineEdit")
        self.saturation85Min = self.findChild(
            QLineEdit, "saturation85MinLineEdit")
        self.saturation85Per = self.findChild(
            QLineEdit, "saturation85PerLineEdit")
        self.lowestSaturation = self.findChild(
            QLineEdit, "lowestSaturationLineEdit")
        self.saturation80Min = self.findChild(
            QLineEdit, "saturation80MinLineEdit")
        self.saturation80Per = self.findChild(
            QLineEdit, "saturation80PerLineEdit")
        self.basalSaturation = self.findChild(
            QLineEdit, "basalSaturationLineEdit")
        self.minimumPulseRate = self.findChild(
            QLineEdit, "minimumPulseRateLineEdit")
        self.maximumPulseRate = self.findChild(
            QLineEdit, "maximumPulseRateLineEdit")
        self.averagePulseRate = self.findChild(
            QLineEdit, "averagePulseRateLineEdit")
        self.CSR = self.findChild(QLineEdit, "CSRLineEdit")
        self.defaultApnea = self.findChild(QLineEdit, "defaultApneaLineEdit")
        self.defaultHypopnea = self.findChild(
            QLineEdit, "defaultHypopneaLineEdit")
        self.defaultSnoring = self.findChild(
            QLineEdit, "defaultSnoringLineEdit")
        self.defaultDesaturation = self.findChild(
            QLineEdit, "defaultDesaturationLineEdit")
        self.defaultCSR = self.findChild(QLineEdit, "defaultCSRLineEdit")
        self.comments = self.findChild(QTextEdit, "commentsTextEdit")
        self.evaluation_duration = self.findChild(
            QLineEdit, "evaluation_duration_line_edit")

    def __defineButton(self):
        self.loadReportButton.clicked.connect(self.selectReport)
        self.loadEDFFileButton.clicked.connect(self.select_edf)
        self.saveReportButton.clicked.connect(self.insertOrUpdate)

    def selectReport(self):
        # Fer QFileDialog path:
        # self.fname = QFileDialog.getOpenFileName(self, "Seleccionar Reporte", r"C:\Users\Nineteen002\Documents\School\SA2\Photos\Qr", "PDF Files (*.pdf)")

        # Eric QFileDialog path:
        self.fname = QFileDialog.getOpenFileName(self, "Seleccionar Reporte", str(
            pathlib.Path("reportWidget.py").parent.absolute()), "PDF Files (*.pdf)")

        if self.fname[0] != "":
            # print("Report Selected: " + self.fname[0])

            try:
                # self.report = ExtractPDFData(self.fname[0])

                self.report = ExtractPdfData(self.fname[0])
                self.report.extract_data()

                log = Log()
                log.insert_log_info(EVENT_PDF)
            except Exception as e:
                log = Log()
                log.insert_log_error()
                self.__pdf_data_extraction_error()

            self.generateReport()

        else:
            pass

    def select_edf(self):
        self.path_edf = QFileDialog.getOpenFileName(self, "Seleccionar Video", str(
            pathlib.Path().absolute()), "EDF/TXT Files (*.edf *.osa)")

        if self.path_edf[0] != "":
            # print("File Selected: " + self.path_edf[0])

            self.osa_file_loaded()
        else:
            pass

    def insertOrUpdate(self):
        if self._is_edit:
            if self._patient.apnea_study.report.id != "":
                self.packData()
                self.updateReport()
            else:
                self.insertReport()

            if self._patient.apnea_study.edf.id != "":
                self.update_osa()
            else:
                self.insert_osa()

        else:
            self.insertReport()
            self.insert_osa()

        if self.path_edf[0] != "":
            self.copy_edf_file()

    def insertReport(self):
        if self._is_edit:
            # print("----- INSERT POST CREATIONS -----")
            self.packData()
            self.tupleData.insert(0, self._patient.apnea_study.id)
            # Error
            self.database.insertReport(tuple(self.tupleData))

        else:
            self.packData()

            if self.checkGeneratedReport():
                self.tupleData.insert(0, self._patient.apnea_study.id)

                tuple_data = tuple(self.tupleData)

                db_controll = ControllDb()
                db_thread = DatabaseThread(
                    target=db_controll.insertReport,
                    args=(tuple_data,)
                )
                db_thread.start()
                insert_db_thread_event(db_thread.native_id)

                pdf_id = db_thread.join()

    def insert_osa(self):
        if self._is_edit:
            tuple_data = [self._patient.apnea_study.id, self.edf_path]
            self.edf_path = OSA_PATH + r"\\" + \
                str(self._patient.apnea_study.id) + OSA_EXTENCION
            # Error
            self.database.insert_edf_file(tuple(tuple_data))

        else:
            self.edf_path = OSA_PATH + r"\\" + \
                str(self._patient.apnea_study.id) + OSA_EXTENCION

            if self.check_loaded_edf_file():
                tuple_data = [self._patient.apnea_study.id, self.edf_path]

                multimedia_db = MultimediaDb()
                db_thread = DatabaseThread(
                    target=multimedia_db.insert_osa,
                    args=(tuple(tuple_data),)
                )
                db_thread.start()
                insert_db_thread_event(db_thread.native_id)
                
                osa_id = db_thread.join()

    def updateReport(self):
        self.packData()
        self.tupleData.append(self._patient.apnea_study.report.id)

        db_controll = ControllDb()
        db_thread = DatabaseThread(
            target=db_controll.updateReport,
            args=(tuple(self.tupleData),)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        db_thread.join()

    def update_osa(self):
        self.edf_path = OSA_PATH + r"\\" + \
            str(self._patient.apnea_study.id) + OSA_EXTENCION

        tuple_data = [self._patient.apnea_study.edf.id, self.edf_path]
        apnea_study_id = self._patient.apnea_study.id

        db_multimedia = MultimediaDb()
        db_thread = DatabaseThread(
            target=db_multimedia.update_osa,
            args=(apnea_study_id, tuple(tuple_data))
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        db_thread.join()

    def copy_edf_file(self):
        home_path = str(pathlib.Path().absolute())
        if self._is_edit:
            fname = home_path + "\\" + OSA_PATH + "\\" + \
                str(self._patient.apnea_study.id) + OSA_EXTENCION
            # print(self.path_edf[0])

            try:
                # os.system(f"copy {str(self.path_edf[0])} {fname}")
                shutil.copyfile(str(self.path_edf[0]), fname)
            except shutil.SameFileError:
                pass

        else:
            fname = home_path + "\\" + OSA_PATH + "\\" + \
                str(self._patient.apnea_study.id) + OSA_EXTENCION
            # print(self.path_edf[0])

            try:
                # os.system(f"copy {str(self.path_edf[0])} {fname}")
                shutil.copyfile(str(self.path_edf[0]), fname)
            except shutil.SameFileError:
                pass

    def fillData(self):
        if self._patient.apnea_study.report.id != "":

            self.IAH.setText(self._patient.apnea_study.report.iah)
            self.rpm.setText(self._patient.apnea_study.report.rpm)
            self.IR.setText(self._patient.apnea_study.report.ir)
            self.respirations.setText(self._patient.apnea_study.report.respirations)
            self.apneasIndex.setText(self._patient.apnea_study.report.apneas_index)
            self.apneas.setText(self._patient.apnea_study.report.apneas)
            self.IAI.setText(self._patient.apnea_study.report.iai)
            self.indeterminatedApneas.setText(
                self._patient.apnea_study.report.indeterminated_apneas)
            self.IAO.setText(self._patient.apnea_study.report.iao)
            self.obstructiveApneas.setText(
                self._patient.apnea_study.report.obstructive_apneas)
            self.IAC.setText(self._patient.apnea_study.report.iac)
            self.centralApneas.setText(self._patient.apnea_study.report.central_apneas)
            self.IAM.setText(self._patient.apnea_study.report.iam)
            self.mixedApneas.setText(self._patient.apnea_study.report.mixed_apneas)
            self.hypopneaIndex.setText(self._patient.apnea_study.report.hypopnea_index)
            self.hypoapneas.setText(self._patient.apnea_study.report.hypoapneas)
            self.lfPercentage.setText(self._patient.apnea_study.report.lf_percentage)
            self.lf.setText(self._patient.apnea_study.report.lf)
            self.lrPercentage.setText(self._patient.apnea_study.report.lr_percentage)
            self.lr.setText(self._patient.apnea_study.report.lr)
            self.snoringEvents.setText(self._patient.apnea_study.report.snoring_events)
            self.IDO.setText(self._patient.apnea_study.report.ido)
            self.desaturationsNumber.setText(
                self._patient.apnea_study.report.desaturations_number)
            self.averageSaturation.setText(
                self._patient.apnea_study.report.average_saturation)
            self.saturation90Min.setText(
                self._patient.apnea_study.report.saturation_90_min)
            self.saturation90Per.setText(
                self._patient.apnea_study.report.saturation_90_per)
            self.minorDesaturation.setText(
                self._patient.apnea_study.report.minor_desaturation)
            self.saturation85Min.setText(
                self._patient.apnea_study.report.saturation_85_min)
            self.saturation85Per.setText(
                self._patient.apnea_study.report.saturation_85_per)
            self.lowestSaturation.setText(
                self._patient.apnea_study.report.lowest_saturation)
            self.saturation80Min.setText(
                self._patient.apnea_study.report.saturation_80_min)
            self.saturation80Per.setText(
                self._patient.apnea_study.report.saturation_80_per)
            self.basalSaturation.setText(
                self._patient.apnea_study.report.basal_saturation)
            self.minimumPulseRate.setText(
                self._patient.apnea_study.report.minimum_pulse_rate)
            self.maximumPulseRate.setText(
                self._patient.apnea_study.report.maximum_pulse_rate)
            self.averagePulseRate.setText(
                self._patient.apnea_study.report.average_pulse_rate)
            self.CSR.setText(self._patient.apnea_study.report.csr)
            self.defaultApnea.setText(self._patient.apnea_study.report.default_apnea)
            self.defaultHypopnea.setText(
                self._patient.apnea_study.report.default_hypopnea)
            self.defaultSnoring.setText(
                self._patient.apnea_study.report.default_snoring)
            self.defaultDesaturation.setText(
                self._patient.apnea_study.report.default_desaturation)
            self.defaultCSR.setText(self._patient.apnea_study.report.default_csr)
            self.comments.setText(self._patient.apnea_study.report.comments)
            self.evaluation_duration.setText(
                self._patient.apnea_study.report.evaluation_duration)

        if self._patient.apnea_study.edf.id != "":
            # print("OSA ID:", patient.apnea_study.edf.id)
            self.osa_file_loaded()

    def packData(self):
        try:
            saturacionA = re.search("\d*", self.saturation90Min.text()).group()
            saturacionB = re.search("\d*", self.saturation85Min.text()).group()
            saturacionC = re.search("\d*", self.saturation80Min.text()).group()
        except:
            saturacionA = ''
            saturacionB = ''
            saturacionC = ''

        self.tupleData = [
            self.IAH.text(),
            self.rpm.text(),
            self.IR.text(),
            self.respirations.text(),
            self.apneasIndex.text(),
            self.apneas.text(),
            self.IAI.text(),
            self.indeterminatedApneas.text(),
            self.IAO.text(),
            self.obstructiveApneas.text(),
            self.IAC.text(),
            self.centralApneas.text(),
            self.IAM.text(),
            self.mixedApneas.text(),
            self.hypopneaIndex.text(),
            self.hypoapneas.text(),
            self.lfPercentage.text(),
            self.lf.text(),
            self.lrPercentage.text(),
            self.lr.text(),
            self.snoringEvents.text(),
            self.IDO.text(),
            self.desaturationsNumber.text(),
            self.averageSaturation.text(),
            saturacionA,
            self.saturation90Per.text(),
            self.minorDesaturation.text(),
            saturacionB,
            self.saturation85Per.text(),
            self.lowestSaturation.text(),
            saturacionC,
            self.saturation80Per.text(),
            self.basalSaturation.text(),
            self.minimumPulseRate.text(),
            self.maximumPulseRate.text(),
            self.averagePulseRate.text(),
            self.CSR.text(),
            self.defaultApnea.text(),
            self.defaultHypopnea.text(),
            self.defaultSnoring.text(),
            self.defaultDesaturation.text(),
            self.defaultCSR.text(),
            self.comments.toPlainText(),
            self.evaluation_duration.text()
        ]

    def generateReport(self):
        # print(self.report.extracted_data)
        self.indeterminatedApneas.setText(self.__parse_value(NUMBER_RGX,
                                                             self.report.extracted_data["IndeterminateApneas"]))

        self.obstructiveApneas.setText(self.__parse_value(NUMBER_RGX,
                                                          self.report.extracted_data["ObstructiveApneas"]))

        self.centralApneas.setText(self.__parse_value(NUMBER_RGX,
                                                      self.report.extracted_data["CentralApneas"]))

        self.mixedApneas.setText(self.__parse_value(NUMBER_RGX,
                                                    self.report.extracted_data["MixedApneas"]))

        self.saturation90Min.setText(self.__parse_value(NUMBER_RGX,
                                                        self.report.extracted_data["90%Saturation"])+" min")

        self.saturation90Per.setText(self.__parse_value(PERCENTAGE_RGX,
                                                        self.report.extracted_data["90%Saturation"]))

        self.saturation85Min.setText(self.__parse_value(NUMBER_RGX,
                                                        self.report.extracted_data["85%Saturation"])+" min")

        self.saturation85Per.setText(self.__parse_value(PERCENTAGE_RGX,
                                                        self.report.extracted_data["85%Saturation"]))

        self.saturation80Min.setText(self.__parse_value(NUMBER_RGX,
                                                        self.report.extracted_data["80%Saturation"])+" min")

        self.saturation80Per.setText(self.__parse_value(PERCENTAGE_RGX,
                                                        self.report.extracted_data["80%Saturation"]))

        self.CSR.setText(self.__parse_value(NUMBER_RGX,
                                            self.report.extracted_data["CSR"]))

        self.IAH.setText(self.report.extracted_data["IAH"])
        self.rpm.setText(self.report.extracted_data["AVERAGE_RPM"])
        self.IR.setText(self.report.extracted_data["IR"])
        self.respirations.setText(self.report.extracted_data["Respirations"])
        self.apneasIndex.setText(self.report.extracted_data["ApneaIndex"])
        self.apneas.setText(self.report.extracted_data["Apneas"])
        self.IAI.setText(self.report.extracted_data["IAI"])
        self.IAO.setText(self.report.extracted_data["IAO"])
        self.IAC.setText(self.report.extracted_data["IAC"])
        self.IAM.setText(self.report.extracted_data["IAM"])
        self.hypopneaIndex.setText(self.report.extracted_data["HypopneaIndex"])
        self.hypoapneas.setText(self.report.extracted_data["Hypopnea"])
        self.lfPercentage.setText(self.report.extracted_data["%Lf"])
        self.lf.setText(self.report.extracted_data["Lf"])
        self.lrPercentage.setText(self.report.extracted_data["%LR"])
        self.lr.setText(self.report.extracted_data["LR"])
        self.snoringEvents.setText(self.report.extracted_data["SnoringEvents"])
        self.IDO.setText(self.report.extracted_data["IDO"])
        self.desaturationsNumber.setText(
            self.report.extracted_data["DesaturationsNumber"])
        self.averageSaturation.setText(
            self.report.extracted_data["AverageSaturation"])
        self.minorDesaturation.setText(
            self.report.extracted_data["MinorDesaturation"])
        self.lowestSaturation.setText(
            self.report.extracted_data["LowestSaturation"])
        self.basalSaturation.setText(
            self.report.extracted_data["BasalSaturation"])
        self.minimumPulseRate.setText(
            self.report.extracted_data["MinimumPulseRate"])
        self.maximumPulseRate.setText(
            self.report.extracted_data["MaximumPulseRate"])
        self.averagePulseRate.setText(
            self.report.extracted_data["AveragePulseRate"])
        self.defaultApnea.setText(self.report.extracted_data["DefaultApnea"])
        self.defaultHypopnea.setText(
            self.report.extracted_data["DefaultHypopnea"])
        self.defaultSnoring.setText(
            self.report.extracted_data["DefaultSnoring"])
        self.defaultDesaturation.setText(
            self.report.extracted_data["DefaultDesaturation"])
        self.defaultCSR.setText(self.report.extracted_data["DefaultCSR"])
        self.comments.setPlainText(self.report.extracted_data["Comments"])
        self.evaluation_duration.setText(
            self.report.extracted_data["EvaluationDuration"])

    def __parse_value(self, rgx: str, value: str) -> None:
        try:
            # print(value)
            match = re.search(rgx, value).group()
        except Exception as e:
            # print(e)
            match = BLANK
            log = Log()
            log.insert_log_error(value)

        return match

    def osa_file_loaded(self):
        self.editEDFFileButton.setStyleSheet("background-color: rgb(0,255,0);")
        self.editEDFFileButton.setText("OSA File Uploaded")

        if not self._is_edit:
            msg = QMessageBox()
            msg.setWindowTitle("File Uploaded")
            msg.setText("OSA File Uploaded")
            msg.exec_()

    def __pdf_data_extraction_error(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error al Cargar PDF")
        msg.setText("Hubo un error al cargar el PDF")
        msg.exec_()

    def checkGeneratedReport(self):
        # print(self.tupleData)
        for data in self.tupleData[1:]:
            if data != "":
                return True
        # If all data is empty don't insert or update
        return False

    def check_loaded_edf_file(self):
        if self.path_edf[0] == "":
            return False
        else:
            return True

    def __os_dir(self):
        try:
            os.makedirs(os.path.normpath(OSA_PATH), exist_ok=False)
        except (FileExistsError, OSError):
            # print("Dirr already exist")
            self.insert_directory_error()

    def insert_directory_error(self) -> None:
        log = Log()
        log.insert_log_error()
