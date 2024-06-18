import mysql.connector
import pymongo
from threading import Thread

from log import Log

MULTIMEDIA_DB_CLIENT = "mongodb://localhost:27017/"
MULTIMEDIA_DB_NAME = "inSAsy"
PHOTO_FRONT_COLLECTION = "photo_front"
PHOTO_LATERAL_COLLECTION = "photo_lateral"
VIDEO_COLLECTION = "video"
AUDIO_COLLECTION = "audio"
PDF_COLLECTION = "pdf"
OSA_COLLECTION = "osa"

PHOTO_PATH_INDEX = 0
PHOTO_COORDINATES_INDEX = 1
PHOTO_TAG_INDEX = 2

VIDEO_PATH_INDEX = 0

OSA_PATH_INDEX = 0

THREAD_STARTED_EVENT = "Thread started with ID: "

INITIAL_DB_CONNECTION_STATUS = False
DB_CONNECTION_SUCCESFUL = True
DB_CONNECTION_FAILED = False


class ControllDb:
    def __init__(self, host="localhost", port=3306, user="admin", db="mydb", password="admin"):
        self.host = host
        self.port = port
        self.user = user
        self.database_name = db
        self.password = password
        self.isConnected = False
        
        try:
            self.connection = mysql.connector.connect(
                                host=self.host, 
                                port=self.port, 
                                user = self.user, 
                                password=self.password, 
                                database = self.database_name
                                )
            
            self.cursor = self.connection.cursor(buffered=True)
            self.isConnected = True
        except:
            #TO DO: Pop-up window or text in UI
            self.isConnected = False
            log = Log()
            log.insert_log_error()
            
    # query for LogIn validation
    def selectUserId(self, username):
        query = ("SELECT id_system_user, password FROM system_user WHERE username = %(user)s")
        self.cursor.execute(query, {'user': str(username)})
        return self.cursor.fetchone()
    
    def get_username(self, username) -> tuple:
        query = ("SELECT username FROM system_user WHERE username = %(user)s")
        self.cursor.execute(query, {"user": str(username)})
        return self.cursor.fetchone()

    # query that retrieve the log in user full name
    def getDoctorName(self, id):
        query = ("SELECT first_name, last_name FROM system_user WHERE id_system_user = %(id)s")
        self.cursor.execute(query, {'id': str(id)})
        return self.cursor.fetchone()

    # query that retrieve all attributes from system_user table of one user
    def selectUserInformation(self, id):
        query = ("SELECT id_system_user, username, first_name, last_name password FROM system_user WHERE id_system_user = %(id)s")
        self.cursor.execute(query, {'id': int(id)})
        return self.cursor.fetchone()

    # query that displays the patient information on the search table
    def selectPacientSearchData(self):
        query = "SELECT id_system_user, patient.id_patient, patient.acronym, birthdate, apnea_study.id_apnea_study, patient.registry_date "
        query += "FROM patient INNER JOIN apnea_study ON patient.id_patient = apnea_study.id_patient"
        self.cursor.execute(query)        
        return self.cursor.fetchall()
    
    def select_all_patients(self):
        query = "SELECT id_system_user, id_patient, acronym, birthdate, registry_date FROM patient ORDER BY registry_date ASC"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # query SELECT * FROM patient
    def select_all_from_patients(self):
        query = "SELECT * FROM patient ORDER BY registry_date ASC"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # query that retrieve all the apnea studies id and their dates of one patient
    def select_patient_id_date_apena_studies(self, patient_id):
        query = "SELECT id_apnea_study, study_date FROM mydb.apnea_study WHERE id_patient = %(patient_id)s ORDER BY study_date ASC"
        self.cursor.execute(query, {'patient_id': patient_id})
        return self.cursor.fetchall()
    
    # query that displays all the patient apnea stydies on the studies table
    def select_patient_apena_studies(self, patient_id):
        query = "SELECT id_apnea_study, status, study_date FROM mydb.apnea_study WHERE id_patient = %(patient_id)s ORDER BY study_date ASC"
        self.cursor.execute(query, {'patient_id': patient_id})
        return self.cursor.fetchall()

    # query that retrieve all attributes from patient table of one patient
    def selectAllFromPatient(self, patient_id):
        query = ("SELECT * FROM mydb.patient WHERE id_patient = %(patient_id)s")
        self.cursor.execute(query, {'patient_id': patient_id})
        return self.cursor.fetchone()
    
    # query that validates if the NSS already exist or not
    def validate_existing_nss(self, patient_id):
        # print(patient_id)
        query = ("SELECT id_patient FROM mydb.patient WHERE id_patient = %(patient_id)s")
        self.cursor.execute(query, {'patient_id': patient_id})
        # None type means there is not a PK with that NSS at patient table
        if self.cursor.fetchone() == None:
            # print("NSS don't exists")
            return False
        else:
            # print("NSS already exists")
            return True
        
    # query that verify if exist osa file of one study
    def status_osa_file(self, apnea_study_id: int) -> bool:
        query = ("SELECT id_osa FROM mydb.osa WHERE id_apnea_study = %(apnea_study_id)s")
        self.cursor.execute(query, {"apnea_study_id" : apnea_study_id})
        status = False
        if self.cursor.fetchone() == None:
            # No osa asociated to that apnea_study_id
            status = False
        else:
            # apnea study with osa file
            status = True
        
        return status
        
    # query that verify if exist pdf file of one study
    def status_pdf_file(self, apnea_study_id: int) -> bool:
        query = ("SELECT id_pdf FROM mydb.pdf WHERE id_apnea_study = %(apnea_study_id)s")
        self.cursor.execute(query, {"apnea_study_id" : apnea_study_id})
        status = False
        if self.cursor.fetchone() == None:
            # No pdf asociated to that apnea_study_id
            status = False
        else:
            # apnea study with pdf file
            status = True
        
        return status
    
    # query that verify if exist video of one study
    def status_video_file(self, apnea_study_id: int) -> bool:
        query = ("SELECT id_video FROM mydb.video WHERE id_apnea_study = %(apnea_study_id)s")
        self.cursor.execute(query, {"apnea_study_id" : apnea_study_id})
        status = False
        if self.cursor.fetchone() == None:
            # No video asociated to that apnea_study_id
            status = False
        else:
            # apnea study with video file
            status = True
        
        return status

    # query that retrive all attributes from medical_record table of one patient
    def selectAllFromMedicalRecord(self, apnea_study_id):
        query = ("SELECT * FROM mydb.medical_record WHERE id_apnea_study = %(apnea_study_id)s")
        self.cursor.execute(query, {'apnea_study_id': apnea_study_id})
        return self.cursor.fetchone()
    
    # query that retrive all attributes from metrics table of one patient
    def selectAllFromMetrics(self, metrics_id):
        query = ("SELECT * FROM mydb.metrics WHERE id_metrics = %(metrics_id)s")
        self.cursor.execute(query, {'metrics_id': metrics_id})
        return self.cursor.fetchone()
    
    # query that retrive all attributes from vital_signs table of one patient
    def selectAllFromVitalSigns(self, vital_signs_id):
        query = ("SELECT * FROM mydb.vital_signs WHERE id_vital_signs = %(vital_signs_id)s")
        self.cursor.execute(query, {'vital_signs_id': vital_signs_id})
        return self.cursor.fetchone()
    
    # query that retrive all attributes from record table of one patient
    def selectAllFromHistory(self, record_id):
        query = ("SELECT * FROM mydb.record WHERE id_record = %(record_id)s")
        self.cursor.execute(query, {'record_id': record_id})
        return self.cursor.fetchone()

    # query that retrive all attributes from charlson_comorbidity table of one patient
    def selectAllFromCharlsonComorbidity(self, comorbility_id):
        query = ("SELECT * FROM mydb.charlson_comorbidity WHERE id_charlson_comorbidity = %(comorbility_id)s")
        self.cursor.execute(query, {'comorbility_id': comorbility_id})
        return self.cursor.fetchone()
    
    # query that retrive all attributes from diagnostic_aids table of one patient
    def selectAllFromAuxDiagnostic(self, diagnostic_aids_id):
        query = ("SELECT * FROM mydb.diagnostic_aids WHERE id_diagnostic_aids = %(diagnostic_aids_id)s")
        self.cursor.execute(query, {'diagnostic_aids_id': diagnostic_aids_id})
        return self.cursor.fetchone()

    # query that retrive all attributes from apnea_study table of one patient
    def selectAllApneaStudy(self, apnea_study_id):
        query = ("SELECT * FROM mydb.apnea_study WHERE id_apnea_study = %(apnea_study_id)s")
        self.cursor.execute(query, {'apnea_study_id': apnea_study_id})
        return self.cursor.fetchone()

    # query that retrive all attributes from image table of one patient
    def selectAllPicture(self, apnea_id):
        # print("Apnea ID:", apnea_id)
        query = ("SELECT * FROM mydb.image WHERE id_apnea_study = %(apnea_id)s")
        self.cursor.execute(query, {'apnea_id': apnea_id})
        # ------- Wierd print ----------
        # print(self.cursor.fetchone())
        return self.cursor.fetchone()
    
    # query that retrieve all patient images of one apnea study for excel export data
    def select_all_study_images(self, apnea_id):
        query = ("SELECT image, path, tag FROM mydb.image WHERE id_apnea_study = %(apnea_id)s")
        self.cursor.execute(query, {'apnea_id': apnea_id})
        return self.cursor.fetchall()
    
    # query that retrive all attributes from pfd table of one patient
    def selectAllReport(self, apnea_id):
        query = ("SELECT * FROM mydb.pdf WHERE id_apnea_study = %(apnea_id)s")
        self.cursor.execute(query, {'apnea_id' : apnea_id})
        return self.cursor.fetchone()
    
    # query that retrive all attributes from pdf table of one patient
    def pdf_to_excel(self, apnea_id):
        query = "SELECT iah, rmp, apneas_index, csr, apneas, iai, indeterminated_apneas, iao, obstructive_apneas, iac, central_apnea, iam, mixed_apneas, hypopnea_index, lr, snoring_events, desaturations_number, saturation_90_min, saturation_90_per, minior_desaturation, saturation_85_min, saturation_80_per, maximum_pulse_rate, avarage_pulse_rate, flow_evaluation_period FROM mydb.pdf WHERE id_apnea_study = %(apnea_id)s"
        self.cursor.execute(query, {'apnea_id' : apnea_id})
        return self.cursor.fetchone()
    
    # query that retrive the tags of one patient image
    def selectTagPicture(self, apnea_id, tag):
        query = ("SELECT * FROM mydb.image WHERE id_apnea_study = %s and tag = %s")
        values  = (apnea_id, tag)
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    # query that retrive all attributes from video table of one patient
    def select_all_video(self, apnea_id):
        # print("Video Apnea ID:", apnea_id)
        query = ("SELECT * FROM mydb.video WHERE id_apnea_study = %(apnea_id)s")
        self.cursor.execute(query, {"apnea_id": apnea_id})
        return self.cursor.fetchone()
    
    # query that retrive all attributes from osa table of one patient
    def select_edf_file(self, apnea_id):
        # print("Edf file ID:", apnea_id)
        query = "(SELECT * FROM mydb.osa WHERE id_apnea_study = %(apnea_id)s)"
        self.cursor.execute(query, {"apnea_id" : apnea_id})
        return self.cursor.fetchone()
    
    # query that retrieve an image path and it's tag from the asociated id_apnea
    def select_image_path(self, apnea_id: int) -> list:
        query = ("SELECT path, tag FROM mydb.image WHERE id_apnea_study = %(apnea_id)s")
        self.cursor.execute(query, {"apnea_id" : apnea_id})
        return self.cursor.fetchall()
    
    # query that retrieve a video path from the asociated id_apnea
    def select_video_path(self, apnea_id: int) -> tuple:
        query = ("SELECT video_path FROM mydb.video WHERE id_apnea_study = %(apnea_id)s")
        self.cursor.execute(query, {"apnea_id" : apnea_id})
        return self.cursor.fetchone()
    
    # query that retrieve an osa path from the asociated id_apnea
    def select_osa_path(self, apnea_id: int) -> tuple:
        query = ("SELECT osa_path FROM mydb.osa WHERE id_apnea_study = %(apnea_id)s")
        self.cursor.execute(query, {"apnea_id" : apnea_id})
        return self.cursor.fetchone()
    
    # query that retrieve all the patients id's
    def select_all_id_patients(self) -> list:
        query = ("SELECT id_patient FROM mydb.patient")
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # query that retrieve all the apnea studies from the asociated id_patient
    def select_all_id_apnea_studies(self, id_patient: int) -> list:
        query = ("SELECT id_apnea_study FROM mydb.apnea_study WHERE id_patient = %(id_patient)s")
        self.cursor.execute(query, {"id_patient" : id_patient})
        return self.cursor.fetchall()
    
    # query that retrieve the coords of an image asociated to a id_apnea study
    def select_image_coords(self, id_apnea: int) -> list:
        query = ("SELECT image, tag FROM mydb.image WHERE id_apnea_study = %(id_apnea)s")
        self.cursor.execute(query, {"id_apnea" : id_apnea})
        return self.cursor.fetchall()
    
    # --------------- APRIORI FILTER QUERIES ---------------

    def select_data_filtered_distinct_gender(self, tuple_data: tuple) -> list[tuple]:
        query = "SELECT DISTINCT(P.id_patient), id_system_user, acronym, birthdate, sex, registry_date FROM mydb.patient AS P "
        query += "INNER JOIN mydb.apnea_study AS APS "
        query += "ON P.id_patient = APS.id_patient "
        query += "INNER JOIN mydb.medical_record AS MR "
        query += "ON MR.id_apnea_study = APS.id_apnea_study "
        query += "INNER JOIN mydb.metrics AS M "
        query += "ON M.id_metrics = MR.id_metrics "
        query += "INNER JOIN mydb.pdf AS PD "
        query += "ON APS.id_apnea_study = PD.id_apnea_study "
        query += "WHERE P.sex = %s "
        query += "AND PD.iah BETWEEN %s AND %s "
        query += "AND DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(), P.birthdate)), '%Y') + 0 BETWEEN %s AND %s "
        query += "AND M.weight BETWEEN %s AND %s "
        query += "ORDER BY P.registry_date ASC;"
        self.cursor.execute(query, tuple_data)
        
        return self.cursor.fetchall()
    
    def select_data_filtered_undistinct_gender(self, tuple_data: tuple) -> list[tuple]:
        query = "SELECT DISTINCT(P.id_patient), id_system_user, acronym, birthdate, sex, registry_date FROM mydb.patient AS P "
        query += "INNER JOIN mydb.apnea_study AS APS "
        query += "ON P.id_patient = APS.id_patient "
        query += "INNER JOIN mydb.medical_record AS MR "
        query += "ON MR.id_apnea_study = APS.id_apnea_study "
        query += "INNER JOIN mydb.metrics AS M "
        query += "ON M.id_metrics = MR.id_metrics "
        query += "INNER JOIN mydb.pdf AS PD "
        query += "ON APS.id_apnea_study = PD.id_apnea_study "
        query += "WHERE PD.iah BETWEEN %s AND %s "
        query += "AND DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(), P.birthdate)), '%Y') + 0 BETWEEN %s AND %s "
        query += "AND M.weight BETWEEN %s AND %s "
        query += "ORDER BY P.registry_date ASC;"
        self.cursor.execute(query, tuple_data)
        
        return self.cursor.fetchall()
    
    # --------------------------------------------------
    # INSERTS
    # --------------------------------------------------

    def insert_new_system_user(self, tuple_data: tuple) -> None:
        # print(tuple_data)
        query = ("INSERT INTO mydb.system_user (username, password, first_name, last_name, type_user) VALUES ('%s', '%s', '%s', '%s', %s)" %tuple_data)
        # query += "VALUES ('%s', %s, '%s', '%s', %s)" %tuple_data
        # query = "INSERT INTO mydb.system_user VALUES ('%s', '%s', '%s', '%s', %d)" %tuple_data
        self.cursor.execute(query)
        self.connection.commit()

    # query that add a new patient
    def insertIntoPatient(self, tuple_data):
        # print(tuple_data)
        query = "INSERT INTO mydb.patient VALUES ('%s', %s, '%s', '%s', %s, '%s')" %tuple_data
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    # query that add new patient medical record
    def insertIntoMedicalRecord(self, tuple_data):
        # print(tuple_data)
        query = "INSERT INTO mydb.medical_record (id_apnea_study, id_metrics, id_vital_signs, id_record, "
        query += "id_charlson_comorbidity, id_diagnostic_aids) VALUES (%d, %d, %d, %d, %d, %d)" %tuple_data
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    # query that add new patient metrics
    def insertIntoMetrics(self, tuple_data):
        # print(tuple_data)
        query = "INSERT INTO mydb.metrics (height, weight, neck_circumference) VALUES (%s, %s, %s)" %tuple_data
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    # query that add new patient vital signs
    def insertIntoVitalSigns(self, tuple_data):
        # print(tuple_data)
        query = "INSERT INTO mydb.vital_signs (heart_rate, systolic_blood_pressure, diastolic_blood_pressure,"
        query += "respiratory_rate, oxigen_saturation, temperature) VALUES (%d, %d, %d, %d, %d, %d)" %tuple_data
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    # query that add new patient record
    def insertIntoHistory(self, tuple_data):
        # print(tuple_data)
        query = "INSERT INTO mydb.record (oxigen_use, smoker, exsomker, snoring, witnessed_apneas,"
        query += "chronic_fatigue, hypertension, medicines) VALUES (%s, %s, %s, %s, %s, %s, %s, '%s')" %tuple_data
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    # query that add new patient charlson comorbidity test values
    def insertIntoCharlsonComorbidity(self, tuple_data):
        # print(tuple_data)
        query = "INSERT INTO mydb.charlson_comorbidity (cardiac_insufficiency, historyc_cerebral_vascular_accident, peripherial_vascular_disease, "
        query += "dementia, chronic_obstructive_pulmonary_disease, connective_tissue_disease, liver_disease, diabetes_militus, hemiplegia, renal_disease, solid_tumor,"
        query += "leukemia, lymphoma, human_immunodeficiency_virus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" %tuple_data
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    # query that add new patient diagnostic aids values
    def insertIntoDiagnostiAux(self, tuple_data):
        # print(tuple_data)
        query = "INSERT INTO mydb.diagnostic_aids (scale_epworth, etco2, scale_mallampati, ph, pco2, po2, eb, fvc_litros, fvc, fev1_litros, fev1)"
        query += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" %tuple_data
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    # query that add new patient apnea study
    def insertApneaStudy(self, tuple_data):
        query = ("INSERT INTO mydb.apnea_study (id_patient, status, study_date) VALUES ('%s', %s, '%s')" %tuple_data)
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    # query that add new patient image
    def insertPicture(self, tuple_data):
        query = ("INSERT INTO mydb.image (id_apnea_study, image, path, tag) VALUES (%s, %s, '%s', %s)" %tuple_data)
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    # query that add new patient video
    def insert_video(self, tuple_data):
        query = ("INSERT INTO mydb.video (id_apnea_study, video_path) VALUES (%s, '%s')" %tuple_data)
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    # query that add new patient JSON image data
    def insertJson(self, id_pic, json):
        query = ("INSERT INTO mydb.image WHERE id_image =  (image) VALUES (%d)")
        record = (id_pic, json)
        self.cursor.execute(query, record)
        self.connection.commit()
    
    # query that add new patient pdf study data
    def insertReport(self, tuple_data):
        # print(tuple_data)
        query = "INSERT INTO mydb.pdf (id_apnea_study, iah, rmp, ir, respirations, "
        query += "apneas_index, csr, apneas, iai, indeterminated_apneas, iao, obstructive_apneas, "
        query += "iac, central_apnea, iam, mixed_apneas, hypopnea_index, hypoapneas, lf_percentage, "
        query += "lf, lr_percentage, lr, snoring_events, ido, desaturations_number, avarage_saturation, "
        query += "saturation_90_min, saturation_90_per, minior_desaturation, saturation_85_min, saturation_85_per, "
        query += "lowest_saturation, saturation_80_min, saturation_80_per, basal_saturation, minimum_pulse_rate, "
        query += "maximum_pulse_rate, avarage_pulse_rate, default_apnea, default_hypopnea, default_snoring, "
        query += "default_desaturation, default_csr, comments, flow_evaluation_period) VALUES "
        query += "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # query += "defaultDesaturation, defaultCSR, comments) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', "
        # query += "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', "
        # query += "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %tupleData
        # self.cursor.execute(query)
        self.cursor.execute(query, tuple_data)
        self.connection.commit()
    
    # query that add new patient osa file
    def insert_edf_file(self, tuple_data):
        # print("Insert OSA", tuple_data)
        query = ("INSERT INTO mydb.osa (id_apnea_study, osa_path) VALUES (%s, '%s')" %tuple_data)
        self.cursor.execute(query)
        self.connection.commit()
        
    # --------------------------------------------------
    # UPDATES
    # --------------------------------------------------
    
    # query that update the patient information
    def updatePatient(self, tuple_data):
        # print(tuple_data)
        query = "UPDATE mydb.patient SET acronym = %s, birthdate = %s, "
        query += "sex = %s, registry_date = %s WHERE id_patient = %s"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()

    # query that update the patient metrics
    def updateMetrics(self, tuple_data):
        # print(tuple_data)
        query = "UPDATE mydb.metrics SET height = %s, weight = %s, neck_circumference = %s "
        query += "WHERE id_metrics = %s"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()

    # query that update the patient vital signs
    def updateVitalSigns(self, tuple_data):
        # print(tuple_data)
        query = "UPDATE mydb.vital_signs SET heart_rate = %s, systolic_blood_pressure = %s, diastolic_blood_pressure = %s, respiratory_rate = %s, "
        query += "oxigen_saturation = %s, temperature = %s WHERE id_vital_signs = %s"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()

    # query that update the patient record
    def updateHistory(self, tuple_data):
        # print(tuple_data)
        query = "UPDATE mydb.record SET oxigen_use = %s, smoker = %s, exsomker = %s, snoring = %s, "
        query += "witnessed_apneas = %s, chronic_fatigue = %s, hypertension = %s, medicines = %s "
        query += "WHERE id_record = %s"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()

    # query that update the patient charlson comorbidity test values
    def updateCharlsonComorbidity(self, tuple_data):
        # print(tuple_data)
        query = "UPDATE mydb.charlson_comorbidity SET cardiac_insufficiency = %s, historyc_cerebral_vascular_accident = %s, "
        query += "peripherial_vascular_disease = %s, dementia = %s, chronic_obstructive_pulmonary_disease = %s, liver_disease = %s, "
        query += "connective_tissue_disease = %s, diabetes_militus = %s, hemiplegia = %s, renal_disease = %s, solid_tumor = %s, leukemia = %s, "
        query += "lymphoma = %s, human_immunodeficiency_virus = %s WHERE id_charlson_comorbidity = %s"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()

    # query that update the patient diagnostic aids values
    def updateDiagnostiAux(self, tuple_data):
        # print(tuple_data)
        query = "UPDATE mydb.diagnostic_aids SET scale_epworth = %s, etco2 = %s, scale_mallampati = %s, "
        query += "ph = %s, pco2 = %s, po2 = %s, eb = %s, fvc_litros = %s, fvc = %s, fev1_litros = %s, fev1 = %s "
        query += "WHERE id_diagnostic_aids = %s"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()

    # query that update the patient image
    def updatePicture(self, tuple_data):
        # print(tuple_data)
        query = "UPDATE mydb.image SET image = %s, path = %s, tag = %s WHERE id_image = %s"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()
    
    # query that update the status of each apnea study
    def updateStatus(self, tuple_data):
        # print(tuple_data)
        query = "UPDATE mydb.apnea_study SET status = %s WHERE id_apnea_study = %s"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()
    
    # query that update the pdf patient study values
    def updateReport(self, tuple_data):
        # print(tuple_data)
        query = " UPDATE mydb.pdf SET iah = %s, rmp = %s, ir = %s, respirations = %s, "
        query += "apneas_index = %s, csr = %s, apneas = %s, iai = %s, indeterminated_apneas = %s, iao = %s, "
        query += "obstructive_apneas = %s, iac = %s, central_apnea = %s, iam = %s, mixed_apneas = %s, "
        query += "hypopnea_index = %s, hypoapneas = %s, lf_percentage = %s, lf = %s, lr_percentage = %s, lr = %s, "
        query += "snoring_events = %s, ido = %s, desaturations_number = %s, avarage_saturation = %s,saturation_90_min = %s, "
        query += "saturation_90_per = %s, minior_desaturation = %s, saturation_85_min = %s, saturation_85_per = %s, "
        query += "lowest_saturation = %s, saturation_80_min = %s, saturation_80_per = %s, basal_saturation = %s, minimum_pulse_rate = %s, "
        query += "maximum_pulse_rate = %s, avarage_pulse_rate = %s, default_apnea = %s, default_hypopnea = %s, "
        query += "default_snoring = %s, default_desaturation = %s, default_csr = %s, comments = %s, flow_evaluation_period = %s WHERE id_pdf = %s"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()
    
    # query that update the patient video
    def update_video(self, tuple_data):
        # print(tuple_data)
        query = "UPDATE mydb.video SET video_path = %s WHERE id_apnea_study = %s"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()
    
    # quety that update the patient osa study
    def update_edf_file(self, tuple_data):
        # print("Update OSA", tuple_data)
        query = "UPDATE mydb.osa SET osa_path = %s WHERE id_apnea_study = %s;"
        self.cursor.execute(query, tuple_data)
        self.connection.commit()


class MultimediaDb:
    def __init__(self) -> None:
        self.is_connected = INITIAL_DB_CONNECTION_STATUS
        try:
            self._my_client = pymongo.MongoClient(MULTIMEDIA_DB_CLIENT)
            self._my_db = self._my_client[MULTIMEDIA_DB_NAME]

            self.is_connected = DB_CONNECTION_SUCCESFUL
        except:
            self.is_connected = DB_CONNECTION_FAILED
            log = Log()
            log.insert_log_error()

    # -------------------------------------------------------------------------
    # -------------------- VERIFY DATABASE CONNECTION -------------------------
    # -------------------------------------------------------------------------
    
    def verify_existing_database(self) -> bool:
        if MULTIMEDIA_DB_NAME in self._my_client.list_database_names():
            # print(MULTIMEDIA_DB_NAME + ": Exist.")
            exist = True
        else:
            exist = False
        
        return exist
    
    # -------------------------------------------------------------------------
    # ---------------------- GET DATA FROM DATABASE ---------------------------
    # -------------------------------------------------------------------------
    
    def get_front_photo_data(self, id_apnea_study: int) -> tuple:
        photo_collection = self._my_db[PHOTO_FRONT_COLLECTION]
        
        get_photo_query = {"id_apnea_study" : id_apnea_study}

        front_photo = photo_collection.find_one(get_photo_query)
        
        try:
            front_photo_tuple = (
                front_photo["_id"],
                front_photo["id_apnea_study"],
                front_photo["path"],
                front_photo["coordinates"],
                front_photo["tag"]
            )
        except:
            front_photo_tuple = None
        
        return front_photo_tuple
    
    def get_lateral_photo_data(self, id_apnea_study: int) -> tuple:
        photo_collection = self._my_db[PHOTO_LATERAL_COLLECTION]
        get_photo_query = {"id_apnea_study" : id_apnea_study}

        lateral_photo = photo_collection.find_one(get_photo_query)
        try:
            lateral_photo_tuple = (
                lateral_photo["_id"],
                lateral_photo["id_apnea_study"],
                lateral_photo["path"],
                lateral_photo["coordinates"],
                lateral_photo["tag"]
            )
        except:
            lateral_photo_tuple = None
        
        return lateral_photo_tuple

    def get_video_data(self, id_apnea_study: int) -> tuple:
        video_collection = self._my_db[VIDEO_COLLECTION]
        get_video_query = {"id_apnea_study" : id_apnea_study}

        video = video_collection.find_one(get_video_query)

        try:
            video_tuple = (
                video["_id"],
                video["id_apnea_study"],
                video["path"]
            )
        except:
            video_tuple = None

        return video_tuple
    
    def get_audio_data(self, id_apnea_study: int) -> tuple:
        audio_collection = self._my_db[AUDIO_COLLECTION]
        get_audio_query = {"id_apnea_study" : id_apnea_study}

        audio = audio_collection.find_one(get_audio_query)

        try:
            audio_tuple = (
                audio["_id"],
                audio["id_apnea_study"],
                audio["path"]
            )
        except:
            audio_tuple = None

        return audio_tuple
    
    def get_osa_data(self, id_apnea_study: int) -> tuple:
        osa_collection = self._my_db[OSA_COLLECTION]
        get_osa_query = {"id_apnea_study" : id_apnea_study}

        osa = osa_collection.find_one(get_osa_query)

        try:
            osa_tuple = (
                osa["_id"],
                osa["id_apnea_study"],
                osa["path"]
            )
        except:
            osa_tuple = None

        return osa_tuple

    # -------------------------------------------------------------------------
    # --------------------- INSERT DATA INTO DATABSE --------------------------
    # -------------------------------------------------------------------------

    def insert_front_photo(self, photo_data: tuple) -> int:
        front_photo_collection = self._my_db[PHOTO_FRONT_COLLECTION]

        new_document = {
            "id_apnea_study" : photo_data[0],
            "path" : photo_data[1],
            "coordinates" : photo_data[2],
            #"measures" : photo_data[3],
            "tag": photo_data[3]
        }

        inserted_document = front_photo_collection.insert_one(new_document)

        return inserted_document.inserted_id
    
    def insert_lateral_photo(self, photo_data: tuple) -> int:
        lateral_photo_collection = self._my_db[PHOTO_LATERAL_COLLECTION]

        new_document = {
            "id_apnea_study" : photo_data[0],
            "path" : photo_data[1],
            "coordinates" : photo_data[2],
            # "measures" : photo_data[3],
            "tag": photo_data[3]
        }

        inserted_document = lateral_photo_collection.insert_one(new_document)

        return inserted_document.inserted_id
    
    def insert_video(self, video_data: tuple) -> int:
        video_collection = self._my_db[VIDEO_COLLECTION]

        new_document = {
            "id_apnea_study" : video_data[0],
            "path" : video_data[1]
        }

        inserted_document = video_collection.insert_one(new_document)
        
        return inserted_document.inserted_id
    
    # insert audio
    
    def insert_osa(self, osa_data: tuple) -> int:
        osa_collection = self._my_db[OSA_COLLECTION]

        new_document = {
            "id_apnea_study" : osa_data[0],
            "path" : osa_data[1]
        }
        inserted_document = osa_collection.insert_one(new_document)

        return inserted_document.inserted_id

    # -------------------------------------------------------------------------
    # --------------------- UPDATE DATA INTO DATABSE --------------------------
    # -------------------------------------------------------------------------

    def update_front_photo(self, apnea_study_id: int, photo_data: tuple) -> None:
        front_photo_collection = self._my_db[PHOTO_FRONT_COLLECTION]

        db_filter = {"id_apnea_study" : apnea_study_id}
        update_value = {"$set": {
            "path" : photo_data[PHOTO_PATH_INDEX],
            "coordinates" : photo_data[PHOTO_COORDINATES_INDEX],
            "tag" : photo_data[PHOTO_TAG_INDEX]
        }}

        front_photo_collection.update_one(db_filter, update_value)

    def update_lateral_photo(self, apnea_study_id: int, photo_data: tuple) -> None:
        lateral_photo_collection = self._my_db[PHOTO_LATERAL_COLLECTION]

        db_filter = {"id_apnea_study" : apnea_study_id}
        update_value = {"$set": {
            "path" : photo_data[PHOTO_PATH_INDEX],
            "coordinates" : photo_data[PHOTO_COORDINATES_INDEX],
            "tag" : photo_data[PHOTO_TAG_INDEX]
        }}

        lateral_photo_collection.update_one(db_filter, update_value)

    def update_video(self, apnea_study_id: int, video_data: tuple) -> None:
        video_collection = self._my_db[VIDEO_COLLECTION]

        db_filter = {"id_apnea_study" : apnea_study_id}
        update_value = {"$set": {
            "path" : video_data[VIDEO_PATH_INDEX]
        }}

        video_collection.update_one(db_filter, update_value)

    # Update Audio

    def update_osa(self, apnea_study_id: int, osa_data: tuple) -> None:
        osa_collection = self._my_db[OSA_COLLECTION]

        db_filter = {"id_apnea_study" : apnea_study_id}
        update_value = {"$set": {
            "path" : osa_data[OSA_PATH_INDEX]
        }}

        osa_collection.update_one(db_filter, update_value)
    # -------------------------------------------------------------------------
    # ---------------------- DELETE DATA OF DATABSE ---------------------------
    # -------------------------------------------------------------------------

    def delete_front_photo(self) -> None:
        front_photo_collection = self._my_db[PHOTO_FRONT_COLLECTION]

        front_photo_collection.delete_many({})
    
    def delete_lateral_photo(self) -> None:
        lateral_photo_collection = self._my_db[PHOTO_LATERAL_COLLECTION]

        lateral_photo_collection.delete_many({})

    def delete_video(self) -> None:
        video_collection = self._my_db[VIDEO_COLLECTION]

        video_collection.delete_many({})

    def delete_audio(self) -> None:
        audio_collection = self._my_db[AUDIO_COLLECTION]

        audio_collection.delete_many({})
    
    def delete_osa(self) -> None:
        osa_collection = self._my_db[OSA_COLLECTION]

        osa_collection.delete_many({})


class DatabaseThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
            
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def insert_connection_result(connection_message):
    log = Log()
    log.insert_log_info(connection_message)

def insert_connection_error():
    log = Log()
    log.insert_log_error()

def insert_db_thread_event(thread_id: int) -> None:
        # print(THREAD_STARTED_EVENT + str(thread_id))
        log = Log()
        log.insert_log_info(THREAD_STARTED_EVENT + str(thread_id))
