from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QCheckBox, QLineEdit
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, QMessageBox

import pathlib
import re

from log import Log

UI_PATH = "ui/rangeDiscretization.ui"

CLINIC_DATA_IDX = 0
MEASUREMENTS_IDX = 1

MALE = 1
FEMALE = 2
MIN_IAH = 0
MAX_IAH = 150
MIN_AGE = 0
MAX_AGE = 110
MIN_WEIGHT = 0
MAX_WEIGHT = 200
MIN_VALUE_IDX = 0
MAX_VALUE_IDX = 1
BLANK = ''
VALID_NUMBER_RGX = r"(?:^|[^\d,.])\d*(?:[,.]\d+)?(?:$|[^\d,.])$"

CLINIC_DATA_HEADER = ['Age', 'Heart rate', 'Systolic blood pressure', 'Diastolic blood pressure', 'Breathing frequency', 'Oxygen saturation', 'Temperature', 'Height', 'Neck circumference', 'Weight', 'Oxygen use', 'Smoking', 'Former smoker', 'Hypertension', 'Presence of snoring', 'Epworth scale', 'ET CO2', 'Mallampati scale', 'PH', 'pCO2', 'pO2', 'EB', 'FVC Litro', 'FVC%', 'FEV1 Litros', 'FEV1L%', 'FEV1L/FVCL', 'Medication intake', 'Acute myocardial infarction', 'History of cerebrovascular accident', 'Peripheral vascular disease', 'Dementia', 'EPOC', 'Charlson scale']
PDF_HEADER = ['IAH', 'Promedio de respiraciones por minuto', 'Indice de Apneas', 'Apneas', 'ÍAI', 'Apneas indeterminadas', 'ÍAO', 'Apneas obstructivas', 'ÍAC', 'Apneas centrales', 'ÍAM', 'Apneas mixtas', 'Indice de hipopneas', 'Hipoapneas', 'Eventos de ronquidos', 'IDO', 'Saturación promedio', 'Saturación <90%', 'Desaturación menor', 'Saturación <85%', 'Saturación <80%', 'Saturación basal', 'Frecuencia de pulso promedio', 'Proporcion de periodo CSR\nen el periodo de análisis', 'Periodo de evaluación de flujo']
MEASUREMENTS_HEADER = ['Ancho de cara', 'Ángulo Ancho de Cara', 'Ancho intercantal', 'Ancho Biocular', 'Ancho mandibular', 'Área triágulo maxilar', 'Ángulo Ancho de Mandibula', 'Ancho de Nariz', 'Àngulo Nasion Mandibular', 'Ángulo Sub-Nasion Mandibular', 'Ángulo ANB', 'Distancia Submental', 'Volumen Medio Fosa Craneal']


class RangeDiscretizationWidget(QWidget):
    def __init__(self, selected_data: tuple[bool,bool]):
        super(RangeDiscretizationWidget, self).__init__()
        self._selected_data = selected_data

        self.__load_ui_file(pathlib.Path(__file__).parent)
        self.__define_widgets()
        self.__define_fields()
        # self._apply_filters_button.clicked.connect(self.select_data_with_filter)
    
    def __load_ui_file(self, path) -> None:
        uic.loadUi(path / UI_PATH, self)
    
    def __define_widgets(self) -> None:
        self._main_grid = self.findChild(QGridLayout, "fieldsGridLayout")
        self._apply_ranges_button = self.findChild(QPushButton, "applyRangesButton")
        title_label = QLabel()
        attribute_header_label = QLabel()
        range_header_label = QLabel()
        default_range_header_label = QLabel()
        self._discretizated_values = []
        self._discretizated_values_header = []

        title_label.setText("Definition of Ranges")
        title_label.setStyleSheet("font-size: 30px")
        attribute_header_label.setText("Attribute")
        attribute_header_label.setStyleSheet("font-size: 25px")
        range_header_label.setText("Custom Range")
        range_header_label.setStyleSheet("font-size: 25px")
        default_range_header_label.setText("Default Range")
        default_range_header_label.setStyleSheet("font-size: 25px")

        self._main_grid.addWidget(title_label, 0,0,1,0, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(attribute_header_label, 1,0, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(range_header_label, 1,1, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(default_range_header_label, 1,2, alignment=Qt.AlignCenter)

        if self._selected_data[CLINIC_DATA_IDX]:
            self._discretizated_values_header += CLINIC_DATA_HEADER
        if self._selected_data[MEASUREMENTS_IDX]:
            self._discretizated_values_header += MEASUREMENTS_HEADER
    
    def __define_fields(self) -> None:
        row = 2
        column = 0

        for value in self._discretizated_values_header:
                attribute_name = QLabel(alignment=Qt.AlignCenter)
                attribute_name.setText(value)
                field_range = QLineEdit()
                default_range_box = QCheckBox()
                default_range_box.setChecked(True)
                default_range_box.setText('Default Range')
                field = (attribute_name, field_range, default_range_box)
                
                self._discretizated_values.append(field_range)

                self._main_grid.addWidget(field[0], row,column, alignment=Qt.AlignCenter)
                self._main_grid.addWidget(field[1], row,column+1, alignment=Qt.AlignCenter)
                self._main_grid.addWidget(field[2], row,column+2, alignment=Qt.AlignCenter)

                row += 1

def validate_fields(min_value: float, max_value: float) -> bool:
        valid_fields = False

        if re.match(VALID_NUMBER_RGX, str(min_value)) and \
                re.match(VALID_NUMBER_RGX, str(max_value)) and \
                    valid_range_values(min_value, max_value):
            
            valid_fields = True

        return valid_fields
    
def valid_range_values(min_value: float, max_value: float) -> bool:
    valid_range = False

    if min_value <= max_value:
        valid_range = True
    
    return valid_range
