from datetime import date
import json

NO_ID = -1
NO_AGE = -1
MALE = 0
FEMALE = 1
ZERO = 0
BLANK = ""


class Patient:
    def __init__(self):
        self.nss = BLANK
        self.doctor_id = NO_ID
        self.acronym = BLANK
        self.age = NO_AGE
        self.apnea_study = ApneaStudy()
        self.status = ZERO
        self.registration_date = BLANK
        self.birth_date = BLANK
        self.medical_record = MedicalRecord()
        # self.report = Report()

    def set_patient_data(self, data):
        print("Patient:", data)
        self.nss = data[0]
        self.doctor_id = data[1]
        self.acronym = data[2]
        self.birth_date = data[3]
        self.sex = int(data[4])
        self.registration_date = data[5]

    def set_doctor(self, doctor_id):
        self.doctor_id = doctor_id

    def print_patient_data(self):
        print("Patient ID", self.nss)
        print("Patient doctor ID", self.doctor_id)
        print("Patient Acronym", self.acronym)
        print("Patinet Apnea Study ID", self.apnea_study.id)
        print("Patinet Status", self.status)
        print("Patinet Registration Date", self.registration_date)

    def calculate_age(self, born):
        today = date.today()
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


class ApneaStudy:
    def __init__(self):
        self.id = BLANK
        self.patient_id = BLANK
        self.result = BLANK
        self.status = BLANK
        self.creation_date = BLANK
        self.front_photo = Picture()
        self.lateral_photo = Picture()
        self.report = Report()
        # Change
        self.video = Video()
        self.edf = Osa()

    def set_apnea_study(self, data):
        print("Apnea Study:", data)
        self.id = data[0]
        self.patient_id = data[1]
        self.result = data[2]
        self.status = data[3]
        self.creation_date = data[4]

    def print_apnea_study_data(self):
        print("----- APNEA STUDY -------")
        print("Apnea Study ID:", self.id)
        print("Patient ID:", self.patient_id)
        print("Results:", self.result)
        print("Registration Date:", self.creation_date)
        print("Status:", self.status)


class Picture:
    def __init__(self):
        self.id = BLANK

    def set_picture(self, data):
        self.id = data[0]
        self.apnea_id = data[1]
        self.path = data[2]
        self.picture_json = json.loads(json.loads(data[3]))
        # self.picture_json = pd.read_json(data[2])
        self.tag = data[4]
        # self.measures = json.loads(data[5])

    def print_picture_data(self):
        print("----- PICTURE -------")
        print("Picture ID:", self.id)
        print("Apnea Study ID:", self.apnea_id)
        print("JSON:", self.picture_json)
        print("Path:", self.path)
        print("Tag:", self.tag)
        # print("Measures:", self.measures)


class Video:
    def __init__(self):
        self.id = BLANK

    def set_video(self, data):
        self.id = data[0]
        self.apnea_id = data[1]
        self.path = data[2]

    def print_video_data(self):
        print("----- VIDEO -----")
        print("Video ID:", self.id)
        print("Apnea Study ID:", self.apnea_id)
        print("Video Path:", self.path)


class Osa:
    def __init__(self):
        self.id = BLANK

    def set_edf(self, data):
        self.id = data[0]
        self.apnea_id = data[1]
        self.path = data[2]

    def print(self):
        print("----- MEDICAL RECORD -------")
        print("OSA ID:", self.id)
        print("Apnea ID:", self.apnea_id)
        print("Path file:", self.path)


class MedicalRecord:
    def __init__(self):
        self.id = BLANK
        self.vital_sign = VitalSigns()
        self.metrics = Metrics()
        self.comorbility = Comorbility()
        self.history = History()
        self.aux_diagnostics = AuxiliaryDiagnostic()

    def set_medical_record(self, data):
        self.id = data[0]
        self.id_apnea_study = data[1]
        self.metrics.id = data[2]
        self.vital_sign.id = data[3]
        self.history.id = data[4]
        self.comorbility.id = data[5]
        self.aux_diagnostics.id = data[6]

    def print_medical_record_data(self):
        print("----- MEDICAL RECORD -------")
        print("Medical Record ID:", self.id)
        print("Vital Signs ID:", self.vital_sign.id)
        print("Metrics ID:", self.metrics.id)
        print("Comorbilidad Charlson ID:", self.comorbility.id)
        print("History ID:", self.history.id)
        print("Auxiliary Diagnostic ID:", self.aux_diagnostics.id)


class VitalSigns:
    def __init__(self):
        self.id = BLANK

    def set_vital_sings(self, data):
        self.id = data[0]
        self.cardiac_frequency = int(data[1])
        self.arterial_tension_high = int(data[2])
        self.arterial_tension_low = int(data[3])
        self.respiratory_frequency = int(data[4])
        self.oxigen_saturation = int(data[5])
        self.temperature = int(data[6])

    def print(self):
        print("----- VITAL SIGNS -------")
        print("Vital Signs ID: ", self.id)
        print("Caridiac Frequency (FC):", self.cardiac_frequency)
        print("Low Arterial Tension:", self.arterial_tension_low)
        print("High Arterial Tension:", self.arterial_tension_high)
        print("Respiratory Frequency:", self.respiratory_frequency)
        print("Oxigen Saturation:", self.oxigen_saturation)
        print("Temperature:", self.temperature)


class Metrics:
    def __init__(self):
        self.id = BLANK

    def set_metrics(self, data):
        self.id = data[0]
        self.height = float(data[1])
        self.weight = float(data[2])
        self.neck_circumference = float(data[3])

    def print(self):
        print("----- METRICS -------")
        print("Metrics ID:", self.id)
        print("Height:", self.height)
        print("Weight:", self.weight)
        print("Neck Circumference:", self.neck_circumference)


class Comorbility:
    def __init__(self):
        self.id = BLANK

    def set_comorbility(self, data):
        self.id = data[0]
        self.cardiac_insuficiency = int(data[1])
        self.antecedente_cerebro_vascular = int(data[2])
        self.enfermedad_vascular_periferica = int(data[3])
        self.demencia = int(data[4])
        self.epoc = int(data[5])
        self.enfermedad_tejido_conectivo = int(data[6])
        self.liver_disease = int(data[7])
        self.diabetes_mellitus = int(data[8])
        self.hemiplejia = int(data[9])
        self.afeccion_renal = int(data[10])
        self.tumor_solido = int(data[11])
        self.leucemia = int(data[12])
        self.linfoma = int(data[13])
        self.vih = int(data[14])

    def print_comorbility_data(self):
        print("------- CHARLSON CORMOBODITY -------")
        print("Charlson Cormobidity ID:", self.id)
        print("Cardiac Insuficiency:", self.cardiac_insuficiency)
        print("historyc cerebral vascular accident:",
              self.antecedente_cerebro_vascular)
        print("peripherial vascular disease:",
              self.enfermedad_vascular_periferica)
        print("dementia:", self.demencia)
        print("chronic obstructive pulmonary disease:", self.epoc)
        print("connective tissue disease:", self.enfermedad_tejido_conectivo)
        print("liver disease", self.liver_disease)
        print("diabetes militus:", self.diabetes_mellitus)
        print("hemiplegia:", self.hemiplejia)
        print("renal disease:", self.afeccion_renal)
        print("solid tumor:", self.tumor_solido)
        print("leukemia:", self.leucemia)
        print("lymphoma:", self.linfoma)
        print("human_immunodeficiency_virus:", self.vih)


class History:
    def __init__(self):
        self.id = BLANK

    def set_history(self, data):
        self.id = data[0]
        self.oxigen_use = int(data[1])
        self.smoker = int(data[2])
        self.ex_smoker = int(data[3])
        self.snoring = int(data[4])
        self.witnessed_apneas = int(data[5])
        self.chronic_fatigue = int(data[6])
        self.hypertension = int(data[7])
        self.medicines = data[8]

    def print_history_data(self):
        print("----- HISTORY -------")
        print("History ID:", self.id)
        print("Use of Oxigen:", self.oxigen_use)
        print("Smoker :", self.smoker)
        print("Ex smoker:", self.ex_smoker)
        print("Snoring:", self.snoring)
        print("Presented Apneas :", self.witnessed_apneas)
        print("Cronic Fatigue:", self.chronic_fatigue)
        print("Hipertension :", self.hypertension)
        print("Meds:", self.medicines)


class AuxiliaryDiagnostic:
    def __init__(self):
        self.id = BLANK

    def set_auxiliary_diagnostic(self, data):
        self.id = data[0]
        try:
            self.escala_epworth = int(data[1])
            self.etco2 = int(data[2])
            self.escala_mallampati = int(data[3])
        except (TypeError):
            self.escala_epworth = ZERO
            self.etco2 = ZERO
            self.escala_mallampati = ZERO

        try:
            self.pH = float(data[4])
            self.pco2 = int(data[5])
            self.po2 = int(data[6])
            self.eb = int(data[7])
        except (TypeError):
            self.pH = ZERO
            self.pco2 = ZERO
            self.po2 = ZERO
            self.eb = ZERO
        try:
            self.fvc_litros = int(data[8])
            self.fvc = int(data[9])
            self.fev1_litros = int(data[10])
            self.fev1 = int(data[11])
        except (TypeError):
            self.fvc_litros = ZERO
            self.fvc = ZERO
            self.fev1_litros = ZERO
            self.fev1 = ZERO

    def print_auxiliary_diagnostic(self):
        print("----- AUXILIAR DIAGNOSTIC -------")
        print("Auxiliar Diagnostic ID:", self.id)
        print("Escala Epwroth:", self.escala_epworth)
        print("etco2 :", self.etco2)
        print("pH:", self.pH)
        print("pco2:", self.pco2)
        print("po2:", self.po2)
        print("EB:", self.eb)
        print("fvc_litros:", self.fvc_litros)
        print("fvc:", self.fvc)
        print("fev1_litros:", self.fev1_litros)
        print("fev1:", self.fev1)


class Report:
    def __init__(self):
        self.id = BLANK

    def set_report(self, data):
        self.id = data[0]
        self.id_apnea_study = data[1]
        self.iah = data[2]
        self.rpm = data[3]
        self.ir = data[4]
        self.respirations = data[5]
        self.apneas_index = data[6]
        self.apneas = data[7]
        self.iai = data[8]
        self.indeterminated_apneas = data[9]
        self.iao = data[10]
        self.obstructive_apneas = data[11]
        self.iac = data[12]
        self.central_apneas = data[13]
        self.iam = data[14]
        self.mixed_apneas = data[15]
        self.hypopnea_index = data[16]
        self.hypoapneas = data[17]
        self.lf_percentage = data[18]
        self.lf = data[19]
        self.lr_percentage = data[20]
        self.lr = data[21]
        self.snoring_events = data[22]
        self.ido = data[23]
        self.desaturations_number = data[24]
        self.average_saturation = data[25]
        self.saturation_90_min = data[26]
        self.saturation_90_per = data[27]
        self.minor_desaturation = data[28]
        self.saturation_85_min = data[29]
        self.saturation_85_per = data[30]
        self.lowest_saturation = data[31]
        self.saturation_80_min = data[32]
        self.saturation_80_per = data[33]
        self.basal_saturation = data[34]
        self.minimum_pulse_rate = data[35]
        self.maximum_pulse_rate = data[36]
        self.average_pulse_rate = data[37]
        self.csr = data[38]
        self.scan_status = data[39]
        self.default_apnea = data[40]
        self.default_hypopnea = data[41]
        self.default_snoring = data[42]
        self.default_desaturation = data[43]
        self.default_csr = data[44]
        self.comments = data[45]
        self.evaluation_duration = data[45]

    def print(self):
        print("----- REPORT -------")
        print("id:", self.id)
        print("id_apnea_study:", self.id_apnea_study)
        print("iah:", self.iah)
        print("RPM:", self.rpm)
        print("ir:", self.ir)
        print("respirations:", self.respirations)
        print("apneas_index:", self.apneas_index)
        print("apneas:", self.apneas)
        print("iai:", self.iai)
        print("indeterminated_apneas:", self.indeterminated_apneas)
        print("iao:", self.iao)
        print("obstructive_apneas:", self.obstructive_apneas)
        print("iac:", self.iac)
        print("central_apneas:", self.central_apneas)
        print("iam:", self.iam)
        print("mixed_apneas:", self.mixed_apneas)
        print("hypopnea_index:", self.hypopnea_index)
        print("hypoapneas:", self.hypoapneas)
        print("lf_percentage:", self.lf_percentage)
        print("lf:", self.lf)
        print("lr_percentage:", self.lr_percentage)
        print("lr:", self.lr)
        print("snoring_events:", self.snoring_events)
        print("ido:", self.ido)
        print("desaturations_number:", self.desaturations_number)
        print("average_saturation:", self.average_saturation)
        print("saturation_90_min:", self.saturation_90_min)
        print("saturation_90_per:", self.saturation_90_per)
        print("minor_desaturation:", self.minor_desaturation)
        print("saturation_85_min:", self.saturation_85_min)
        print("saturation_85_per:", self.saturation_85_per)
        print("lowest_saturation:", self.lowest_saturation)
        print("saturation_80_min:", self.saturation_80_min)
        print("saturation_80_per:", self.saturation_80_per)
        print("basal_saturation:", self.basal_saturation)
        print("minimum_pulse_rate:", self.minimum_pulse_rate)
        print("maximum_pulse_rate:", self.maximum_pulse_rate)
        print("average_pulse_rate:", self.average_pulse_rate)
        print("csr:", self.csr)
        print("scan_status:", self.scan_status)
        print("default_apnea:", self.default_apnea)
        print("default_hypopnea:", self.default_hypopnea)
        print("default_snoring:", self.default_snoring)
        print("default_desaturation:", self.default_desaturation)
        print("default_csr:", self.default_csr)
        print("comments:", self.comments)
        print("evaluation_duration:", self.evaluation_duration)
