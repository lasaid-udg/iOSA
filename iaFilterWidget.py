from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QRadioButton, QLineEdit
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, QMessageBox

import pathlib
import re

from log import Log

UI_PATH = "ui/filtersWidget.ui"
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


class iaFiltersWidget(QWidget):
    def __init__(self):
        super(iaFiltersWidget, self).__init__()

        self.__load_ui_file(pathlib.Path(__file__).parent)
        self.__define_widgets()
        # self._apply_filters_button.clicked.connect(self.select_data_with_filter)
    
    def __load_ui_file(self, path) -> None:
        uic.loadUi(path / UI_PATH, self)
    
    def __define_widgets(self) -> None:
        self._main_grid = self.findChild(QGridLayout, "mainGridLayout")
        title_label = QLabel()
        gender_label = QLabel()
        iah_title_label = QLabel()
        age_title_label = QLabel()
        weight_title_label = QLabel()
        self._male_radio_button = QRadioButton()
        self._female_radio_button = QRadioButton()
        self._both_radio_button = QRadioButton()
        self._iah_range_inclusive = QLineEdit()
        self._iah_range_exclusive = QLineEdit()
        self._age_range_inclusive = QLineEdit()
        self._age_range_exclusive = QLineEdit()
        self._weight_range_inclusive = QLineEdit()
        self._weight_range_exclusive = QLineEdit()
        self._apply_filters_button = QPushButton()

        title_label.setText("Selección de Filtros")
        title_label.setStyleSheet("font-size: 30px")
        gender_label.setText("Sexo")
        self._male_radio_button.setText("Hombre")
        self._female_radio_button.setText("Mujer")
        self._both_radio_button.setText("Ambos")
        iah_title_label.setText("Índice IAH")
        age_title_label.setText("Edad")
        weight_title_label.setText("Peso")
        self._apply_filters_button.setText("Aplicar Filtros")

        self._iah_range_inclusive.setText("0")
        self._iah_range_exclusive.setText("150")
        self._age_range_inclusive.setText("0")
        self._age_range_exclusive.setText("150")
        self._weight_range_inclusive.setText("0")
        self._weight_range_exclusive.setText("200")

        self._main_grid.addWidget(title_label, 0,0,1,0, alignment=Qt.AlignCenter)

        self._main_grid.addWidget(gender_label, 1,0,1,0, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(self._male_radio_button, 2,0, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(self._female_radio_button, 2,1, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(self._both_radio_button, 2,2, alignment=Qt.AlignCenter)
        
        self._main_grid.addWidget(iah_title_label, 3,0,1,0, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(self._iah_range_inclusive, 4,0, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(QLabel(" de | a "), 4,1, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(self._iah_range_exclusive, 4,2, alignment=Qt.AlignCenter)

        self._main_grid.addWidget(age_title_label, 5,0,1,0, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(self._age_range_inclusive, 6,0, alignment=Qt.AlignCenter) 
        self._main_grid.addWidget(QLabel(" de | a "), 6,1, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(self._age_range_exclusive, 6,2, alignment=Qt.AlignCenter)
        
        self._main_grid.addWidget(weight_title_label, 7,0,1,0, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(self._weight_range_inclusive, 8,0, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(QLabel(" de | a "), 8,1, alignment=Qt.AlignCenter)
        self._main_grid.addWidget(self._weight_range_exclusive, 8,2, alignment=Qt.AlignCenter)
        
        self._main_grid.addWidget(self._apply_filters_button, 9,0,2,0, alignment=Qt.AlignCenter)
    
    def select_data_with_filter(self) -> None:
        if self._both_radio_button.isChecked():
            filter_options = self.__filtered_data_undistinct_gender()
        
        elif self._female_radio_button.isChecked() or self._male_radio_button.isChecked():
            filter_options = self.__filtered_data_distinct_gender()
        
        else:
            filter_options = self.__filtered_data_undistinct_gender()
        
        return filter_options
    
    def __filtered_data_distinct_gender(self) -> tuple:
        try:
            iah_range = get_range_values(float(self._iah_range_inclusive.text()),
                                               float(self._iah_range_exclusive.text()))
            age_range = get_range_values(float(self._age_range_inclusive.text()),
                                               float(self._age_range_exclusive.text()))
            weight_range = get_range_values(float(self._weight_range_inclusive.text()),
                                                  float(self._weight_range_exclusive.text()))
            gender = FEMALE if self._female_radio_button.isChecked() else MALE
            
            filter_options = (gender,
            iah_range[MIN_VALUE_IDX],
            iah_range[MAX_VALUE_IDX],
            age_range[MIN_VALUE_IDX],
            age_range[MAX_VALUE_IDX],
            weight_range[MIN_VALUE_IDX],
            weight_range[MAX_VALUE_IDX]
            )
        
            return filter_options
    
        except Exception as e:
            self.__invalid_input()
            log = Log()
            log.insert_log_error(str(e))
    
    def __filtered_data_undistinct_gender(self) -> list[tuple]:
        try:
            iah_range = get_range_values(float(self._iah_range_inclusive.text()),
                                               float(self._iah_range_exclusive.text()))
            age_range = get_range_values(float(self._age_range_inclusive.text()),
                                               float(self._age_range_exclusive.text()))
            weight_range = get_range_values(float(self._weight_range_inclusive.text()),
                                                  float(self._weight_range_exclusive.text()))
            
            filter_options = (
            iah_range[MIN_VALUE_IDX],
            iah_range[MAX_VALUE_IDX],
            age_range[MIN_VALUE_IDX],
            age_range[MAX_VALUE_IDX],
            weight_range[MIN_VALUE_IDX],
            weight_range[MAX_VALUE_IDX]
            )

            return filter_options
    
        except Exception as e:
            log = Log()
            log.insert_log_error(str(e))
            self.__invalid_input()

    def __invalid_input(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("Valor Inválido")
        msg.setText("El valor ingresado no es válido.")
        msg.exec_()


def get_range_values(min_value: float, max_value: float) -> tuple[int, int]:
    
    if validate_fields(min_value, max_value):
        max_value -= 0.001
        return (min_value, max_value)

    else:
        raise ValueError

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
