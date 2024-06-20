import pathlib
from os import listdir
import os

from contourDetection import *
from faceMesh import *
from qrDetection import *

import threading
import time

class QrThread(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.args = args
    
    def run(self):
        # print("Qr Thread Starting...")
        obtainQrCodePositions(self.args[0])
        #qrs.drawQRcodes()
        qrs.getQrCords()
        # print("Qr Thread Done")

IMAGE_PROCESSED = []
IMAGE_FILES = []
front_index_list = [34, 264, 133, 362,
                    33, 263, 136, 365,
                    152, 64, 294,
                    2]

profile_index_list =[168,
                    #34, 264, 356, 389, 454, 127, 162, 234, #ears
                    454,
                    294, #nose
                    152, #menton
                    378, #neck
                    362,
                    365]

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
qrs = QrCodes()

def getImagesPathFromDirectory(readPath, writePath):	
    validExtensions = [".jpg",".gif",".png", ".jpeg"]
    for file in listdir(readPath):
        ext = os.path.splitext(file)[1]
        if ext.lower() in validExtensions:
            IMAGE_FILES.append(readPath+'/%s' % file)
            IMAGE_PROCESSED.append(writePath+'/%s' % file)

def getImageWritePath(imagePath):
    filename = os.path.splitext(imagePath)[0]
    ext = os.path.splitext(imagePath)[1]
    return (filename + "_processed" + ext)

def showImage(image):
	cv2.imshow("Image", image)
	cv2.waitKey(0)

def obtainQrCodePositions(image):
    invertedImage = qrs.getBlackWhiteInvertedImage(image)
    return qrs.detectQR(invertedImage)

def processImage(imagePath, tag):
    with mp_face_mesh.FaceMesh(static_image_mode=True,
        max_num_faces=1, min_detection_confidence=0.5) as faceMesh:
        
        im = cv2.imread(imagePath)
        if tag == "Front":
            image = Facemesh(im, front_index_list, faceMesh)
        else: 
            image = Facemesh(im, profile_index_list, faceMesh)

        runQr = QrThread(image.image)
        runQr.daemon = True
        runQr.start()
        # print("Thread Facemesh: Starting...")
        image.createFaceMesh()
        # print("Thread Facemesh: Done")
        
        return image