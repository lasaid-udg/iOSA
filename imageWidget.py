#from asyncio.windows_events import NULL
from PyQt5 import uic
from PyQt5.QtWidgets import QGraphicsView, QWidget, QFileDialog
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap

import pathlib
import json
import threading
import os
import shutil

from imageProcessing import *
from processedScene import *
from measures import *
from qrDetection import *
from DetailsWidget import DetailsWidget
from log import Log
from database import MultimediaDb, DatabaseThread, insert_db_thread_event

UI_PATH = "ui/imageWidget.ui"

FRONT_IMG_PATH = r"multimedia\photos\front"
LATERAL_IMG_PATH = r"multimedia\photos\lateral"
FRONT_IMG_DB = r"multimedia\\photos\\front"
LATERAL_IMG_DB = r"multimedia\\photos\\lateral"
IMG_EXTENCION = ".jpeg"
IMG_LATERAL_POINTS_PATH = r"bin\icons\lateral_face_points.png"
IMG_FRONT_POINTS_PATH = r"bin\icons\front_face_points.png"

BLANK = ''
COORDINATES_INDEX = 3
FRONT_TAG = 0
LATERAL_TAG = 1
HARCODE_POINTS = [
    [0.632787226, 0.425296607, 0.0, 168],
    [0.541116168, 0.460134664, 0.0, 454],
    [0.645365269, 0.491916434, 0.0, 294],
    [0.647365269, 0.588999069, 0.0, 152],
    [0.623120958, 0.605077844, 0.0, 378],
    [0.646402395, 0.556341184, 0.0, 362],
    [0.561288623, 0.554963673, 0.0, 365]
]


class ImageWidget(QWidget):
    def __init__(self, patient, is_edit):
        super(ImageWidget, self).__init__()
        self._is_edit = is_edit
        self._patient = patient
        self.points = []
        self.path = BLANK
        self.currentPointSelected = None
        self.zoom = 0
        self.pixmap = QPixmap()
        self.coordinates = BLANK
        self.details_window = DetailsWidget()
        
        self.__loadUiFile(pathlib.Path(__file__).parent)
        self.__os_dir()
        self.__defineWidgets()
        self.__defineScene()
        self.__defineButton()
        self.__defineMeasurments()
        self.__clearScene()
        self.__getScaleRatioImage()


#INSTANTIATE

    def __loadUiFile(self, path):
        uic.loadUi(path / UI_PATH, self)

    def __defineWidgets(self):        
        self.processedGraphicsView = self.findChild(QGraphicsView, "processed_graphicsView")
        
        self.selectImageButton = self.findChild(QPushButton, "selectImageButton")
        self.nextPageButton = self.findChild(QPushButton, "nextPageButton")
        self.previousPageButton = self.findChild(QPushButton, "previousPageButton")
        self.zoomInButton = self.findChild(QPushButton, "zoomInButton")
        self.zoomOutButton = self.findChild(QPushButton, "zoomOutButton")
        self.redoButton = self.findChild(QPushButton, "redoButton")
        self.undoButton = self.findChild(QPushButton, "undoButton")
        self.updateMeasurementsButton = self.findChild(QPushButton, "updateMeasuresButton")
        self.details_button = self.findChild(QPushButton, "details_push_button")

        self.previousPageButton.hide()
        self.redoButton.hide()
        self.undoButton.hide()
        
        self.tag = self.findChild(QComboBox, "imageTagComboBox")
    
    def __defineScene(self):
        self.processedScene = ProcessedScene()
        self.processedGraphicsView.setScene(self.processedScene)
        self.processedScene.setFocusOnTouch(True)
        
    def __defineButton(self):
        self.selectImageButton.clicked.connect(self.selectImage)
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomOutButton.clicked.connect(self.zoomOut)
        self.tag.currentTextChanged.connect(self.changeTag)
        self.updateMeasurementsButton.clicked.connect(self.getMeasurements)
        self.details_button.clicked.connect(self.open_details_window)
        self.nextPageButton.clicked.connect(self.insertImage)
        
    def __defineMeasurments(self):
        self.measurmentLabel1 = self.findChild(QLabel, "measurement_label1")
        self.measurment_label_1_2=self.findChild(QLabel,"measurement_label_1_2")
        self.measurmentLabel2 = self.findChild(QLabel, "measurement_label2")
        self.measurmentLabel3 = self.findChild(QLabel, "measurement_label3")
        self.measurmentLabel4 = self.findChild(QLabel, "measurement_label4")
        self.measurmentLabel5 = self.findChild(QLabel, "measurement_label5")
        self.measurment_label_7 = self.findChild(QLabel, "measurement_label_7")
        self.measurment_label_8 = self.findChild(QLabel, "measurement_label_8")
        self.measurment1 = self.findChild(QLineEdit, "measurement_lineEdit1")
        self.measurment2 = self.findChild(QLineEdit, "measurement_lineEdit2")
        self.measurment3 = self.findChild(QLineEdit, "measurement_lineEdit3")
        self.measurment4 = self.findChild(QLineEdit, "measurement_lineEdit4")
        self.measurment5 = self.findChild(QLineEdit, "measurement_lineEdit5")
        self.measurment6 = self.findChild(QLineEdit, "measurement_lineEdit6")
        self.measurment_7 = self.findChild(QLineEdit, "measurement_lineEdit_7")
        self.measurment_8 = self.findChild(QLineEdit, "measurement_lineEdit_8")
        self.image_reference = self.findChild(QLabel, "image_reference_label")

#IMAGES

    def __getScaleRatioImage(self):
        self.w = int(self.width()/1.5)
        self.h = int(self.height()/1.5)

    def selectImage(self):
        self.findFileWindow()
        if self.isValidPath():
            self.setPixmap()
            self.processImage()
            if self.isUnsuccessfulDetection():
                self.unsuccessfulDetectionHandler()
            else:
                self.drawPointsOnScene()
                self.getMeasurements()
        else:
            self.unsuccessfulImageSelectionHandler()

    def findFileWindow(self):
        #TO DO: Change default directory path. STATUS: Changed. Pending revision.
        self.fname = QFileDialog.getOpenFileName(self, "Open File", str(pathlib.Path().absolute()), "Images (*.png *.xpm *.jpg *.jpeg)")
        self.path = self.fname[0]

    def __clearScene(self):
        self.processedScene.clear()

    def setPixmap(self):
        self.pixmap = QPixmap(self.path)
        self.processedScene.clear()
        self.processedScene.setPixmap(self.pixmap, self.w, self.h)
        
    def processImage(self):
        if not self.pixmap.isNull():
            if self.isFrontPicture():
                self.image = processImage(self.path, "Front")
            else:
                self.image = processImage(self.path, "Lateral")
            
            self.coordinates = self.image.coordinates
            self.df = self.image.df
            
            if not self.isFrontPicture():
                self.coordinates = HARCODE_POINTS
    
    def drawPointsOnScene(self):
        self.processedScene.drawPoints(self.coordinates, self.tag.currentText())

    def createDataframe(self):
        X = []
        Y = []
        I = []
        x = []
        y = []
        i = []
        
        w = self.processedScene.width
        h = self.processedScene.height
        # print("Width", w)
        # print("Height", h)
        
        for p in self.processedScene.points:
            if not p.hasMoved:
                X.append(p.originalPosX / w)
                Y.append(p.originalPosY / h)
                I.append(p.index)
                x.append(p.originalPosX)
                y.append(p.originalPosY)
                i.append(p.index)
            else:
                X.append(p.updatedPosX / w)
                Y.append(p.updatedPosY / h)
                I.append(p.index)
                x.append(p.originalPosX)
                y.append(p.originalPosY)
                i.append(p.index)
            
            # print("X", X)
            # print("Y", Y)
            # print("I", I)
            # print("x", x)
            # print("y", y)
            # print("i", i)
                
        coords = list(zip(I,X,Y))
        # print("---------- IN-THREAD COORDS ----------")
        # print(coords)
        self.df = pd.DataFrame(coords, columns=['Landmark','X', 'Y'])
        self.df = self.df.set_index('Landmark')
        # print("---------- IN-THREAD ----------")
        # print(self.df)

#MEASUREMENTS

    def getMeasurements(self):
        if not self.pixmap.isNull():

            # print("Img Coords:", self.coordinates)
            dfThread = threading.Thread(target=self.createDataframe())
            dfThread.start()
            qrCoords, w, h = self.getQrInformation()

            dfThread.join()
            # print("---------- THREAD ----------")
            # print(self.df)
            # print("Thread Get Measurements Starting...")
            self.m = Measurements(self.df, w, h)
            self.m.generateScale(qrCoords)
            self.details_window.add_detail(self.m.measures_details)
            changeLabelsThread = threading.Thread(target=self.changeMeasurementLabels()).start()
            if self.tag.currentText() == "Front":
                self.getFrontMeasurements()
            else:
                face_width = self.get_front_face_width(self.m.scale, self.m.w)
                self.getProfileMeasurements(face_width)

    
            # print("Thread Get Measurements Done...")
            
    def getFrontMeasurements(self):
        self.measurment1.setText(str(self.m.getFaceWidth()) + " cm")
        self.measurment2.setText(str(self.m.getFaceWidthAngle()) + " °")
        self.measurment3.setText(str(self.m.getIntercantalWidth()) + " cm")
        self.measurment4.setText(str(self.m.getBiocularWidth()) + " cm")
        self.measurment5.setText(str(self.m.getJawWidth()) + " cm")
        self.measurment6.setText(str(self.m.getAreaMaxilarTriangle()) + " cm2")
        self.measurment_7.setText(str(self.m.get_mandibular_width_angle())+" °")
        self.measurment_8.setText(str(self.m.get_nose_width()) + " cm")
        # add nose
    
    def getProfileMeasurements(self, face_width):
        self.measurment1.setText(str(self.m.get_mandibular_nasion_angle())+" °")
        self.measurment2.setText(str(self.m.get_mandibular_subnasion_angle())+" °")
        self.measurment3.setText(str(self.m.get_anb_angle()) + " °")
        self.measurment4.setText(str(self.m.get_sm_gns()) + " cm")
        self.measurment5.setText(str(self.m.get_middle_ranial_fossa_volume()*face_width)+" cm3")

    def get_front_face_width(self, scale, w):
        multimedia_db = MultimediaDb()
        db_thread = DatabaseThread(
            target=multimedia_db.get_front_photo_data,
            args=(self._patient.apnea_study.id,)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        front = db_thread.join()

        if front is None:
            faceWidth = -1
        else:
                    # front[2] = coordinates
            points = json.loads(json.loads(front[COORDINATES_INDEX]))
            df = pd.DataFrame.from_dict(points)

            left = getXValueOfIndex(df, str(INDEX_EAR_LEFT))
            right = getXValueOfIndex(df, str(INDEX_EAR_RIGHT))
            faceWidth = ((right - left) * self.m.w) / scale
                    
                    # print("Face Width:", faceWidth, "cm")
        return round(faceWidth, 4)
        
    def changeMeasurementLabels(self):
        # print("Thread Changing Labels Starting...")
        if self.tag.currentText() == "Front":
            self.changeLabelsToFrontalMeasurements()
        else:
            self.changeLabelsToProfileMeasurements()
        # print("Thread Changing Labels Done...")
    
    def changeLabelsToFrontalMeasurements(self):
        self.measurmentLabel1.setText("Face Width")
        self.measurmentLabel1.setHidden(False)
        self.measurmentLabel2.setHidden(False)
        self.measurment2.setVisible(True)
        
        self.measurmentLabel2.setText("Intercantal Width")
        self.measurment3.setVisible(True)

        self.measurment_label_1_2.setText("Face width-midface\ndepth angle")
        self.measurment_label_1_2.setVisible(True)
        
        self.measurmentLabel3.setHidden(False)
        self.measurmentLabel3.setText("Biocular width")
        self.measurment4.setVisible(True)
        
        self.measurmentLabel4.setHidden(False)
        self.measurmentLabel4.setText("Mandibular width")
        self.measurment5.setVisible(True)
        
        self.measurmentLabel5.setHidden(False)
        self.measurmentLabel5.setText("Maxilary triangle\narea")
        self.measurment6.setVisible(True)

        image_points_reference = QPixmap()
        image_points_reference.load(IMG_FRONT_POINTS_PATH)
        self.image_reference.setPixmap(image_points_reference)
    
    def changeLabelsToProfileMeasurements(self):
        self.measurmentLabel1.setText("Mandibular nasion angle")
        self.measurment_label_1_2.setText("Mandibular subnasion angle")
        self.measurmentLabel2.setText("ANB angle")
        self.measurmentLabel3.setText("Submental distance")
        self.measurmentLabel4.setText("Middle cranial fossa volume")

        self.measurment1.setVisible(True)
        self.measurment2.setVisible(True)
        self.measurment3.setVisible(True)
        self.measurment4.setVisible(True)
        self.measurment5.setVisible(True)

        self.measurment1.setPlaceholderText("°")
        self.measurment2.setPlaceholderText("°")
        self.measurment3.setPlaceholderText("°")
        self.measurment4.setPlaceholderText("cm")
        self.measurment5.setPlaceholderText("cm3")

        self.measurmentLabel5.setHidden(True)
        self.measurment_label_7.setHidden(True)
        self.measurment_label_8.setHidden(True)
        self.measurment6.setVisible(False)
        self.measurment_7.setVisible(False)
        self.measurment_8.setVisible(False)

        image_points_reference = QPixmap()
        image_points_reference.load(IMG_LATERAL_POINTS_PATH)
        self.image_reference.setPixmap(image_points_reference)
    
    def getQrInformation(self):
        if self._is_edit:
            im = cv2.imread(self.path)
            facemesh = Facemesh(im, [], [])
            facemesh.qrCode()
            return facemesh.qrs.qrCoords, facemesh.width, facemesh.height
        else:
            self.image.qrCode()
            return self.image.qrs.qrCoords, self.image.width, self.image.height
    
    def copy_image(self):
        if self.isValidPath():
            home_path = str(pathlib.Path().absolute())
            if not self._is_edit:
                file_name = str(self._patient.apnea_study.id) + IMG_EXTENCION
            else:
                file_name = str(self._patient.apnea_study.id) + IMG_EXTENCION
            
            if self.isFrontPicture():
                fname = home_path + "\\" + FRONT_IMG_PATH + "\\" + file_name
                image_side = FRONT_IMG_DB
            else:
                fname = home_path + "\\" + LATERAL_IMG_PATH + "\\" + file_name
                image_side = LATERAL_IMG_DB

            try:
                shutil.copyfile(str(self.path), fname)
                self.path = image_side + r"\\" + file_name
                # print(self.path)
            except shutil.SameFileError:
                    self.__insert_copy_image_error()
        else:
            pass


#DATABASE
    def insertImage(self):
        self.createDataframe()
        self.json = self.df.to_json()
        self.copy_image()
        
        # Check the image is loaded
        if not self.pixmap.isNull():
            # Edit flow variable
            if self._is_edit:
                # Update existing image
                if self.getPictureIdFromTag() != "":
                    self.updateToDatabase()
                # Insert image for the first time in edit flow if it wasn't loaded in lineal flow
                else:
                    self.insertToDatabase()
            # Lineal flow
            else:
                # Insert image for the first time
                self.insertToDatabase()
        # If there is no image, but is edit, show image load error message
        elif self._is_edit:
            self.errorOnSaving()

    def updateToDatabase(self):
        tag = self.getTag()
        apnea_study_id = self._patient.apnea_study.id

        tuple_data = (
            str(self.path),
            str(json.dumps(self.json)),
            tag
        )

        db_multimedia = MultimediaDb()
        if tag == FRONT_TAG:
            db_thread = DatabaseThread(
                target=db_multimedia.update_front_photo,
                args=(apnea_study_id, tuple_data)
            )
        elif tag == LATERAL_TAG:
            db_thread = DatabaseThread(
                target=db_multimedia.update_lateral_photo,
                args=(apnea_study_id, tuple_data)
            )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        db_thread.join()

    def insertToDatabase(self):
        # print(self.path)
        tag = self.getTag()
        tuple_data = (
            self._patient.apnea_study.id,
            str(self.path),
            str(json.dumps(self.json)),
            tag
        )
        multimedia_db = MultimediaDb()
        if tag == FRONT_TAG:
            db_thread = DatabaseThread(
                target=multimedia_db.insert_front_photo,
                args=(tuple_data,)
            )
        elif tag == LATERAL_TAG:
            db_thread = DatabaseThread(
                target=multimedia_db.insert_lateral_photo,
                args=(tuple_data,)
            )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        imageId = db_thread.join()

#BUTTONS

    def zoomIn(self):
        if not self.pixmap.isNull():
            self.zoom += 1
            self.resizeImage(1.25)

    def zoomOut(self):
        if not self.pixmap.isNull() and self.zoom > 0:
            self.zoom -= 1
            self.resizeImage(0.8)

    def resizeImage(self, factor):
        self.processedGraphicsView.scale(factor, factor)

    def changeTag(self, text):
        self.tag.setCurrentText(text)
        self.changeMeasurementLabels()

#AUX
    def open_details_window(self):
        self.details_window.show_details_window()

    def isFrontPicture(self):
        return (self.tag.currentText() == "Front")
    
    def isValidPath(self):
        return self.path != ""
    
    def isUnsuccessfulDetection(self):
        return not self.coordinates
    
    def getPictureIdFromTag(self):
        if self.isFrontPicture():
            return self._patient.apnea_study.front_photo.id
        else:
            return self._patient.apnea_study.lateral_photo.id
    
    def getTag(self):
        if self.isFrontPicture(): 
            return 0
        else: 
            return 1

    def unsuccessfulDetectionHandler(self):
        self.errorOnProcessing()
        self.pixmap.swap(QPixmap())
        self.__clearScene()

    def unsuccessfulImageSelectionHandler(self):
        self.pixmap.swap(QPixmap())
        self.__clearScene()
    
    def __insert_copy_image_error(self):
        log = Log()
        log.insert_log_error()

    def errorOnProcessing(self):
        msg = QMessageBox()
        msg.setWindowTitle("Alerta!")
        msg.setText("Error en la deteccion de puntos craneofaciales. Seleccione otra imagen.")
        msg.exec_()
        
    def errorOnSaving(self):
        msg = QMessageBox()
        msg.setWindowTitle("Alerta!")
        msg.setText("Error en el guardado de la imagen.")
        msg.exec_()
    
    def __os_dir(self):
        try:
            os.makedirs(os.path.normpath(FRONT_IMG_PATH), exist_ok=False)
            
        except (FileExistsError, OSError):
            # print("Dirr already exist")
            self.insert_directory_error()

        try:
            os.makedirs(os.path.normpath(LATERAL_IMG_PATH), exist_ok=False)
        except (FileExistsError, OSError):
            self.insert_directory_error()
    
    def insert_directory_error(self) -> None:
        log = Log()
        log.insert_log_error()
