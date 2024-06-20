'''
Created By: Geravid
Date: 20/12/2021 14:50:37
Last Update 25/06/2023 22:56:21

Program for read reports in PDF files and extract patien medic data.
'''
# Tesseract required. (3 hours lost because of this "little" detail, so please, take note...)

PATH = R"C:\Users\EricG\Desktop\SA2\BackUpIMSS\2023-06-06\Raw\POLIGRAFIAS PDF\BAJ.pdf"
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import fitz # PyMuPDF library. (ver. 1.19.3)
from PIL import Image   # Pillow (ver. 8.4.0)
import io
from pytesseract import pytesseract # Tesseract (ver. 0.3.8)
import re
from pathlib import Path
import unicodedata

from log import Log

LST_START = 0
INDEX = 0
DATA = 1
TITLE_1 = 0
REGISTRY = 0
EVALUATION = 1
BLANK = ''
DL = '|'
COMMENTS_STOP = "Versión del firmware"

IMAGE_RGX = "[<](.*?)[>]"
PATIENT_DATA_RGX = "Datos del paciente"
EVALUATION_REGISTRY_RGX = "Registrando"
ANALISYS_RGX = "* Consulte el Manual Clínico para obtener información sobre las abreviaturas y los parámetros estándar de ResMed"
DATA_TITLE_RGX = ".+[:]"
TITLE_TEXT_ONLY = "([:].*)|\.*"
ONLY_TEXT_RGX = "(\w\s)*"
TIME_RGX = "\d+[:]\d+.*"
DATE_RGX = "\d+[/]\d+[/]\d+"
NUMBERS_SPACES_RGX = "\d+\s*"
NATURAL_NUMBERS_SPACES_RGX = "\d+(\s*\w*)*"
DECIMAL_NUMBERS_SPACES_METRIC_RGX = "\d*[\.]*\d*(\s*\w*)*"
DECIMAL_NUMBERS_PER_RGX = "\d*\s*%*"
DURATION_REGISTRY_EVAL_RGX = "\d+\s*\w*\s*\d+\s*\w*"
BRACKETS_ANALISYS_RGX = "(?<=\[).+?(?=\])"
BRACKETS_RGX = "\[|\]"
SEMICOLON = ";"
ONLY_SPACES_RGX = "\s+"
ALL_RGX = ".*"

PATTERN_NAME = ["Nombre"]
PATTERN_PATIENT_ID = ["ID paciente"]
PATTERN_BIRTH_DAY = ["Fecha de nac"]
PATTERN_STREET = ["Calle"]
PATTERN_HEIGH = ["Altura"]
PATTERN_CP_CITY = ["Código postal, ciudad"]
PATTERN_WEIGHT = ["Peso"]
PATTERN_PHONE = ["Teléfono"]
PATTERN_BMI = ["IMC"]
PATTERN_DATE = ["Fecha"]
PATTERN_START_TIME = ["Inicio"]
PATTERN_END_TIME = ["Fin"]
PATTERN_DURATION = ["Duración"]
PATTERN_IAH = ["IAH"]
PATTERN_AVERAGE_RMP = ["Promedio de respiraciones por minuto [rpm]"]
PATTERN_IR = ["IR"]
PATTERN_RESPIRATIONS = ["Respiraciones"]
PATTERN_APNEA_INDEX = ["Índice de apneas"]
PATTERN_APNEAS = ["Apneas"]
PATTERN_IAI = ["ÍAI"]
PATTERN_INDETERMINATED_APNEAS = ["Apneas indeterminadas"]
PATTERN_IAO = ["ÍAO"]
PATTERN_OBSTRUCTIVE_APNEAS = ["Apneas obstructivas"]
PATTERN_IAC = ["ÍAC"]
PATTERN_CENTRAL_APNEAS = ["Apneas centrales"]
PATTERN_IAM = ["ÍAM"]
PATTERN_MIXED_APNEAS = ["Apneas mixtas"]
PATTERN_HYPOAPNEA_INDEX = ["Índice de hipopnea"]
PATTERN_HYPOAPNEA = ["Hipopneas"]
PATTERN_LF_P = [r"% lim Flujo Res sin Ron (Lf)"]
PATTERN_LF = ["Lim Flujo Res sin Ron (Lf)"]
PATTERN_LR_P = [r"% lim Flujo Res con Ron (LR)"]
PATTERN_LR = ["Lim flujo Res con Ron (LR)"]
PATTERN_SNORING_EVENTS = ["Eventos de ronquidos"]
PATTERN_IDO = ["Oxígeno"]
PATTERN_DESATURATIONS_COUNT = ["Nº de desaturaciones"]
PATTERN_AVERAGE_SATURATION = ["Saturación promedio"]
PATTERN_SATURATION_90 = ["SaturaciónA"]
PATTERN_MINOR_SATURATION = ["Desaturación menor"]
PATTERN_SATURATION_85 = ["SaturaciónB"]
PATTERN_LOWEST_SATURATION = ["Saturación más baja"]
PATTERN_SATURATION_80 = ["SaturaciónC"]
PATTERN_BASAL_SATURATION = ["Saturación basal"]
PATTERN_MINIMUM_PULSE_RATE = ["Frecuencia de pulso mínima"]
PATTERN_MAXIMUM_PULSE_RATE = ["Frecuencia de pulso máxima"]
PATTERN_AVERAGE_PULSE_RATE = ["Frecuencia de pulso promedio"]
PATTERN_CSR = ["período de análisis"]
PATTERN_ANALISYS_PARAMETERS = ["Estado del análisis"]
PATTERN_COMMENTS = ["Comentarios"]
PATTERN_DEFAULT_APNEA = ["Apnea"]
PATTERN_DEFAULT_HYPOAPNEA = ["Hipopnea"]
PATTERN_DEFAULT_SNORING = ["Ronquido"]
PATTERN_DEFAULT_DESATURATION = ["Desaturación"]
PATTERN_DEFAULT_CSR = ["CSR"]

NAME = "name"
ID_PATIENT = "id_patient"
BIRTH_DAY = "birth_date"
STREET = "street"
HEIGH = "height"
CP_CITY = "cp_city"
WEIGHT = "weight"
PHONE = "phone"
BMI = "bmi"
REGISTRY_EVAL_DATE = "registry_eval_date"
REGISTRY_EVAL_START_TIME = "registry_eval_start_time"
REGISTRY_EVAL_END_TIME = "registry_eval_end_time"
REGISTRY_EVAL_DURATION = "registry_eval_duration"
IAH = "IAH"
AVERAGE_RPM = "AVERAGE_RPM"
IR = "IR"
RESPIRATIONS = "Respirations"
APNEA_INDEX = "ApneaIndex"
APNEAS = "Apneas"
IAI = "IAI"
INDETERMINATED_APNEAS = "IndeterminateApneas"
IAO = "IAO"
OBSTRUCTIVE_APNEAS = "ObstructiveApneas"
IAC = "IAC"
CENTRAL_APNEAS= "CentralApneas"
IAM = "IAM"
MIXED_APNEAS = "MixedApneas"
HYPOAPNEA_INDEX = "HypopneaIndex"
HYPOAPNEA = "Hypopnea"
LF_P = "%Lf"
LF = "Lf"
LR_P = "%LR"
LR = "LR"
SNORING_EVENTS = "SnoringEvents"
IDO = "IDO"
DESATURATIONS_COUNT = "DesaturationsNumber"
AVERAGE_SATURATION = "AverageSaturation"
SATURATION_90 = "90%Saturation"
MINOR_SATURATION = "MinorDesaturation"
SATURATION_85 = "85%Saturation"
LOWEST_SATURATION = "LowestSaturation"
SATURATION_80 = "80%Saturation"
BASAL_SATURATION = "BasalSaturation"
MINIMUM_PULSE_RATE = "MinimumPulseRate"
MAXIMUM_PULSE_RATE = "MaximumPulseRate"
AVERAGE_PULSE_RATE = "AveragePulseRate"
CSR = "CSR"
DEFAULT_APNEA = "DefaultApnea"
DEFAULT_HYPOAPNEA = "DefaultHypopnea"
DEFAULT_SNORING = "DefaultSnoring"
DEFAULT_DESATURATION = "DefaultDesaturation"
DEFAULT_CSR = "DefaultCSR"
COMMENTS = "Comments"
EVALUATION_DURATION = "EvaluationDuration"


EXTRACTED_DATA = {
    NAME : BLANK,
    ID_PATIENT : BLANK,
    BIRTH_DAY : BLANK,
    STREET : BLANK,
    HEIGH : BLANK,
    WEIGHT : BLANK,
    CP_CITY : BLANK,
    PHONE : BLANK,
    BMI : BLANK,
    REGISTRY_EVAL_DATE : BLANK,
    REGISTRY_EVAL_START_TIME : [],  # [0] = Registry and [1] = Evaluation
    REGISTRY_EVAL_END_TIME : [],    # [0] = Registry and [1] = Evaluation
    REGISTRY_EVAL_DURATION: [],     # [0] = Registry and [1] = Evaluation
    IAH : BLANK,
    AVERAGE_RPM : BLANK,
    IR : BLANK,
    RESPIRATIONS : BLANK,
    APNEA_INDEX : BLANK,
    APNEAS : BLANK,
    IAI : BLANK,
    INDETERMINATED_APNEAS  : BLANK,
    IAO : BLANK,
    OBSTRUCTIVE_APNEAS : BLANK,
    IAC : BLANK,
    CENTRAL_APNEAS : BLANK,
    IAM : BLANK,
    MIXED_APNEAS : BLANK,
    HYPOAPNEA_INDEX : BLANK,
    HYPOAPNEA : BLANK,
    LF_P : BLANK,
    LF : BLANK,
    LR_P : BLANK,
    LR : BLANK,
    SNORING_EVENTS : BLANK,
    IDO : BLANK,
    DESATURATIONS_COUNT : BLANK,
    AVERAGE_SATURATION : BLANK,
    SATURATION_90 : BLANK,
    MINOR_SATURATION : BLANK,
    SATURATION_85 : BLANK,
    LOWEST_SATURATION : BLANK,
    SATURATION_80 : BLANK,
    BASAL_SATURATION : BLANK,
    MINIMUM_PULSE_RATE : BLANK,
    MAXIMUM_PULSE_RATE : BLANK,
    AVERAGE_PULSE_RATE : BLANK,
    CSR : BLANK,
    DEFAULT_APNEA : BLANK,
    DEFAULT_HYPOAPNEA : BLANK,
    DEFAULT_SNORING : BLANK,
    DEFAULT_DESATURATION : BLANK,
    DEFAULT_CSR : BLANK,
    COMMENTS : BLANK,
    EVALUATION_DURATION : BLANK
}

NFKD = "NFKD"
ASCII = "ASCII"
IGNORE = "ignore"


class ExtractPdfData():
    def __init__(self, path: Path) -> None:
        self._pdf_path = path
        self._image_lst = list()
        self.extracted_data = dict()

    def extract_data(self) -> bool:
        text = self.__read_pdf()
        self.__initialize_data()
        # print(text)
        last_value = BLANK
        data = list()
        pos = LST_START
        img_cont = LST_START
        cont = LST_START
        while last_value != COMMENTS_STOP and cont < len(text):
            last_value = text[pos]
            # print("Last Value:", last_value)

            if re.match(IMAGE_RGX, last_value):
                img_cont += 1
            
            else:

                if re.match(ONLY_TEXT_RGX, last_value):
            
                    if re.match(DATA_TITLE_RGX, last_value):

                        last_value = re.sub(TITLE_TEXT_ONLY, BLANK, last_value)
                        
                        if re.match(IMAGE_RGX, text[pos + 1]):
                            dt = self.__text_from_image(img_cont)
                            data.append((last_value, dt))
                            text.pop(pos + 1)
                            img_cont += 1

                        elif re.match(TIME_RGX, text[pos + 1]):
                            dt = text[pos + 1]
                            data.append((last_value, dt))
                            text.pop(pos + 1)

                        elif re.match(DATA_TITLE_RGX, text[pos + 1]):
                            dt = BLANK
                            data.append((last_value, dt))

                        else:
                            dt = text[pos + 1]
                            data.append((last_value, dt))
                            text.pop(pos + 1)
                    else:
                        dt = BLANK
                        data.append((last_value, dt))
                    
                    # print("Data:", dt)
                else:
                    pass

            pos += 1
            cont += 1
        
        self.__standardize_extracted_data(data)

        '''
        for k, v in self.extracted_data.items():
            print(k, ':', v)
        '''
        

    def __read_pdf(self) -> list[any]:
        self._doc = fitz.open(self._pdf_path)
        pages = len(self._doc)

        first_page = self._doc[0]
        self._image_lst = first_page.get_images()

        data = list()
        for i in range(pages):
            page = self._doc.load_page(i)
            data.append(page.get_text("blocks"))
        #print(data)
        text = list()
        
        for block in data:
            for line in block:
                # print(line[4])
                text.append(re.sub("\s{2}", BLANK, re.sub('\n', DL, line[4])))
            
        text = self.__clean_text(text)
        text = self.__handle_text(text)
        
        return text

    def __handle_text(self, text: list[any]) -> list[any]:
        only_text = list()

        for line in text:
            for data in line.split(DL):
                # print(data)
                if data == BLANK:
                    pass
                else:
                    only_text.append(data)

        return only_text

    def __clean_text(self, text: list[any]) -> list[any]:
        clean_text = list()

        for i in text:
            try:
                i = re.sub("Análisis(.*? / .*?)Índices|Análisis(.*?)Índices",
                            BLANK, i)
                i = re.sub("< 5 / h", BLANK, i)
                i = re.sub("< 5", BLANK, i)
                i = re.sub("< Aprox. 60", BLANK, i)
                i = re.sub("< Aprox. 40", BLANK, i)
                i = re.sub("94% - 98%", BLANK, i)
                i = re.sub("Saturación <= 90%", 'SaturaciónA', i)
                i = re.sub("Saturación <= 85%", 'SaturaciónB', i)
                i = re.sub("Saturación <= 80%", 'SaturaciónC', i)
                i = re.sub("90% - 98%", BLANK, i)
                i = re.sub("< 40 bpm", BLANK, i)
                i = re.sub("> 40 bpm", BLANK, i)
                i = re.sub("< 90 bpm", BLANK, i)
                i = re.sub("-", BLANK, i)
                i = re.sub("\*", BLANK, i)
                if re.match("\s", i):
                    i = re.sub("^.", BLANK, i)
                clean_text.append(i)

            # If don't found something it throw an "AttributeError". 
            # So we catch it and avoid it.
            except AttributeError:
                break


        return clean_text

    def __text_from_image(self, image_cont: int) -> str:
        # The first two image are skipped.
        if image_cont > 1:
            zoom_x = 2.0  # horizontal zoom
            zoom_y = 2.0  # vertical zoom
            mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension
            # The path to "Tesseract-ocr".
            # pytesseract.tesseract_cmd = r"C:\Users\Nineteen002\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
            pytesseract.tesseract_cmd = TESSERACT_PATH

            # # Access XREF of the image.
            xref = self._image_lst[image_cont][0]

            # Extract image information.
            img_info = self._doc.extract_image(xref)

            # Extract image bytes.
            image_bytes = img_info["image"]

            # Load the image to PIL for the text extraction.
            image_open = Image.open(io.BytesIO(image_bytes))
            width, height = image_open.size
            width *= 5
            height *= 5

            new_size = (width, height)

            image_open.resize(new_size)

            # Use tesseract to extract the text on the image.
            text = pytesseract.image_to_string(image_open)

            # Returns the extracted test or a none value.
            while True:
                try:
                    return re.search("(\d+(?:\.\d+|[%])?)",text[:-1]).group()
                except AttributeError:
                    break
        else:
            return "None"

    def __standardize_extracted_data(self, raw_data: list) -> None:
        start_time_pos = 0
        end_time_pos = 0
        duration_pos = 0
        for idx, rd in enumerate(raw_data):
            # print(rd)
            # Patient name
            if self.__string_comparison(rd[LST_START],
                                        PATTERN_NAME[TITLE_1]):
                try:
                    self.extracted_data[NAME] = self.extracted_data[NAME] + rd[DATA] + ' '

                except:
                    self.extracted_data[NAME] = BLANK
                    
            # Patiend Id number
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_PATIENT_ID[TITLE_1]):
                self.__parse_value(ID_PATIENT,NUMBERS_SPACES_RGX,rd[DATA])
            # Patient birth date
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_BIRTH_DAY[TITLE_1]):
                self.__parse_value(BIRTH_DAY,DATE_RGX,rd[DATA])
            # Patient street
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_STREET[TITLE_1]):
                self.__parse_value(STREET,ALL_RGX,rd[DATA]) # ALL
            # Patient height
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_HEIGH[TITLE_1]):
                self.__parse_value(HEIGH,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # Patient city and cp
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_CP_CITY[TITLE_1]):
                self.__parse_value(CP_CITY,ALL_RGX,rd[DATA]) #ALL
            # Patient weight
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_WEIGHT[TITLE_1]):
                self.__parse_value(WEIGHT,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # Patient phone
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_PHONE[TITLE_1]):
                self.__parse_value(PHONE,NUMBERS_SPACES_RGX,rd[DATA])
            # Patient bmi
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_BMI[TITLE_1]):
                self.__parse_value(BMI,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # Evaluation and registry date
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_DATE[TITLE_1]):
                self.__parse_value(REGISTRY_EVAL_DATE,DATE_RGX,rd[DATA])
            # Evaluation and registry start time
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_START_TIME[TITLE_1]):
                self.__parse_value_to_lst(start_time_pos,
                                            REGISTRY_EVAL_START_TIME,
                                            TIME_RGX,rd[DATA])
                start_time_pos = 1
            # Evaluation and registry end time
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_END_TIME[TITLE_1]):
                self.__parse_value_to_lst(end_time_pos, REGISTRY_EVAL_END_TIME,
                                            TIME_RGX,rd[DATA])
                end_time_pos = 1
            # Evaluation and registry duration
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_DURATION[TITLE_1]):
                
                self.__parse_value_to_lst(duration_pos, REGISTRY_EVAL_DURATION,
                                            DURATION_REGISTRY_EVAL_RGX,
                                            rd[DATA])
                duration_pos = 1
            # IAH
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_IAH[TITLE_1]):
                self.__parse_value(IAH,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # AVERAGE RMP
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_AVERAGE_RMP[TITLE_1]):
                self.__parse_value(AVERAGE_RPM,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # IR
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_IR[TITLE_1]):
                self.__parse_value(IR,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # RESPIRATIONS
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_RESPIRATIONS[TITLE_1]):
                self.__parse_value(RESPIRATIONS,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # APNEA INDEX
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_APNEA_INDEX[TITLE_1]):
                self.__parse_value(APNEA_INDEX,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # APNEAS
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_APNEAS[TITLE_1]):
                self.__parse_value(APNEAS,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # IAI
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_IAI[TITLE_1]):
                self.__parse_value(IAI,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # INDETERMINATED APNEAS
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_INDETERMINATED_APNEAS[TITLE_1]):
                self.__parse_value(INDETERMINATED_APNEAS,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # IA0
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_IAO[TITLE_1]):
                self.__parse_value(IAO,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # OBSTRUCTIVE APNEAS
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_OBSTRUCTIVE_APNEAS[TITLE_1]):
                self.__parse_value(OBSTRUCTIVE_APNEAS,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # IAC
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_IAC[TITLE_1]):
                self.__parse_value(IAC,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # CENTRAL_APNEAS
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_CENTRAL_APNEAS[TITLE_1]):
                self.__parse_value(CENTRAL_APNEAS,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # IAM
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_IAM[TITLE_1]):
                self.__parse_value(IAM,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # MIXED APNEAS
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_MIXED_APNEAS[TITLE_1]):
                self.__parse_value(MIXED_APNEAS,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # HYPOAPNEA INDEX
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_HYPOAPNEA_INDEX[TITLE_1]):
                self.__parse_value(HYPOAPNEA_INDEX,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # HYPOAPNEA
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_HYPOAPNEA[TITLE_1]):
                self.__parse_value(HYPOAPNEA,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # % lim. Flujo Res sin Ron (Lf)
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_LF_P[TITLE_1]):
                self.__parse_value(LF_P,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # Lim. Flujo Res sin Ron (Lf)
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_LF[TITLE_1]):
                self.__parse_value(LF,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # % lim. Flujo Res con Ron (LR)
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_LR_P[TITLE_1]):
                self.__parse_value(LR_P,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # Lim. flujo Res con Ron (LR)
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_LR[TITLE_1]):
                self.__parse_value(LR,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # SNORING EVENTS
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_SNORING_EVENTS[TITLE_1]):
                self.__parse_value(SNORING_EVENTS,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                        rd[DATA])
            # IDO
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_IDO[TITLE_1]):
                self.__parse_value(IDO,DECIMAL_NUMBERS_SPACES_METRIC_RGX,
                                    rd[DATA])
            # DESATURATIONS COUNT
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_DESATURATIONS_COUNT[TITLE_1]):
                self.__parse_value(DESATURATIONS_COUNT,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # AVERAGE SATURATION
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_AVERAGE_SATURATION[TITLE_1]):
                self.__parse_value(AVERAGE_SATURATION,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # SATURATION 90
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_SATURATION_90[TITLE_1]):
                self.__parse_value_percetage(SATURATION_90,
                                    DECIMAL_NUMBERS_PER_RGX, rd[DATA])
            # MINOR SATURATION
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_MINOR_SATURATION[TITLE_1]):
                self.__parse_value(MINOR_SATURATION,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # SATURATION 85
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_SATURATION_85[TITLE_1]):
                self.__parse_value_percetage(SATURATION_85,
                                    DECIMAL_NUMBERS_PER_RGX, rd[DATA])
            # LOWEST SATURATION
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_LOWEST_SATURATION[TITLE_1]):
                self.__parse_value(LOWEST_SATURATION,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # SATURATION 80
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_SATURATION_80[TITLE_1]):
                self.__parse_value_percetage(SATURATION_80,
                                    DECIMAL_NUMBERS_PER_RGX, rd[DATA])
            # BASAL SATURATION
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_BASAL_SATURATION[TITLE_1]):
                self.__parse_value(BASAL_SATURATION,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # MINIMUM PULSE RATE
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_MINIMUM_PULSE_RATE[TITLE_1]):
                self.__parse_value(MINIMUM_PULSE_RATE,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # MAXIMUM PULSE RATE
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_MAXIMUM_PULSE_RATE[TITLE_1]):
                self.__parse_value(MAXIMUM_PULSE_RATE,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # AVERAGE PULSE RATE
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_AVERAGE_PULSE_RATE[TITLE_1]):
                self.__parse_value(AVERAGE_PULSE_RATE,
                                    DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # CSR
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_CSR[TITLE_1]):
                self.__parse_value(CSR,DECIMAL_NUMBERS_SPACES_METRIC_RGX,rd[DATA])
            # PATTERN ANALISYS PARAMETERS
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_ANALISYS_PARAMETERS[TITLE_1]):
                self.__parse_multivalue_value(BRACKETS_ANALISYS_RGX,
                                                raw_data[idx + 1][INDEX])
            # COMMENTS
            elif self.__string_comparison(rd[LST_START],
                                        PATTERN_COMMENTS[TITLE_1]):
                self.__parse_value(COMMENTS,ALL_RGX,
                                    raw_data[idx + 1][INDEX])
            else:
                pass
        # Set evaluation duration
        try:
            self.extracted_data[EVALUATION_DURATION] = self.extracted_data[REGISTRY_EVAL_DURATION][EVALUATION]
        except:
            log = Log()
            log.insert_log_error()

    def __string_comparison(self, s1: str, s2: str) -> bool:
        if unicodedata.normalize(NFKD, s1).encode(ASCII,
            IGNORE).strip().lower() == unicodedata.normalize(NFKD,
            s2).encode(ASCII, IGNORE).strip().lower():
            
            return True
        else:
            return False
    
    def __parse_value(self, idx: str, rgx: str, value: str) -> None:
        try:
            # print(value)
            self.extracted_data[idx] = re.search(rgx, value).group()
        except Exception as e:
            # print(e)
            self.extracted_data[idx] = BLANK
            log = Log()
            log.insert_log_error()
    
    def __parse_value_to_lst(self, pos: int, idx: str, rgx: str, value: str) -> None:
        try:
            rslt = re.search(rgx, value).group()
            tup = self.extracted_data.get(idx)
            # tup.append(rslt)
            if pos == REGISTRY:
                tup.insert(pos, rslt)
            elif pos == EVALUATION:
                tup.insert(pos, rslt)
            else:
                pass
            self.extracted_data[idx] = tup
        except:
            self.extracted_data[idx] = BLANK
            log = Log()
            log.insert_log_error()
    
    def __parse_value_percetage(self, idx: str, rgx: str, value: str) -> None:
        try:
            data = ""
            for match in re.finditer(rgx, value):
                data += match.group()
            
            self.extracted_data[idx] = data
        except:
            self.extracted_data[idx] = BLANK
            log = Log()
            log.insert_log_error()
    
    def __parse_multivalue_value(self, rgx: str, value: str) -> None:
        try:
            brackets_data = list()
            for match in re.finditer(rgx, value):
                brackets_data.append(match.group())
            
            titles = re.sub(rgx, BLANK, value)
            titles = re.sub(BRACKETS_RGX, BLANK, titles)
            titles = re.sub(SEMICOLON, DL, titles)
            titles = re.sub(ONLY_SPACES_RGX, BLANK, titles)

            for title, data in zip(titles.split(DL), brackets_data):
                if self.__string_comparison(title, PATTERN_DEFAULT_APNEA[TITLE_1]):
                    self.extracted_data[DEFAULT_APNEA] = data
                elif self.__string_comparison(title,
                                                PATTERN_DEFAULT_HYPOAPNEA[TITLE_1]):
                    self.extracted_data[DEFAULT_HYPOAPNEA] = data
                elif self.__string_comparison(title,
                                                PATTERN_DEFAULT_SNORING[TITLE_1]):
                    self.extracted_data[DEFAULT_SNORING] = data
                elif self.__string_comparison(title,
                                                PATTERN_DEFAULT_DESATURATION[TITLE_1]):
                    self.extracted_data[DEFAULT_DESATURATION] = data
                elif self.__string_comparison(title,
                                                PATTERN_DEFAULT_CSR[TITLE_1]):
                    self.extracted_data[DEFAULT_CSR] = data
                else:
                    pass
        except:
            log = Log()
            log.insert_log_error()
    
    def __initialize_data(self) -> None:
        self.extracted_data = {
            NAME : BLANK,
            ID_PATIENT : BLANK,
            BIRTH_DAY : BLANK,
            STREET : BLANK,
            HEIGH : BLANK,
            WEIGHT : BLANK,
            CP_CITY : BLANK,
            PHONE : BLANK,
            BMI : BLANK,
            REGISTRY_EVAL_DATE : BLANK,
            REGISTRY_EVAL_START_TIME : [],  # [0] = Registry and [1] = Evaluation
            REGISTRY_EVAL_END_TIME : [],    # [0] = Registry and [1] = Evaluation
            REGISTRY_EVAL_DURATION: [],     # [0] = Registry and [1] = Evaluation
            IAH : BLANK,
            AVERAGE_RPM : BLANK,
            IR : BLANK,
            RESPIRATIONS : BLANK,
            APNEA_INDEX : BLANK,
            APNEAS : BLANK,
            IAI : BLANK,
            INDETERMINATED_APNEAS  : BLANK,
            IAO : BLANK,
            OBSTRUCTIVE_APNEAS : BLANK,
            IAC : BLANK,
            CENTRAL_APNEAS : BLANK,
            IAM : BLANK,
            MIXED_APNEAS : BLANK,
            HYPOAPNEA_INDEX : BLANK,
            HYPOAPNEA : BLANK,
            LF_P : BLANK,
            LF : BLANK,
            LR_P : BLANK,
            LR : BLANK,
            SNORING_EVENTS : BLANK,
            IDO : BLANK,
            DESATURATIONS_COUNT : BLANK,
            AVERAGE_SATURATION : BLANK,
            SATURATION_90 : BLANK,
            MINOR_SATURATION : BLANK,
            SATURATION_85 : BLANK,
            LOWEST_SATURATION : BLANK,
            SATURATION_80 : BLANK,
            BASAL_SATURATION : BLANK,
            MINIMUM_PULSE_RATE : BLANK,
            MAXIMUM_PULSE_RATE : BLANK,
            AVERAGE_PULSE_RATE : BLANK,
            CSR : BLANK,
            DEFAULT_APNEA : BLANK,
            DEFAULT_HYPOAPNEA : BLANK,
            DEFAULT_SNORING : BLANK,
            DEFAULT_DESATURATION : BLANK,
            DEFAULT_CSR : BLANK,
            COMMENTS : BLANK,
            EVALUATION_DURATION : BLANK
        }
