from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QSpinBox, QMessageBox
from PyQt5.QtWidgets import QDoubleSpinBox, QSlider, QTextEdit

import pathlib
import datetime
import re

from database import ControllDb, DatabaseThread, insert_db_thread_event

UI_PATH = "ui/MedicalRecordWidget.ui"
YES = 1
NULL = "NULL"
NONE = None
TRUE = True
FALSE = False
ZERO = 0


class MedicalRecordForm(QWidget):
    def __init__(self, patient, is_edit):
        super(MedicalRecordForm, self).__init__()
        self.is_edit = is_edit
        self.patient = patient
        self.flag = True

        self.__loadUiFile(pathlib.Path(__file__).parent)
        self.__defineWidgets()
        # self.lazyFill()
        self.__operations()

        self.nextPageButton.clicked.connect(self.__save)

    def __loadUiFile(self, path):
        uic.loadUi(path / UI_PATH, self)

    def __defineWidgets(self):
        self.nextPageButton = self.findChild(QPushButton, "nextPageButton")
        # WORKAROUND
        self.nextPageButton.setText("Guardar y Continuar")

        # Weight/Height/BMI
        self.patientweight = self.findChild(QLineEdit, "weightLineEdit")
        self.patientheight = self.findChild(QLineEdit, "heightLineEdit")
        self.neckCircumference = self.findChild(
            QLineEdit, "neckCircumferenceLineEdit")
        self.patientBmi = self.findChild(QLineEdit, "BMILineEdit")

        # Vital Signs
        self.CF = self.findChild(QSpinBox, "heartRateSpinBox")
        self.RF = self.findChild(QSpinBox, "respiratoryFrequencySpinBox")
        self.OS = self.findChild(QSpinBox, "oxigenSaturationSpinBox")
        self.highArterialTension = self.findChild(
            QSpinBox, "systolic_blood_pressure_spin_box")
        self.lowArterialTension = self.findChild(
            QSpinBox, "diastolic_blood_pressure_spin_box")
        self.temperature = self.findChild(
            QDoubleSpinBox, "temperatureDoubleSpinBox")

        # History
        self.OxigenUse = self.findChild(QSlider, "oxigenUseHorizontalSlider")
        self.smoker = self.findChild(QSlider, "smokerHorizontalSlider")
        self.exsmoker = self.findChild(QSlider, "exsomkerHorizontalSlider")
        self.hypertension = self.findChild(
            QSlider, "hypertensionHorizontalSlider")
        self.snoring = self.findChild(QSlider, "snoringHorizontalSlider")
        self.witnessedApneas = self.findChild(
            QSlider, "witnessedApneasHorizontalSlider")
        self.chronicFatigue = self.findChild(
            QSlider, "chronicFatigueHorizontalSlider")
        self.medicines = self.findChild(QTextEdit, "medicinesTextEdit")

        # Comorbility Charlson
        self.CI = self.findChild(
            QSlider, "cardiacInsufficiencyHorizontalSlider")
        self.HCVA = self.findChild(
            QSlider, "historyCerebralVascularAccidentHorizontalSlider")
        self.PVD = self.findChild(
            QSlider, "peripherialVascularDiseaseHorizontalSlider")
        self.dementia = self.findChild(QSlider, "dementiaHorizontalSlider")
        self.EPOC = self.findChild(QSlider, "EPOCHorizontalSlider")
        self.CTD = self.findChild(
            QSlider, "connectiveTissueDiseaseHorizontalSlider")
        self.liverDisease = self.findChild(
            QSlider, "liverDiseaseHorizontalSlider")
        self.diabetesMilitus = self.findChild(
            QSlider, "diabetesMilitusHorizontalSlider")
        self.hemiplegia = self.findChild(QSlider, "hemiplegiaHorizontalSlider")
        self.renalDisease = self.findChild(
            QSlider, "renalDiseaseHorizontalSlider")
        self.solidTumor = self.findChild(QSlider, "solidTumorHorizontalSlider")
        self.leukemia = self.findChild(QSlider, "leukemiaHorizontalSlider")
        self.lymphoma = self.findChild(QSlider, "lymphomaHorizontalSlider")
        self.VIH = self.findChild(QSlider, "VIHHorizontalSlider")
        self.charlsonSum = self.findChild(
            QLineEdit, "comorbilityCharlsonTotalLineEdit")

        # Diagnostic Assistants
        self.diagnostic_aids_slider = self.findChild(
            QSlider, "diagnostic_aids_slider")
        self.scaleEpwort = self.findChild(QSpinBox, "scaleEpworthSpinBox")
        self.ETco2 = self.findChild(QSpinBox, "ETco2SpinBox")
        self.scaleMallampati = self.findChild(
            QSpinBox, "scaleMallampatiSpinBox")

        # Blood Gases
        self.blood_gases_slider = self.findChild(QSlider, "blood_gases_slider")
        self.PH = self.findChild(QDoubleSpinBox, "PHDoubleSpinBox")
        self.pCO2 = self.findChild(QSpinBox, "pCO2SpinBox")
        self.pO2 = self.findChild(QSpinBox, "pO2SpinBox")
        self.EB = self.findChild(QDoubleSpinBox, "EBDoubleSpinBox")

        # Spirometry
        self.spirometry_slider = self.findChild(QSlider, "spirometry_slider")
        self.FVClitros = self.findChild(
            QDoubleSpinBox, "FVClitrosDoubleSpinBox")
        self.FVC = self.findChild(QSpinBox, "FVCSpinBox")
        self.FEV1litros = self.findChild(
            QDoubleSpinBox, "FEV1litrosDoubleSpinBox")
        self.FEV1L = self.findChild(QSpinBox, "FEV1LSpinBox")
        self.FEV1LFVCLitros = self.findChild(
            QLineEdit, "FEV1LFVCLitrosLineEdit")

    def __save(self):
        self.__catchData()
        # clean data?
        # lock button?

    def __catchData(self):
        # Data for Metrics table
        try:
            self.metricsData = [
                float(self.patientheight.text()),
                float(self.patientweight.text()),
                float(self.neckCircumference.text())
            ]

        except ValueError:
            self.metricsData = [
                self.patientheight.text(),
                self.patientweight.text(),
                self.neckCircumference.text()
            ]

        # Data for vital_signs table
        self.vital_signsData = [
            self.CF.value(),
            self.highArterialTension.value(),
            self.lowArterialTension.value(),
            self.RF.value(),
            self.OS.value(),
            self.temperature.value()
        ]
        # Data for History table
        self.historyData = [
            self.OxigenUse.value(),
            self.smoker.value(),
            self.exsmoker.value(),
            self.snoring.value(),
            self.witnessedApneas.value(),
            self.chronicFatigue.value(),
            self.hypertension.value(),
            self.medicines.toPlainText()
        ]
        # Data for ComorbilidadCharlosn tabele
        self.charlsonComorbidityData = [
            self.CI.value(),
            self.HCVA.value(),
            self.PVD.value(),
            self.dementia.value(),
            self.EPOC.value(),
            self.CTD.value(),
            self.liverDisease.value(),
            self.diabetesMilitus.value(),
            self.hemiplegia.value(),
            self.renalDisease.value(),
            self.solidTumor.value(),
            self.leukemia.value(),
            self.lymphoma.value(),
            self.VIH.value(),
        ]
        # Data for AuxiliaresDiagnostico table

        self.diagnostiAuxData = []
        self.__diagnostic_aids_values()

        if self.validate_metrics():
            if self.validate_fields():
                if self.is_edit:
                    self.__update_database()
                else:
                    self.__insert_into_database()
            else:
                self.__missing_filds_pop_up()
        else:
            self.wrong_metrics_fields()

    def __insert_into_database(self):
        # Create apnea study object
        self.__create_apnea_study()
        # List to store the id's of each insert
        self.id_commits_medical_record = []
        # Insert patient FK from the last insertion at patient table
        self.id_commits_medical_record.append(self.patient.apnea_study.id)

        db_controll = ControllDb()
        # thread_lock = Lock()
        metrics_thread = DatabaseThread(
            target=db_controll.insertIntoMetrics,
            args=(tuple(self.metricsData),)
        )
        metrics_thread.start()
        insert_db_thread_event(metrics_thread.native_id)
        self.id_commits_medical_record.append(metrics_thread.join())

        vital_signs_thread = DatabaseThread(
            target=db_controll.insertIntoVitalSigns,
            args=(tuple(self.vital_signsData),)
        )
        vital_signs_thread.start()
        insert_db_thread_event(vital_signs_thread.native_id)
        self.id_commits_medical_record.append(vital_signs_thread.join())

        record_thread = DatabaseThread(
            target=db_controll.insertIntoHistory,
            args=(tuple(self.historyData),)
        )
        record_thread.start()
        insert_db_thread_event(record_thread.native_id)
        self.id_commits_medical_record.append(record_thread.join())

        charlson_comorbidity_thread = DatabaseThread(
            target=db_controll.insertIntoCharlsonComorbidity,
            args=(tuple(self.charlsonComorbidityData),)
        )
        charlson_comorbidity_thread.start()
        insert_db_thread_event(charlson_comorbidity_thread.native_id)
        self.id_commits_medical_record.append(charlson_comorbidity_thread.join())

        diagnostic_aids_thread = DatabaseThread(
            target=db_controll.insertIntoDiagnostiAux,
            args=(tuple(self.diagnostiAuxData),)
        )
        diagnostic_aids_thread.start()
        insert_db_thread_event(diagnostic_aids_thread.native_id)
        self.id_commits_medical_record.append(diagnostic_aids_thread.join())

        medical_record_thread = DatabaseThread(
            target=db_controll.insertIntoMedicalRecord,
            args=(tuple(self.id_commits_medical_record),)
        )
        medical_record_thread.start()
        insert_db_thread_event(medical_record_thread.native_id)

        # Create tuple with the primary keys
        self.id_commits_medical_record.insert(
            0,
            medical_record_thread.join())

        self.create_medical_record_object()

    def __create_apnea_study(self):
        today = datetime.date.today()
        self.patient.apnea_study.creation_date = str(
            today.year) + '/' + str(today.month) + '/' + str(today.day)
        self.patient.apnea_study.status = 1

        apnea_study = (
            self.patient.nss,
            self.patient.apnea_study.status,
            self.patient.apnea_study.creation_date
        )

        db_controll = ControllDb()
        db_thread = DatabaseThread(
            target=db_controll.insertApneaStudy,
            args=(apnea_study,)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        self.patient.apnea_study.id = db_thread.join()

    def create_medical_record_object(self):
        self.patient.medical_record.set_medical_record(self.id_commits_medical_record)
        # print("Medical Record Created...")

    def fillData(self):
        # metrics
        self.patientweight.setText(str(self.patient.medical_record.metrics.weight))
        self.patientheight.setText(str(self.patient.medical_record.metrics.height))
        self.neckCircumference.setText(
            str(self.patient.medical_record.metrics.neck_circumference))
        self.bmi_calculation()

        # vital_signs
        self.CF.setValue(self.patient.medical_record.vital_sign.cardiac_frequency)
        self.highArterialTension.setValue(
            self.patient.medical_record.vital_sign.arterial_tension_high)
        self.lowArterialTension.setValue(
            self.patient.medical_record.vital_sign.arterial_tension_low)
        self.RF.setValue(self.patient.medical_record.vital_sign.respiratory_frequency)
        self.OS.setValue(self.patient.medical_record.vital_sign.oxigen_saturation)
        self.temperature.setValue(self.patient.medical_record.vital_sign.temperature)

        # history
        self.OxigenUse.setValue(self.patient.medical_record.history.oxigen_use)
        self.smoker.setValue(self.patient.medical_record.history.smoker)
        self.exsmoker.setValue(self.patient.medical_record.history.ex_smoker)
        self.snoring.setValue(self.patient.medical_record.history.snoring)
        self.witnessedApneas.setValue(
            self.patient.medical_record.history.witnessed_apneas)
        self.chronicFatigue.setValue(
            self.patient.medical_record.history.chronic_fatigue)
        self.hypertension.setValue(self.patient.medical_record.history.hypertension)
        self.medicines.setText(self.patient.medical_record.history.medicines)

        # Charlson
        self.CI.setValue(self.patient.medical_record.comorbility.cardiac_insuficiency)
        self.HCVA.setValue(
            self.patient.medical_record.comorbility.antecedente_cerebro_vascular)
        self.PVD.setValue(
            self.patient.medical_record.comorbility.enfermedad_vascular_periferica)
        self.dementia.setValue(self.patient.medical_record.comorbility.demencia)
        self.EPOC.setValue(self.patient.medical_record.comorbility.epoc)
        self.CTD.setValue(
            self.patient.medical_record.comorbility.enfermedad_tejido_conectivo)
        self.liverDisease.setValue(
            self.patient.medical_record.comorbility.liver_disease)
        self.diabetesMilitus.setValue(
            self.patient.medical_record.comorbility.diabetes_mellitus)
        self.hemiplegia.setValue(self.patient.medical_record.comorbility.hemiplejia)
        self.renalDisease.setValue(
            self.patient.medical_record.comorbility.afeccion_renal)
        self.solidTumor.setValue(self.patient.medical_record.comorbility.tumor_solido)
        self.leukemia.setValue(self.patient.medical_record.comorbility.leucemia)
        self.lymphoma.setValue(self.patient.medical_record.comorbility.linfoma)
        self.VIH.setValue(self.patient.medical_record.comorbility.vih)
        self.comorbilityCharlsonSum()

        # Aux Diagnostic
        self.scaleEpwort.setValue(
            self.patient.medical_record.aux_diagnostics.escala_epworth)
        self.ETco2.setValue(self.patient.medical_record.aux_diagnostics.etco2)
        self.scaleMallampati.setValue(
            self.patient.medical_record.aux_diagnostics.escala_mallampati)
        self.set_diagnostic_aids_slider(self.patient.medical_record.aux_diagnostics.escala_epworth,
                                        self.patient.medical_record.aux_diagnostics.etco2,
                                        self.patient.medical_record.aux_diagnostics.escala_mallampati)

        self.PH.setValue(self.patient.medical_record.aux_diagnostics.pH)
        self.pCO2.setValue(self.patient.medical_record.aux_diagnostics.pco2)
        self.pO2.setValue(self.patient.medical_record.aux_diagnostics.po2)
        self.EB.setValue(self.patient.medical_record.aux_diagnostics.eb)
        self.set_blood_gases_slider(self.patient.medical_record.aux_diagnostics.pH,
                                    self.patient.medical_record.aux_diagnostics.pco2,
                                    self.patient.medical_record.aux_diagnostics.po2,
                                    self.patient.medical_record.aux_diagnostics.eb)

        self.FVClitros.setValue(self.patient.medical_record.aux_diagnostics.fvc_litros)
        self.FVC.setValue(self.patient.medical_record.aux_diagnostics.fvc)
        self.FEV1litros.setValue(
            self.patient.medical_record.aux_diagnostics.fev1_litros)
        self.FEV1L.setValue(self.patient.medical_record.aux_diagnostics.fev1)
        self.set_spirometry_slider(self.patient.medical_record.aux_diagnostics.fvc_litros,
                                   self.patient.medical_record.aux_diagnostics.fvc,
                                   self.patient.medical_record.aux_diagnostics.fev1_litros,
                                   self.patient.medical_record.aux_diagnostics.fev1)
        self.fev1lfvclitros()

    def __update_database(self):
        self.metricsData.append(self.patient.medical_record.metrics.id)
        db_controll = ControllDb()
        metric_thread = DatabaseThread(
            target=db_controll.updateMetrics,
            args=(tuple(self.metricsData),)
        )
        metric_thread.start()
        insert_db_thread_event(metric_thread.native_id)
        metric_thread.join()
        # self.database.updateMetrics(tuple(self.metricsData))

        self.vital_signsData.append(self.patient.medical_record.vital_sign.id)
        vital_signs_thread = DatabaseThread(
            target=db_controll.updateVitalSigns,
            args=(tuple(self.vital_signsData),)
        )
        vital_signs_thread.start()
        insert_db_thread_event(vital_signs_thread.native_id)
        vital_signs_thread.join()
        
        #self.database.updatevital_signs(tuple(self.vital_signsData))

        self.historyData.append(self.patient.medical_record.history.id)
        history_thread = DatabaseThread(
            target=db_controll.updateHistory,
            args=(tuple(self.historyData),)
        )
        history_thread.start()
        insert_db_thread_event(history_thread.native_id)
        history_thread.join()
        # self.database.updateHistory(tuple(self.historyData))

        self.charlsonComorbidityData.append(
            self.patient.medical_record.comorbility.id)
        comorbidity_thread = DatabaseThread(
            target=db_controll.updateCharlsonComorbidity,
            args=(tuple(self.charlsonComorbidityData),)
        )
        comorbidity_thread.start()
        insert_db_thread_event(comorbidity_thread.native_id)
        comorbidity_thread.join()
        # self.database.updateCharlsonComorbidity(
            # tuple(self.charlsonComorbidityData))

        self.change_null_values()
        self.diagnostiAuxData.append(self.patient.medical_record.aux_diagnostics.id)
        diagnostic_aids_thread = DatabaseThread(
            target=db_controll.updateDiagnostiAux,
            args=(tuple(self.diagnostiAuxData),)
        )
        diagnostic_aids_thread.start()
        insert_db_thread_event(diagnostic_aids_thread.native_id)
        diagnostic_aids_thread.join()
        # self.database.updateDiagnostiAux(tuple(self.diagnostiAuxData))

    def __operations(self):
        # Calculate the BMI
        self.patientweight.textChanged[str].connect(self.bmi_calculation)
        self.patientheight.textChanged[str].connect(self.bmi_calculation)

        # Calculate the comorbility of Charlson
        self.CI.valueChanged[int].connect(self.comorbilityCharlsonSum)
        self.HCVA.valueChanged[int].connect(self.comorbilityCharlsonSum)
        self.dementia.valueChanged[int].connect(self.comorbilityCharlsonSum)
        self.PVD.valueChanged[int].connect(self.comorbilityCharlsonSum)
        self.EPOC.valueChanged[int].connect(self.comorbilityCharlsonSum)
        self.CTD.valueChanged[int].connect(self.comorbilityCharlsonSum)
        self.liverDisease.valueChanged[int].connect(
            self.comorbilityCharlsonSum)
        self.diabetesMilitus.valueChanged[int].connect(
            self.comorbilityCharlsonSum)
        self.hemiplegia.valueChanged[int].connect(self.comorbilityCharlsonSum)
        self.renalDisease.valueChanged[int].connect(
            self.comorbilityCharlsonSum)
        self.solidTumor.valueChanged[int].connect(self.comorbilityCharlsonSum)
        self.leukemia.valueChanged[int].connect(self.comorbilityCharlsonSum)
        self.lymphoma.valueChanged[int].connect(self.comorbilityCharlsonSum)
        self.VIH.valueChanged[int].connect(self.comorbilityCharlsonSum)

        # Calculate the FEV1L / FVCL division
        self.FEV1litros.valueChanged[float].connect(self.fev1lfvclitros)
        self.FVClitros.valueChanged[float].connect(self.fev1lfvclitros)

        self.diagnostic_aids_slider.valueChanged[int].connect(
            self.set_diagnostic_aids)
        self.blood_gases_slider.valueChanged[int].connect(self.set_blood_gases)
        self.spirometry_slider.valueChanged[int].connect(self.set_spirometry)

        # Parameter for charlson calculation
        # self.birthYear.valueChanged[int].connect(self.comorbilityCharlsonSum)
        # self.birthMonth.valueChanged[int].connect(self.comorbilityCharlsonSum)
        # self.birthDay.valueChanged[int].connect(self.comorbilityCharlsonSum)

    def bmi_calculation(self):
        try:
            weight = float(self.patientweight.text())
            height = float(self.patientheight.text())
        except ValueError:
            weight = 0
            height = 1

        try:
            bmi = weight / (height**2)
        except (ZeroDivisionError):
            bmi = -1
        # Write the result in the bmiQLineEdit
        self.patientBmi.setText(str("{:.4f}".format(bmi)))

    def comorbilityCharlsonSum(self):
        if self.is_edit:
            age = self.calculateAge(self.patient.birth_date)
        else:
            age = self.calculateAge(self.patient.birth_date)
        charlsonSum = 0
        # Comorbility age parameters
        if age < 50:
            charlsonSum += 0
        elif 49 < age < 60:
            charlsonSum += 1
        elif 59 < age < 70:
            charlsonSum += 1
        elif 69 < age < 80:
            charlsonSum += 2
        elif age > 79:
            charlsonSum += 3

        charlsonSum += self.CI.value() + self.HCVA.value() + self.dementia.value()
        charlsonSum += self.PVD.value() + self.EPOC.value() + self.CTD.value()
        charlsonSum += self.diabetesMilitus.value() + self.liverDisease.value()

        if self.hemiplegia.value() == 1:
            charlsonSum += 2

        if self.renalDisease.value() == 1:
            charlsonSum += 2

        if self.leukemia.value() == 1:
            charlsonSum += 2

        if self.lymphoma.value() == 1:
            charlsonSum += 2

        if self.solidTumor.value() == 1:
            charlsonSum += 2
        elif self.solidTumor.value() == 2:
            charlsonSum += 3

        if self.VIH.value() == 1:
            charlsonSum += 6

        # Write the result in the charlsonSumQLineEdit
        self.charlsonSum.setText(str(charlsonSum))

    def fev1lfvclitros(self):
        try:
            FEV1litros = float(self.FEV1litros.text())
            FVClitros = float(self.FVClitros.text())
        except ValueError:
            FEV1litros = 0
            FVClitros = 1

        try:
            division = FEV1litros / FVClitros
        except (ZeroDivisionError):
            division = -1

        self.FEV1LFVCLitros.setText(str("{:.2f}".format(division)))

    def __diagnostic_aids_values(self):

        if self.diagnostic_aids_slider.value() == YES:
            self.diagnostiAuxData.append(self.scaleEpwort.value())
            self.diagnostiAuxData.append(self.ETco2.value())
            self.diagnostiAuxData.append(self.scaleMallampati.value())
        else:
            self.diagnostiAuxData.append(NULL)
            self.diagnostiAuxData.append(NULL)
            self.diagnostiAuxData.append(NULL)

        if self.blood_gases_slider.value() == YES:
            self.diagnostiAuxData.append(self.PH.value())
            self.diagnostiAuxData.append(self.pCO2.value())
            self.diagnostiAuxData.append(self.pO2.value())
            self.diagnostiAuxData.append(self.EB.value())
        else:
            self.diagnostiAuxData.append(NULL)
            self.diagnostiAuxData.append(NULL)
            self.diagnostiAuxData.append(NULL)
            self.diagnostiAuxData.append(NULL)

        if self.spirometry_slider.value() == YES:
            self.diagnostiAuxData.append(self.FVClitros.value())
            self.diagnostiAuxData.append(self.FVC.value())
            self.diagnostiAuxData.append(self.FEV1litros.value())
            self.diagnostiAuxData.append(self.FEV1L.value())
        else:
            self.diagnostiAuxData.append(NULL)
            self.diagnostiAuxData.append(NULL)
            self.diagnostiAuxData.append(NULL)
            self.diagnostiAuxData.append(NULL)

    def set_diagnostic_aids(self):
        if self.diagnostic_aids_slider.value() == YES:
            self.scaleEpwort.setEnabled(TRUE)
            self.ETco2.setEnabled(TRUE)
            self.scaleMallampati.setEnabled(TRUE)
        else:
            self.scaleEpwort.setEnabled(FALSE)
            self.ETco2.setEnabled(FALSE)
            self.scaleMallampati.setEnabled(FALSE)

    def set_blood_gases(self):
        if self.blood_gases_slider.value() == YES:
            self.PH.setEnabled(TRUE)
            self.pCO2.setEnabled(TRUE)
            self.pO2.setEnabled(TRUE)
            self.EB.setEnabled(TRUE)
        else:
            self.PH.setEnabled(FALSE)
            self.pCO2.setEnabled(FALSE)
            self.pO2.setEnabled(FALSE)
            self.EB.setEnabled(FALSE)

    def set_spirometry(self):
        if self.spirometry_slider.value() == YES:
            self.FVClitros.setEnabled(TRUE)
            self.FVC.setEnabled(TRUE)
            self.FEV1litros.setEnabled(TRUE)
            self.FEV1L.setEnabled(TRUE)
        else:
            self.FVClitros.setEnabled(FALSE)
            self.FVC.setEnabled(FALSE)
            self.FEV1litros.setEnabled(FALSE)
            self.FEV1L.setEnabled(FALSE)

    def set_diagnostic_aids_slider(self, scaleEpwort, ETco2, scaleMallampati):
        if scaleEpwort == ZERO and ETco2 == ZERO and scaleMallampati == ZERO:
            self.diagnostic_aids_slider.setValue(0)
        else:
            self.diagnostic_aids_slider.setValue(1)

    def set_blood_gases_slider(self, PH, pCO2, pO2, EB):
        if PH == ZERO and pCO2 == ZERO and pO2 == ZERO and EB == ZERO:
            self.blood_gases_slider.setValue(0)
        else:
            self.blood_gases_slider.setValue(1)

    def set_spirometry_slider(self, FVClitros, FVC, FEV1litros, FEV1L):
        if FVClitros == ZERO and FVC == ZERO and FEV1litros == ZERO and FEV1L == ZERO:
            self.spirometry_slider.setValue(0)
        else:
            self.spirometry_slider.setValue(1)

    def change_null_values(self):
        for pos in range(len((self.diagnostiAuxData))):
            if self.diagnostiAuxData[pos] == NULL:
                self.diagnostiAuxData[pos] = NONE
            else:
                pass

    def calculateAge(self, born):
        today = datetime.date.today()
        try:
            birthday = born.replace(year=today.year)

        # raised when birth date is February 29
        # and the current year is not a leap year
        except ValueError:
            birthday = born.replace(year=today.year,
                                    month=born.month + 1, day=1)

        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def clear(self):
        # Data for Metrics table

        self.patientheight.clear()
        self.patientweight.clear()
        self.neckCircumference.clear()

        # Data for vital_signs table

        self.CF.cleanText()
        self.highArterialTension.cleanText()
        self.lowArterialTension.cleanText()
        self.RF.cleanText()
        self.OS.cleanText()
        self.temperature.cleanText()

        # Data for History table

        self.OxigenUse.setValue(0)
        self.smoker.setValue(0)
        self.exsmoker.setValue(0)
        self.snoring.setValue(0)
        self.witnessedApneas.setValue(0)
        self.chronicFatigue.setValue(0)
        self.hypertension.setValue(0)
        self.medicines.setText("")

        # Data for ComorbilidadCharlosn tabele

        self.CI.setValue(0)
        self.HCVA.setValue(0)
        self.PVD.setValue(0)
        self.dementia.setValue(0)
        self.EPOC.setValue(0)
        self.CTD.setValue(0)
        self.diabetesMilitus.setValue(0)
        self.hemiplegia.setValue(0)
        self.renalDisease.setValue(0)
        self.solidTumor.setValue(0)
        self.leukemia.setValue(0)
        self.lymphoma.setValue(0)
        self.VIH.setValue(0)

        # Data for AuxiliaresDiagnostico table

        self.scaleEpwort.cleanText()
        self.ETco2.cleanText()
        self.scaleMallampati.cleanText()
        self.PH.cleanText()
        self.pCO2.cleanText()
        self.pO2.cleanText()
        self.EB.cleanText()
        self.FVClitros.cleanText()
        self.FVC.cleanText()
        self.FEV1litros.cleanText()
        self.FEV1L.cleanText()

    def validate_fields(self):
        self.emptyFields = ""

        # print("--- FIELDS VALIDATION ---")
        if self.patientheight.text() == '':
            self.emptyFields += "\n* --> Estatura"
        if self.patientweight.text() == '':
            self.emptyFields += "\n* --> Peso"
        if self.neckCircumference.text() == '':
            self.emptyFields += "\n* --> Circunferencia del Cuello"

        # print(self.emptyFields, len(self.emptyFields))

        if len(self.emptyFields) == 0:
            # print("Data OK")
            return True
        else:
            # print("Data WRONG")
            return False

    def validate_metrics(self):
        # print("--- METRICS VALIDATION ---")
        self.wrong_metrics = ""
        if not self.validate_heigth():
            self.wrong_metrics += "\n* --> Estatura"

        if not self.validate_weigth():
            self.wrong_metrics += "\n* --> Peso"

        if not self.validate_neck_circumference():
            self.wrong_metrics += "\n* --> Circunferencia de Cuello"

        # print(self.wrong_metrics, len(self.wrong_metrics))

        if len(self.wrong_metrics) == 0:
            return True
        else:
            return False

    def validate_heigth(self):
        float_rgx = r"\d{0,1}(\.|[^\.])\d{0,2}"

        if not re.match(float_rgx, self.patientheight.text()):
            return False

        try:
            float_value = float(self.patientheight.text())
        except ValueError:
            return False

        return True

    def validate_weigth(self):
        float_rgx = r"\d{1,3}(\.|[^\.])\d{0,2}"

        if not re.match(float_rgx, self.patientweight.text()):
            return False

        try:
            float_value = float(self.patientweight.text())
        except ValueError:
            return False

        return True

    def validate_neck_circumference(self):
        float_rgx = r"\d{1,2}(\.|[^\.])\d{0,2}"

        if not re.match(float_rgx, self.neckCircumference.text()):
            return False

        try:
            float_value = float(self.neckCircumference.text())
        except ValueError:
            return False

        return True

    def __missing_filds_pop_up(self):
        msg = QMessageBox()
        msg.setWindowTitle("Campos Erroneos")

        msg.setText("Error en los siguientes campos:\n" + self.emptyFields)

        msg.exec_()

    def wrong_metrics_fields(self):
        msg = QMessageBox()
        msg.setWindowTitle("Datos Erroneos")

        msg.setText("Datos Erroneos detectados:\n" + self.wrong_metrics)
        self.wrong_metrics = ""

        msg.exec_()
