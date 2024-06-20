# use mydb schema
USE mydb;
# show all tables
SHOW TABLES;

# ---------------------------------------------
# --------------- SELLECT ALL TABLES ---------------
# ---------------------------------------------

# --------------- SYSTEM USER ---------------
# select all from table: system_user
SELECT * FROM system_user;

# ---------------- PATIENT ------------------
# select all from table: patient
SELECT * FROM patient;

# --------------- MEDICAL RECORD ---------------
# ---------------------------------------------
# select all apneas studies
SELECT * FROM apnea_study;

# --------------- MEDICAL RECORD ---------------
# ---------------------------------------------
# select all FK on table: medical_record
SELECT * FROM medical_record;

# --------------- METRICS ---------------
# select all from table: metrics
SELECT * FROM metrics;
# --------------- VITAL SIGNS ---------------
# select all from table: vital_signs
SELECT * FROM vital_signs;
# --------------- HISTORY ---------------
# select all from table: record
SELECT * FROM record;
# --------------- CHARLSON COMORBIDITY ---------------
# select all from table: charlson_comorbidity
SELECT * FROM charlson_comorbidity;
# --------------- DIAGNOSTIC AIDS ---------------
# select all from table: diagnostic_aids
SELECT * FROM diagnostic_aids;

# --------------- IMAGES ---------------
# select all from table: image
SELECT * FROM image;

# --------------- PDF ---------------
# select all from table: pdf
SELECT * FROM pdf;

# --------------- VIDEO ---------------
# select all from table: video
SELECT * FROM video;

# --------------- OSA ---------------
# select all from table: osa
SELECT * FROM osa;

# --------------- RESULT ---------------
# select all from table: result
SELECT * FROM result;



# --------------- ADD ADMIN USER ---------------
# add new user (ADMIN ONLY)
INSERT INTO system_user (username, password, first_name, last_name, type_user) VALUES ("admin", "admin", "Geravid", "Divgar", 0);
# --------------- DELETE ADMIN USER ---------------
SELECT * FROM system_user;
DELETE FROM system_user WHERE id_system_user = 1;

# --------------- TEST QUERIES ---------------

# Check the type "TINYINT"
# It's not a bool, even when the documentation explains that Workbench change BOOL to TINYINT but its BOOL
# But in real queries, TINYINT insert INTEGER values (signed: -128 to 127 or unsigned: 0 to 255.)
# If you declare TINYINT(2), it can be inserted the same integers as just TINYINT

INSERT INTO record (oxigen_use, smoker, exsomker, snoring, witnessed_apneas, chronic_fatigue, hypertension, medicines) VALUES (0, 10, 6, 5, 4, 3, 128, "No medicines");
SELECT * FROM record;

SELECT id_system_user, id_patient, acronym, birthdate FROM patient;
SELECT * FROM mydb.patient WHERE id_patient = '5168432032321354';

SELECT id_system_user, id_patient, acronym, birthdate, registry_date FROM patient;

SELECT * FROM mydb.medical_record WHERE id_apnea_study = 21;

SELECT * FROM mydb.osa WHERE id_apnea_study = 116;

SELECT * FROM mydb.patient JOIN mydb;

SELECT DISTINCT(id_patient) FROM mydb.apnea_study AS AP JOIN mydb.pdf AS PD WHERE PD.iah BETWEEN 0 AND 10 AND AP.sex = 1;

SELECT DISTINCT(id_patient) FROM mydb.patient AS P JOIN mydb.metrics as M JOIN mydb.pdf AS PD WHERE (PD.iah BETWEEN 10 AND 20) AND (P.sex = 2) AND (M.weight BETWEEN 60 AND 80);

SELECT MAX(weight) AS MaxWeight FROM mydb.metrics;
SELECT MIN(weight) AS MinWeight FROM mydb.metrics;
SELECT AVG(weight) AS AvgWeight FROM mydb.metrics;

SELECT MAX(iah) AS MaxWeight FROM mydb.pdf;

SELECT COUNT(id_patient) AS PatientCount FROM mydb.patient;

SELECT DISTINCT(id_apnea_study) FROM mydb.pdf 
WHERE iah BETWEEN 10 AND 20;

SELECT *, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(), birthdate)), '%Y') + 0 AS age FROM mydb.patient;

SELECT DISTINCT(P.id_patient) FROM mydb.patient AS P
INNER JOIN mydb.apnea_study AS APS
ON P.id_patient = APS.id_patient
INNER JOIN mydb.medical_record AS MR
ON MR.id_apnea_study = APS.id_apnea_study
INNER JOIN mydb.metrics AS M
ON M.id_metrics = MR.id_metrics
INNER JOIN mydb.pdf AS PD
ON APS.id_apnea_study = PD.id_apnea_study
WHERE P.sex = 2
AND PD.iah BETWEEN 0 AND 9
AND DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(), P.birthdate)), '%Y') + 0 BETWEEN 0 AND 50
AND M.weight BETWEEN 50 AND 120;

SELECT * FROM mydb.patient WHERE id_patient = '10169577801F1995';