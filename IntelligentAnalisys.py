from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QLabel, QCheckBox, QPushButton, QTableView, QSlider
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import QSortFilterProxyModel

import pathlib
import pandas as pd
import numpy as np
import json
import cv2
import shutil
from multiprocessing import Process
from mlxtend.frequent_patterns import apriori, association_rules
import re

from database import ControllDb, MultimediaDb, DatabaseThread, insert_db_thread_event
from faceMesh import Facemesh
from measures import *
from io import TextIOWrapper
from datetime import datetime
from log import Log
from WaitingSpinnerWidget import define_waiting_spinner, insert_process_event
from iaFilterWidget import iaFiltersWidget
from rangesDiscretization import RangeDiscretizationWidget

UI_PATH = "ui/IntelligentAnalisys.ui"

ID_PATIENT_IDX = 0
ID_APNEA_STUDY_IDX = 0
BLANK = ""
YES = "1"
NO = "0"
DEGREE_1 = "1"
DEGREE_2 = "2"
DEGREE_3 = "3"
DEGREE_4 = "4"
DEGREE_5 = "5"
MALE = "Hombre"
FEMALE = "Mujer"
OTHER = 2
MALE_EXCEL = "masculino"
FEMALE_EXCEL = "femenino"
OTHER_EXCEL = "otro"
ENCODE = "utf-8"
PD_COLUMNS = ['Landmark', 'X', 'Y']

MALE_FILTER = 1
FEMALE_FILTER = 2
MIN_VALUE = 0
MAX_VALUE = 1

ID_INDEX = 0
FECHA_ESTUDIO_INDEX = 1
SEXO_INDEX = 4
EDAD_INDEX = 3

ID_METRICS = 2
ID_VITAL_SIGNS = 3
ID_RECORD = 4
ID_COMORBIDITY = 5
ID_DIAGNOSTIC_AIDS = 6

FRECUENCIA_CARDIACA_INDEX = 1
PRESION_ARTERIAL_SISTOLICA_INDEX = 2
PRESION_ARTERIAL_DIASTOLICA_INDEX = 3
FRECUENCIA_RESPIRATORIA_INDEX = 4
SATURACION_DE_OXIGENO_INDEX = 5
TEMPERATURA_INDEX = 6

TALLA_INDEX = 1
CIRCUNFERENCIA_DE_CUELLO_INDEX = 3
PESO_INDEX = 2

USO_DE_OXIGENO_INDEX = 1
TABAQUISMO_INDEX = 2
EXFUMADOR_INDEX = 3
INGESTA_DE_MEDICAMENTOS_INDEX = 8
PRESENCIA_DE_RONQUIDO_INDEX = 5

INFARTO_AGUDO_AL_MIOCARDIO_INDEX = 1
ANTECEDENTE_DE_ACCIDENTE_CEREBROVASCULAR_INDEX = 2
ENFERMEDAD_VASCULAR_PERIFERICA_INDEX = 3
DEMENCIA_INDEX = 4
EPOC_INDEX = 5

ESCALA_DE_EPWORTH_INDEX = 1
ET_CO2_INDEX = 2
ESCALA_DE_MALLAMPATI_INDEX = 3
PH_INDEX = 4
PCO2_INDEX = 5
PO2_INDEX = 6
EB_INDEX = 7
FVC_LITRO_INDEX = 8
FVC_INDEX = 9
FEV1_LITROS_INDEX = 10
FEV1L_INDEX = 11
FEV1L_FVCL_INDEX = -1

INDICE_DE_APNEA_HIPOAPNEA_INDEX = 0
INDICE_DE_APNEAS_INDEX = 1
IAI_INDEX = 2
IAO_INDEX = 3
IAC_INDEX = 4
IAM_INDEX = 5
INDICE_DE_HIPOPNEAS_INDEX = 6
IDO_INDEX = 7
SATURACION_PROMEDIO_INDEX = 8
DESATURACION_MENOR_INDEX = 9
SATURACION_BASAL_INDEX = 10
FRECUENCIA_DE_PULSO_PROMEDIO_INDEX = 11
PROMEDIO_DE_RESPIRACIONES_POR_MINUTO_INDEX = 12
PROPORCION_DE_PERIODO_CSR_EN_EL_PERIODO_DE_ANALISIS_INDEX = 12
APNEAS_INDEX = 13
APNEAS_INDETERMINADAS_INDEX = 14
APNEAS_OBSTRUCTIVAS_INDEX = 15
APNEAS_CENTRALES_INDEX = 16
APNEAS_MIXTAS_INDEX = 17
HIPOAPNEAS_INDEX = 18
EVENTOS_DE_RONQUIDOS_INDEX = 19
SATURACION_90_INDEX = 20
SATURACION_85_INDEX = 21
SATURACION_80_INDEX = 22
PERIODO_DE_EVALUACION_DE_FLUJO_INDEX = 22

IMAGE_PATH = 2
IMAGE_COORDINATES = 3
IMAGE_TAG = 4
FRONT = 0
LATERAL = 1
ANCHO_DE_CARA_INDEX = -1
ANGULO_ANCHO_DE_CARA_INDEX = -1
ANCHO_INTERCANTAL_INDEX = -1
ANCHO_BIOCULAR_INDEX = -1
ANCHO_MANDIBULAR_INDEX = -1
AREA_TRIANULO_MAXILAR_INDEX = -1
ANGULO_ANCHO_DE_CARA_INDEX = -1
ANCHO_DE_NARIZ_INDEX = -1
ANGULO_NASION_MANDIBULAR_INDEX = -1
ANGULO_SUB_NASION_MANDIBULAR_INDEX = -1
ANGULO_ANB_INDEX = -1
DISTANCIA_SUBMENTAL_INDEX = -1
VOLUMEN_MEDIO_FOSA_CRANEAL_INDEX = -1

VIDEO_PATH_INDEX = 2
AUDIO_PATH_INDEX = 2
OSA_PATH_INDEX = 2

CLINIC_COLUMNS = [
    "ID",
    "Fecha Estudio",
    "Sexo",
    "Edad",
    "Frecuencia cardiaca (lpm)",
    "Presión arterial sistólica (mmhg)",
    "Presión arterial diastólica (mmhg)",
    "Frecuencia respiratoria (rpm)",
    "Saturación de oxigeno (%)",
    "Temperatura (º)",
    "circunferencia de cuello (cm)",
    "IMC",
    "Uso de oxigeno",
    "Tabaquismo",
    "Exfumador",
    "Presencia de ronquido",
    "Escala de Epworth",
    "ET CO2",
    "Escala de Mallampati",
    "PH",
    "pCO2",
    "pO2",
    "EB",
    "FVC Litro",
    "FVC%",
    "FEV1 Litros",
    "FEV1L%",
    "FEV1L/FVCL",
    "Ingesta de medicamentos",
    "Infarto agudo al miocardio",
    "Antecedente de accidente cerebrovascular",
    "Enfermedad vascular periferica",
    "Demencia",
    "EPOC"
]
CRANEOFACIAL_COLUMNS = [
    "Ancho de cara (cm)",
    "Ángulo Ancho de Cara (°)",
    "Ancho intercantal (cm)",
    "Ancho Biocular (cm)",
    "Ancho mandibular (cm)",
    "Área triágulo maxilar (cm2)",
    "Ángulo Ancho de mandibula (°)",
    "Ancho de Nariz (cm)",
    "Àngulo Nasion Mandibular (°)",
    "Ángulo Sub-Nasion Mandibular (°)",
    "Ángulo ANB (°)",
    "Distancia Submental (cm)",
    "Volumen Medio Fosa Craneal (cm3)"
]
POLYSOMNOGRAPHY_COLUMNS = [
    "Indice de Apnea-Hipoapnea",
    "Indice de Apneas",
    "ÍAI (índice de apneas sin clasificar)",
    "ÍAO (índice de apneas obstructivas)",
    "ÍAC (índice de apneas centrales)",
    "ÍAM (índice de apneas mixtas)",
    "Indice de hipopneas",
    "IDO (Índice de Desaturación de Oxigeno",
    "Saturación promedio",
    "Desaturación menor",
    "Saturación basal",
    "Frecuencia de pulso promedio",
    "Promedio de respiraciones por minuto",
    "Proporcion de periodo CSR en el periodo de análisis",
    "Apneas",
    "Apneas indeterminadas",
    "Apneas obstructivas",
    "Apneas centrales",
    "Apneas mixtas",
    "Hipoapneas",
    "Eventos de ronquidos",
    "Saturación <90%",
    "Saturación <85%",
    "Saturación <80%",
    "Periodo de evaluación de flujo"
]

DELIM = '\t'


def start_waitting_spinner() -> None:
    define_waiting_spinner()


class IntelligentAnalisys(QWidget):
    def __init__(self):
        super(IntelligentAnalisys, self).__init__()

        self.__load_ui_file(pathlib.Path(__file__).parent)
        self.__define_widgets()
        self.__define_buttons()
        self.__operations()

    def __load_ui_file(self, path) -> None:
        uic.loadUi(path / UI_PATH, self)

    def __define_widgets(self) -> None:
        self._clinic_data_checkbox = self.findChild(
            QCheckBox, "clinic_data_checkbox")
        self._craniofacial_checkbox = self.findChild(
            QCheckBox, "craniofacial_checkbox")
        self._polysomnography_checkbox = self.findChild(QCheckBox,
                                                        "polysomnography_checkbox")
        self._minimum_support_slider = self.findChild(QSlider, "minimum_support_slider")
        self._minimum_threshold_slider = self.findChild(QSlider,
                                                        "minimum_threshold_slider")
        self._maximum_rules_slider = self.findChild(QSlider, "maximum_rules_slider")
        self._minimum_support_label = self.findChild(QLabel, "minimum_support_label")
        self._minimum_threshold_label = self.findChild(QLabel,"minimum_threshold_label")
        self._maximum_rules_label = self.findChild(QLabel,"maximum_rules_label")
        self._start_analisys_button = self.findChild(
            QPushButton, "start_analisys_button")
        self._results_table = self.findChild(QTableView, "results_tableview")
        self._model = QStandardItemModel()
        self._filter_proxy_model = QSortFilterProxyModel()
        self._filters_button = self.findChild(QPushButton, "filterPushButton")
        self._export_rules_button = self.findChild(QPushButton, "exportRulesPushButton")

        self.discretized_intervals = 3

        self._polysomnography_checkbox.hide()

    def __define_buttons(self) -> None:
        self._start_analisys_button.clicked.connect(self.__define_ranges)
        self._filters_button.clicked.connect(self.__define_filter)
        self._export_rules_button.clicked.connect(self.__export_rules)
    
    def __define_filter(self) -> None:
        self._fw = iaFiltersWidget()
        self._fw.show()
        self._fw._apply_filters_button.clicked.connect(self.__apply_filters)
        self._fw._weight_range_exclusive.returnPressed.connect(self.__apply_filters)
        self._fw._iah_range_inclusive.returnPressed.connect(self.__apply_filters)

    def __apply_filters(self) -> None:
        self._filters = self._fw.select_data_with_filter()
        print(self._filters)
        self.__filters_applied_msg()

    def __operations(self) -> None:
        self._minimum_support_slider.valueChanged[int].connect(self.__change_sliders_values)
        self._minimum_threshold_slider.valueChanged[int].connect(self.__change_sliders_values)
        self._maximum_rules_slider.valueChanged[int].connect(self.__change_sliders_values)
    
    def __change_sliders_values(self) -> None:
        self._minimum_support_label.setText(str(self._minimum_support_slider.value()))
        self._minimum_threshold_label.setText(str(self._minimum_threshold_slider.value()))
        self._maximum_rules_label.setText(str(self._maximum_rules_slider.value()))

    def __define_ranges(self) -> None:
        if self.__check_option_selected():
            selected_data = self.__define_data_selected_ranges()
            self._discretization_ranges = RangeDiscretizationWidget(selected_data)
            self._discretization_ranges.show()
            self._discretization_ranges._apply_ranges_button.clicked.connect(self.__start_analisys)
            
        else:
            self.__no_option_selected_message()
    
    def __start_analisys(self) -> None:
        waitting_spinner_process = Process(target=start_waitting_spinner)
        waitting_spinner_process.start()
        insert_process_event(waitting_spinner_process.pid)
        try:
            # Select algorithms
            # Select data
            # Proprocesing
            # Discretization
            # apriori
            # asociation rules
            dataframe = self.__select_data()
            print(dataframe.columns)
            transaction_dataframe, data_intervals = self.__preproces_data(dataframe)
            apriori_model = self.__apriori(transaction_dataframe)
            self._model.clear()
            print(transaction_dataframe)
            # caracteriztics_with_intervals = self.__get_rules_caracteriztics_with_intervals(
            #     data_intervals)
            print(data_intervals)
            self.__add_rules_to_table(apriori_model,
                                        len(transaction_dataframe),
                                        data_intervals)
            waitting_spinner_process.kill()

        except Exception as e:
            print("Error: ", e)
            log = Log()
            log.insert_log_error()
            waitting_spinner_process.kill()
            self.__analisys_error_msg()

    def __select_data(self) -> pd.DataFrame:
        dataframes_created = list()

        if self._clinic_data_checkbox.isChecked():
            clinic_data_dataframe = pd.DataFrame(
                self.__generate_clinic_data_list(),
                columns=CLINIC_COLUMNS
                )
            dataframes_created.append(clinic_data_dataframe)

        if self._craniofacial_checkbox.isChecked():
            craneofacial_dataframe = pd.DataFrame(
                self.__generate_craneofacial_list(),
                columns=CRANEOFACIAL_COLUMNS    
                )
            dataframes_created.append(craneofacial_dataframe)
        
        if self._polysomnography_checkbox.isChecked():
            polysomnography_dataframe = pd.DataFrame(
                self.__generate_polysomnography_list(),
                columns=POLYSOMNOGRAPHY_COLUMNS)
            dataframes_created.append(polysomnography_dataframe)
        
        if len(dataframes_created) == 1:
            dataframe = dataframes_created[0]
        
        elif len(dataframes_created) == 2:
            dataframe = pd.concat(
                [dataframes_created[0], dataframes_created[1]],
                axis=1
                )
        
        elif len(dataframes_created) == 3:
            dataframe = pd.concat(
                [dataframes_created[0], dataframes_created[1]],
                axis=1
                )
            dataframe = pd.concat(
                [dataframe, dataframes_created[2]],
                axis=1
                )
        else:
            dataframe = None
        
        return dataframe

    def __generate_clinic_data_list(self) -> list:
        db_controll = ControllDb()
        patients = self.__select_data_with_filter()
        all_clinc_data = list()

        for patient in patients:
            db_thread = DatabaseThread(
                target=db_controll.select_patient_id_date_apena_studies,
                args=(patient[ID_PATIENT_IDX],)
            )
            db_thread.start()
            insert_db_thread_event(db_thread.native_id)
            apnea_studies = db_thread.join()
            for apnea_study in apnea_studies:
                data = []

                data.append(patient[ID_INDEX])
                data.append(self.patient_sex(patient[SEXO_INDEX]))
                data.append(self.calculate_age(patient[EDAD_INDEX],
                                               apnea_study[FECHA_ESTUDIO_INDEX]))

                data.insert(1, apnea_study[1].strftime("%d-%m-%Y"))

                db_thread = DatabaseThread(
                    target=db_controll.selectAllFromMedicalRecord,
                    args=(apnea_study[ID_APNEA_STUDY_IDX],)
                )
                db_thread.start()
                insert_db_thread_event(db_thread.native_id)
                medical_record = db_thread.join()
                
                db_thread = DatabaseThread(
                    target=db_controll.selectAllFromMetrics,
                    args=(medical_record[ID_METRICS],)
                )
                db_thread.start()
                insert_db_thread_event(db_thread.native_id)
                metrics  = db_thread.join()
            
                db_thread = DatabaseThread(
                    target=db_controll.selectAllFromVitalSigns,
                    args=(medical_record[ID_VITAL_SIGNS],)
                )
                db_thread.start()
                insert_db_thread_event(db_thread.native_id)
                vital_signs = db_thread.join()
                
                db_thread = DatabaseThread(
                    target=db_controll.selectAllFromHistory,
                    args=(medical_record[ID_RECORD],)
                )
                db_thread.start()
                insert_db_thread_event(db_thread.native_id)
                record = db_thread.join()

                db_thread = DatabaseThread(
                    target=db_controll.selectAllFromCharlsonComorbidity,
                    args=(medical_record[ID_COMORBIDITY],)
                )
                db_thread.start()
                insert_db_thread_event(db_thread.native_id)
                charlson_comorbidity = db_thread.join()
                
                db_thread = DatabaseThread(
                    target=db_controll.selectAllFromAuxDiagnostic,
                    args=(medical_record[ID_DIAGNOSTIC_AIDS],)
                )
                db_thread.start()
                insert_db_thread_event(db_thread.native_id)
                diagnostic_aids = db_thread.join()

                data.append(str(vital_signs[FRECUENCIA_CARDIACA_INDEX]))
                data.append(str(vital_signs[PRESION_ARTERIAL_SISTOLICA_INDEX]))
                data.append(str(vital_signs[PRESION_ARTERIAL_DIASTOLICA_INDEX]))
                data.append(str(vital_signs[FRECUENCIA_RESPIRATORIA_INDEX]))
                data.append(str(vital_signs[SATURACION_DE_OXIGENO_INDEX]))
                data.append(str(float(vital_signs[TEMPERATURA_INDEX])))

                data.append(str(float(metrics[CIRCUNFERENCIA_DE_CUELLO_INDEX])))
                data.append(str(self.__get_bmi(metrics[TALLA_INDEX],
                                               metrics[PESO_INDEX])))

                data.append(self.yes_no_number(record[USO_DE_OXIGENO_INDEX]))
                data.append(self.yes_no_number(record[TABAQUISMO_INDEX]))
                data.append(self.yes_no_number(record[EXFUMADOR_INDEX]))
                data.append(self.yes_no_number(record[PRESENCIA_DE_RONQUIDO_INDEX]))

                data.append(diagnostic_aids[ESCALA_DE_EPWORTH_INDEX])
                data.append(diagnostic_aids[ET_CO2_INDEX])
                data.append(self.scale_mallampati_numner(diagnostic_aids[ESCALA_DE_MALLAMPATI_INDEX]))
                data.append(diagnostic_aids[PH_INDEX])
                data.append(diagnostic_aids[PCO2_INDEX])
                data.append(diagnostic_aids[PO2_INDEX])
                data.append(diagnostic_aids[EB_INDEX])
                data.append(diagnostic_aids[FVC_LITRO_INDEX])
                data.append(diagnostic_aids[FVC_INDEX])
                data.append(diagnostic_aids[FEV1_LITROS_INDEX])
                data.append(diagnostic_aids[FEV1L_INDEX])
                data.append(self.fev1lfvclitros(diagnostic_aids[FEV1_LITROS_INDEX],
                                                diagnostic_aids[FVC_LITRO_INDEX]))

                data.append(self.check_medicine(record[8]))

                data.append(self.yes_no_number(charlson_comorbidity[INFARTO_AGUDO_AL_MIOCARDIO_INDEX]))
                data.append(self.yes_no_number(charlson_comorbidity[ANTECEDENTE_DE_ACCIDENTE_CEREBROVASCULAR_INDEX]))
                data.append(self.yes_no_number(charlson_comorbidity[ENFERMEDAD_VASCULAR_PERIFERICA_INDEX]))
                data.append(self.yes_no_number(charlson_comorbidity[DEMENCIA_INDEX]))
                data.append(self.yes_no_number(charlson_comorbidity[EPOC_INDEX]))

                for i, value in enumerate(data):
                    try:
                        if value is not None:
                            data[i] = float(value)
                        else:
                            pass
                    except ValueError:
                        pass

                all_clinc_data.append(data)

        return all_clinc_data
    
    def __generate_polysomnography_list(self) -> list:
        db_controll = ControllDb()
        db_thread = DatabaseThread(
            target=db_controll.select_all_from_patients,
            args=()
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        patients = db_thread.join()
        all_polysomnography_data = list()

        for patient in patients:
            db_thread = DatabaseThread(
                target=db_controll.select_patient_id_date_apena_studies,
                args=(patient[ID_PATIENT_IDX],)
            )
            db_thread.start()
            insert_db_thread_event(db_thread.native_id)
            apnea_studies = db_thread.join()
            for apnea_study in apnea_studies:
                data = []
                db_thread = DatabaseThread(
                    target=db_controll.pdf_to_excel,
                    args=(apnea_study[ID_APNEA_STUDY_IDX],)
                )
                db_thread.start()
                insert_db_thread_event(db_thread.native_id)
                pdf = db_thread.join()

                if pdf is not None:
                    for i in pdf:
                        data.append(i)
                else:
                    for i in self.blank_fields():
                        data.append(i)
                
                for i, value in enumerate(data):
                    try:
                        if value is not None:
                            data[i] = float(value)
                        else:
                            pass
                    except ValueError:
                        pass
                
                all_polysomnography_data.append(data)

        
        return all_polysomnography_data
    
    def __generate_craneofacial_list(self) -> list:
        db_controll = ControllDb()
        db_multimedia = MultimediaDb()
        patients = self.__select_data_with_filter()
        all_craneofacial_data = list()

        for patient in patients:
            db_thread = DatabaseThread(
                target=db_controll.select_patient_id_date_apena_studies,
                args=(patient[ID_PATIENT_IDX],)
            )
            db_thread.start()
            insert_db_thread_event(db_thread.native_id)
            apnea_studies = db_thread.join()
            for apnea_study in apnea_studies:
                print("Apnea ID:", apnea_study[ID_APNEA_STUDY_IDX])
                data = []
                data = self.get_measures(data, apnea_study[ID_APNEA_STUDY_IDX],
                                        db_multimedia)
                
                for i, value in enumerate(data):
                    try:
                        if value is not None:
                            data[i] = float(value)
                        else:
                            pass
                    except ValueError:
                        pass

                all_craneofacial_data.append(data)
        
        return all_craneofacial_data

    def get_measures(self, data, id_apnea_study, db_multimedia: ControllDb):
        db_thread = DatabaseThread(
            target=db_multimedia.get_front_photo_data,
            args=(id_apnea_study,)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        front_photo = db_thread.join()
        db_thread = DatabaseThread(
            target=db_multimedia.get_lateral_photo_data,
            args=(id_apnea_study,)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        lateral_photo = db_thread.join()
        # Select all the images of the same apnea study
        study_images = [front_photo, lateral_photo]
        print(type(study_images[0]), type(study_images[1]))
        # Condition in case of no images loaded on that apnea study
        if study_images[0] is not None and study_images[1] is not None:
            for image_data in study_images:
                df = self.json_to_list(json.loads(
                                        json.loads(
                                        image_data[IMAGE_COORDINATES])))

                img_path = image_data[IMAGE_PATH]
                im = cv2.imread(img_path)
                facemesh = Facemesh(im, [], [])
                facemesh.qrCode()

                self.m = Measurements(df, facemesh.width, facemesh.height)
                self.m.generateScale(facemesh.qrs.qrCoords)

                if int(image_data[IMAGE_TAG]) == FRONT:
                    data = self.get_front_measurements(data)

                elif int(image_data[IMAGE_TAG]) == LATERAL:
                    data = self.get_profile_measurements(data, front_photo)

        return data

    def json_to_list(self, json):
        df = pd.DataFrame.from_dict(json)
        df.index.name = "Landmark"
        df.index = df.index.astype("int64")
        return df

    def get_front_measurements(self, data):
        data.append(str(self.m.getFaceWidth()))
        data.append(str(self.m.getFaceWidthAngle()))
        data.append(str(self.m.getIntercantalWidth()))
        data.append(str(self.m.getBiocularWidth()))
        data.append(str(self.m.getJawWidth()))
        data.append(str(self.m.getAreaMaxilarTriangle()))
        data.append(str(self.m.get_mandibular_width_angle()))
        data.append(str(self.m.get_nose_width()))

        return data

    def get_profile_measurements(self, data, front_photo):
        face_width = self.get_front_face_width(self.m.scale, self.m.w,
                                               front_photo)

        data.append(str(self.m.get_mandibular_nasion_angle()))
        data.append(str(self.m.get_mandibular_subnasion_angle()))
        data.append(str(self.m.get_anb_angle()))
        data.append(str(self.m.get_sm_gns()))
        data.append(str(self.m.get_middle_ranial_fossa_volume()*face_width))

        return data

    def get_front_face_width(self, scale, w, front_photo) -> float:
        if front_photo is None:
            faceWidth = -1
        else:
            # front[2] = coordinates
            points = json.loads(json.loads(front_photo[IMAGE_COORDINATES]))
            df = pd.DataFrame.from_dict(points)

            left = getXValueOfIndex(df, str(INDEX_EAR_LEFT))
            right = getXValueOfIndex(df, str(INDEX_EAR_RIGHT))
            faceWidth = ((right - left) * w) / scale

            # print("Face Width:", faceWidth, "cm")

        return round(faceWidth, 4)

    def calculate_age(self, born, study_date):
        return study_date.year - born.year - ((study_date.month,
                                               study_date.day) < (born.month, born.day))

    def __get_bmi(self, height, weight) -> float:
        return float(weight) / float((height**2))

    def patient_sex(self, num):
        if num == 1:
            sex = MALE
        elif num == 2:
            sex = FEMALE
        else:
            sex = OTHER

        return sex

    def yes_no_number(self, num):
        if num == 0:
            return NO
        else:
            return YES

    def scale_mallampati_numner(self, num):
        if num == int(DEGREE_1):
            return DEGREE_1
        elif num == int(DEGREE_2):
            return DEGREE_2
        elif num == int(DEGREE_3):
            return DEGREE_3
        elif num == int(DEGREE_4):
            return DEGREE_4
        elif num == int(DEGREE_5):
            return DEGREE_5
        else:
            return BLANK

    def fev1lfvclitros(self, fevl, fvfl) -> float:
        try:
            FEV1litros = float(fevl)
            FVClitros = float(fvfl)
        except:
            FEV1litros = 0
            FVClitros = 1

        try:
            division = FEV1litros / FVClitros
        except (ZeroDivisionError):
            division = -1

        return division

    def check_medicine(self, text):
        if len(text) == 0:
            return NO
        else:
            return YES

    def blank_fields(self):
        blank_list = []
        for i in range(25):
            blank_list.append("")

        return blank_list

    def __select_data_with_filter(self):
        if len(self._filters) == 7:
            patients = self.__filtered_data_distinct_gender()
        else:
            patients = self.__filtered_data_undistinct_gender()
        
        return patients
    
    def __filtered_data_distinct_gender(self) -> list[tuple]:
        db_controll = ControllDb()
        patients = db_controll.select_data_filtered_distinct_gender(
                self._filters
            )
        
        return patients
    
    def __filtered_data_undistinct_gender(self) -> list[tuple]:
        db_controll = ControllDb()

        patients = db_controll.select_data_filtered_undistinct_gender(
                self._filters
            )
        
        return patients

    def __preproces_data(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        if self._clinic_data_checkbox.isChecked():
            dataframe = dataframe.replace('',np.nan)
            dataframe = dataframe.replace(' ',np.nan)
            if self._craniofacial_checkbox.isChecked():
                dataframe = dataframe.drop([33])
            dataframe = dataframe.dropna(subset=dataframe.index[:35], axis='columns')
            drop_columns = list()
            data_flag = 0
            try:
                dataframe["ID"]
                drop_columns.append("ID")
                data_flag += 1
            except KeyError:
                data_flag += 0
            try:
                dataframe["Fecha Estudio"]
                drop_columns.append("Fecha Estudio")
            except KeyError:
                pass
            try:
                dataframe["Periodo de evaluación de flujo"]
                drop_columns.append("Periodo de evaluación de flujo")
                data_flag += 1
            except KeyError:
                data_flag += 0
            
            try:
                dataframe["Temperatura (º)"]
                drop_columns.append("Temperatura (º)")
                data_flag += 1
            except KeyError:
                data_flag += 0

            try:
                dataframe["ET CO2"]
                drop_columns.append("ET CO2")
                data_flag += 1
            except KeyError:
                data_flag += 0
            
            try:
                dataframe["FEV1L/FVCL"]
                drop_columns.append("FEV1L/FVCL")
                data_flag += 1
            except KeyError:
                data_flag += 0
            
            try:
                dataframe["Ingesta de medicamentos"]
                drop_columns.append("Ingesta de medicamentos")
                data_flag += 1
            except KeyError:
                data_flag += 0

            try:
                dataframe["Infarto agudo al miocardio"]
                drop_columns.append("Infarto agudo al miocardio")
                data_flag += 1
            except KeyError:
                data_flag += 0
            
            try:
                dataframe["Antecedente de accidente cerebrovascular"]
                drop_columns.append("Antecedente de accidente cerebrovascular")
                data_flag += 1
            except KeyError:
                data_flag += 0
            
            try:
                dataframe["Enfermedad vascular periferica"]
                drop_columns.append("Enfermedad vascular periferica")
                data_flag += 1
            except KeyError:
                data_flag += 0

            try:
                dataframe["Demencia"]
                drop_columns.append("Demencia")
                data_flag += 1
            except KeyError:
                data_flag += 0
            
            try:
                dataframe["EPOC"]
                drop_columns.append("EPOC")
                data_flag += 1
            except KeyError:
                data_flag += 0

        
            if len(drop_columns) > 0:
                dataframe = dataframe.drop(columns=drop_columns)
            else:
                pass

        if self._craniofacial_checkbox.isChecked():
            dataframe = dataframe.dropna(axis='index')

        transaction_dataframe, data_intervals = self.__discretize_data(dataframe)

        return transaction_dataframe, data_intervals

    def __discretize_data(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        discretize_clinc_data = Discretize(dataframe)
        # dataframe.to_csv(r"C:\Users\zaira\Downloads\test_dump.csv", index=False)
        dataframe = discretize_clinc_data.predefined_discretize(self.discretized_intervals)
        transaction_dataframe = discretize_clinc_data.transaction_discretize()
        data_intervals = discretize_clinc_data.get_data_invervals()

        return transaction_dataframe, data_intervals

    def __apriori(self, transaction_dataframe: pd.DataFrame) -> None:
        frequent_itemsets = apriori(transaction_dataframe,
                                    min_support=self._minimum_support_slider.value()/100,
                                    use_colnames=True,
                                    max_len=5,
                                    verbose=1)
        rules = association_rules(frequent_itemsets,
                                    metric='confidence',
                                    min_threshold=self._minimum_threshold_slider.value()/100)
        
        return rules

    def __add_rules_to_table(self, apriori_model: pd.DataFrame,
                             subjects_count: int,
                             caracteriztics_with_intervals: dict) -> None:
        self.__set_model()
        apriori_model["antecedents"] = apriori_model["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
        apriori_model["consequents"] = apriori_model["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")

        col_antecedents = list(apriori_model["antecedents"])
        col_consequents = list(apriori_model["consequents"])
        col_support = list(apriori_model["support"])
        col_confidence = list(apriori_model["confidence"])

        table_data_unordered = zip(col_antecedents,
                         col_consequents,
                         col_support,
                         col_confidence)
        
        table_data_ordered = sorted(table_data_unordered, key = lambda x: x[3],
                                    reverse=True)

        rows_limit = self._maximum_rules_slider.value()
        with open(r"bin\utils\generated_rules.txt", 'w', encoding="utf-8") as fd:
            self.__write_file_header(fd, subjects_count, caracteriztics_with_intervals)

            for i, row in enumerate(table_data_ordered):
                if rows_limit != 0:
                    confidence = str(row[2])
                    support = str(row[3])
                    if len(confidence) > 5:
                        confidence = confidence[:5]
                    if len(support) > 5:
                        support = support[:5]
                    self._model.setItem(i, 0, QStandardItem(support))
                    self._model.setItem(i, 1, QStandardItem(confidence))
                    self._model.setItem(i, 2, QStandardItem(str(row[0])))
                    self._model.setItem(i, 3, QStandardItem(str(row[1])))
                    rows_limit -= 1
                    fd.write(f"{i+1}{DELIM}{float(support):.3f}{DELIM}{float(confidence):.3f}{DELIM}{row[0]} -> {row[1]}\n")
                else:
                    break
        
        print()
    
    def __set_model(self):
        self._model.setHorizontalHeaderLabels(
            ['Soporte Mínimo', "Confianza", 'Antecedentes', 'Consecuentes'])
        self._filter_proxy_model.setSourceModel(self._model)
        self._filter_proxy_model.setFilterCaseSensitivity(False)
        self._filter_proxy_model.setFilterKeyColumn(2)
        self._results_table.verticalHeader().hide()
        self._results_table.setModel(self._filter_proxy_model)
        self._results_table.setSelectionBehavior(QTableView.SelectRows)
        self._results_table.setSelectionMode(QAbstractItemView.ContiguousSelection)

    def __check_option_selected(self) -> bool:
        check_box_flag = False

        if self._clinic_data_checkbox.isChecked():
            check_box_flag = True
        if self._polysomnography_checkbox.isChecked():
            check_box_flag = True
        if self._craniofacial_checkbox.isChecked():
            check_box_flag = True
        
        return check_box_flag
    
    def __define_data_selected_ranges(self) -> tuple[bool,bool]:
        clinic_data = False
        measures = False

        if self._clinic_data_checkbox.isChecked():
            clinic_data = True
        if self._craniofacial_checkbox.isChecked():
            measures = True
        
        return (clinic_data, measures)
    
    def __no_option_selected_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Seleccion de Opción")
        msg.setText("Favor de seleccionar una opción\npara iniciar el análisis.")
        msg.exec_()

    def __filters_applied_msg(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("Filtros Aplicados")
        msg.setText("Los filtros se han configurado\ncorrectamente.")
        msg.exec_()
    
    def __analisys_error_msg(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("Error de Análisis")
        msg.setText("Se a producido un error con los parámetros especificados.")
        msg.exec_()
    
    def __rules_exported_msg(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("Proceso Terminado")
        msg.setText("Las reglas se han exportado correctamente.")
        msg.exec_()

    def __write_file_header(self, fd: TextIOWrapper, subjects_count: int,
                            analisys_attributes: dict) -> None:
        if len(self._filters) == 7:
            gender = "Hombre" if self._filters[0] == 1 else "Mujer"
            index = 1
        else:
            gender = "Hombre y Mujer"
            index = 0

        fd.write("Análisis de Reglas de asosiación\n")
        fd.write(f"Fecha de Análisis: {datetime.today()}\n")
        fd.write(f"Numero de Sujetos: {subjects_count}\n\n")
        fd.write("Filtros Utilizados:\n")
        fd.write(f"Sexo{DELIM}{gender}\n")

        fd.write(f"IAH{DELIM}{self._filters[index]}")
        index += 1
        fd.write(f"{DELIM}{self._filters[index]}\n")
        index += 1

        fd.write(f"Edad{DELIM}{self._filters[index]}")
        index += 1
        fd.write(f"{DELIM}{self._filters[index]}\n")
        index += 1

        fd.write(f"Peso{DELIM}{self._filters[index]}")
        index += 1
        fd.write(f"{DELIM}{self._filters[index]}\n")

        fd.write(f"Soporte Mínimo{DELIM}{self._minimum_support_slider.value()}\n")
        fd.write(f"Confianza Mínima{DELIM}{self._minimum_threshold_slider.value()}\n\n")
        fd.write("Características y Rangos:\n")
        for attribute, intervals in analisys_attributes.items():
            fd.write(f"{attribute}{DELIM}{DELIM.join(sorted(intervals))}\n")
        fd.write('\n')
        fd.write("Reglas Generadas:\n")
        fd.write(f"No. Regla{DELIM}Soperte Mínimo{DELIM}Confianza Mínima{DELIM}Antecedente -> Consecuente\n\n")
    
    def __get_rules_caracteriztics_with_intervals(self, data_intervals) -> dict:
        rgx = r"\(-?[0-9].+,.+[0-9]"
        rgx_2 = r"\(-?[0-9](.+)?,(.+)?[0-9]"

        data_intervals = {}
        for i in transaction_table:
            try:
                interval = re.search(rgx_2, i).group()
                data = i.split(interval)[0]

                if data not in data_intervals:
                    data_intervals[data] = list()
                    data_intervals[data].append(interval + ']')
                else:
                    data_intervals[data].append(interval + ']')
            except:
                print(i)
        
        return data_intervals
    
    def __export_rules(self) -> None:
        dts_path = QFileDialog.getSaveFileName(self, "Destino a Exportar", str(
            pathlib.Path().absolute()), "TXT (*.txt)")
        org_path = r"bin\utils\generated_rules.txt"
        if dts_path[0] != "":
            try:
                shutil.copyfile(org_path, str(dts_path[0]))
                self.__rules_exported_msg()
            except shutil.SameFileError:
                pass
        

class Discretize:
    def __init__(self, data: pd.DataFrame) -> None:
        self._data: pd.DataFrame = data

    def discretize(self, number_intervals: int) -> pd.DataFrame:
        max_unique_values = 2
        self._transaction_columns = list()
        for column in self._data.columns:
            if len(self._data[column].unique()) > max_unique_values:
                self._data[column] = pd.cut(self._data[column], number_intervals)
            elif len(self._data[column].unique()) > max_unique_values - 1:
                self._data = self._data.drop(columns=[column])
            else:
                pass
        
        return self._data

    def predefined_discretize(self, number_intervals: int) -> pd.DataFrame:
        max_unique_values = 2
        self._transaction_columns = list()
        for column in self._data.columns:
            if len(self._data[column].unique()) > max_unique_values:
                if column == "Edad":
                    age_interval = pd.IntervalIndex.from_tuples(
                        [(0,40), (40,60), (60, 150)])
                    self._data[column] = pd.cut(self._data[column], age_interval)
                
                elif column == "IMC":
                    bmi_interval = pd.IntervalIndex.from_tuples(
                        [(0,25), (25,30), (30, 200)])
                    self._data[column] = pd.cut(self._data[column], bmi_interval)

                elif column == "Saturación de oxigeno (%)":
                    oxygen_saturation_interval = pd.IntervalIndex.from_tuples(
                        [(0,90), (90, 94), (94,100)])
                    self._data[column] = pd.cut(self._data[column], oxygen_saturation_interval)
                
                elif column == "circunferencia de cuello (cm)":
                    neck_circunference_interval = pd.IntervalIndex.from_tuples(
                        [(0,43), (43, 48), (48, 100)])
                    self._data[column] = pd.cut(self._data[column], neck_circunference_interval)
                
                elif column == "Escala de Epworth":
                    epwarth_scale_interval = pd.IntervalIndex.from_tuples(
                        [(-0.01,10), (10,15), (15,50)])
                    self._data[column] = pd.cut(self._data[column], epwarth_scale_interval)

                else:
                    self._data[column] = pd.cut(self._data[column], number_intervals)
            
            elif len(self._data[column].unique()) > max_unique_values - 1:
                self._data = self._data.drop(columns=[column])
            
            else:
                pass
        
        return self._data

    def get_data_invervals(self) -> dict:
        data_intervals = dict()

        for column in self._data.columns:
            data_intervals[column] = list()

            categories = self._data[column].unique()
            for category in categories.categories.T:

                data_intervals[column].append(str(category))
        
        return data_intervals
    
    def transaction_discretize(self) -> pd.DataFrame:
        transaction_dictionary = dict()
        for column in self._data.columns:
            columns_count = 1
            for column_unique_interval in self._data[column].unique():
                if column + ' ' + str(column_unique_interval) not in transaction_dictionary:
                    transaction_dictionary[column + ' ' + str(column_unique_interval)] = []
                else:
                    columns_count += 1
                    transaction_dictionary[column + ' ' + str(column_unique_interval) + str(columns_count)] = []
            for column_value in self._data[column]:
                for column_unique_interval in self._data[column].unique():
                    if column_value == column_unique_interval:
                        transaction_dictionary[column + ' ' + str(column_unique_interval)].append(True)
                    else:
                        transaction_dictionary[column + ' ' + str(column_unique_interval)].append(False)

        # a = pd.DataFrame(transaction_dictionary)
        # a.to_csv(r"C:\Users\zaira\Downloads\transaction_table.csv")
        return pd.DataFrame(transaction_dictionary)
