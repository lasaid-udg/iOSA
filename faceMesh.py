import cv2
import mediapipe as mp
import pandas as pd
from qrDetection import *

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
df = pd.DataFrame()


class Facemesh:
    def __init__(self, image, indexList, face_mesh):
        self.image = image
        self.indexList = indexList
        self.face_mesh = face_mesh
        self.qrs = QrCodes()
        self.isResizeDone = False
        
        self.height, self.width, _ = image.shape
        self.coordinates = []
        
    def getFaceMeshResults(self):
        #Runs facemesh application over image provided and returns all landmarks
        self.results = self.face_mesh.process(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))

    def resizeImage(self):
        # print("Heigh:", self.height, "width:", self.width)
        if self.height > 1500:
            self.image = cv2.resize(self.image, (0,0), fx=0.5, fy=0.5) 
        self.isResizeDone = True
        self.height, self.width, _ = self.image.shape
        # print("Heigh:", self.height, "width:", self.width)
        
    def getCoordinates(self):
        if self.results.multi_face_landmarks is not None:
            for face_landmarks in self.results.multi_face_landmarks:
                for i in self.indexList:
                    x = face_landmarks.landmark[i].x 
                    y = face_landmarks.landmark[i].y
                    z = face_landmarks.landmark[i].z
                    self.coordinates.append([x,y,z,i])

    def drawLandmark(self):
        for coordinate in self.coordinates:
            x = int(coordinate[0] * self.width)
            y = int(coordinate[1] * self.height)
            index = coordinate[3]
            imageWithFaceLandmarks = cv2.circle(self.image, (x, y), 3, (255, 0, 255), 2)
            imageWithFaceLandmarks = cv2.putText(self.image, str(index), (x,y), cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,145))
        return imageWithFaceLandmarks
    
    def createDataFrameFromCoordinates(self):
        X = []
        Y = []
        Z = []
        I = []
        
        for coordinate in self.coordinates:
            X.append(coordinate[0])
            Y.append(coordinate[1])
            Z.append(coordinate[2])
            I.append(coordinate[3])
        
        coords = list(zip(I,X,Y,Z))
        self.df = pd.DataFrame(coords, columns=['Landmark','X', 'Y', 'Z'])
        self.df = self.df.set_index('Landmark')

    def createFaceMesh(self):
        self.resizeImage()
        self.getFaceMeshResults()
        self.getCoordinates()
        self.createDataFrameFromCoordinates()
        #self.qrCode()
        #self.drawLandmark()
    
    def qrCode(self):
        if not self.isResizeDone:
            self.resizeImage()
        invertedImage = self.qrs.getBlackWhiteInvertedImage(self.image)
        self.qrs.detectQR(invertedImage)
        self.qrs.drawQRcodes()
        self.qrs.getQrCords()