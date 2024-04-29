import pandas as pd
import math
import numpy as np

# -------- FRONT POINTS --------
INDEX_INTERCANTAL_LEFT = 133
INDEX_INTERCANTAL_RIGHT = 362
INDEX_BIOCULAR_LEFT = 33
INDEX_BIOCULAR_RIGHT = 263
INDEX_JAW_LEFT = 136
INDEX_JAW_RIGHT = 365
INDEX_JAW_MIDDLE = 152
INDEX_EAR_LEFT = 34
INDEX_EAR_RIGHT = 264
INDEX_NOSE_LEFT = 64
INDEX_NOSE_RIGHT = 294
INDEX_NOSE_MIDDLE = 2
INDEX_NOSE_UPPER = 168
INDEX_T_EAR = 454
INDEX_NECK = 378
# -------- LATERAL POINTS --------
INDEX_N_POINT = 168
INDEX_A_POINT = 294
INDEX_B_POINT = 362
INDEX_GNS_POINT = 152
INDEX_SM_POINT = 378
INDEX_GO_POINT = 365
INDEX_T_POINT = 454


#Gotta get the qr size / cm of real qr = scale
#then calc Width * width / scale = cm
QR_CM_SCALE = 4.5 # cm
# QR_CM_SCALE = 4.65 # cm (Posible better scale)

class Measurements():
    def __init__(self, df, width, height):
        self.scale = 0
        self.w = width
        self.h = height
        self.df = df
        self.measures_details = ""
        # print("---------- Measures ----------")
        # print(df)
    
    def generateScale(self, qrs):
        numQrs = 0
        averageQrSize = 0
        
        if qrs != []:
            for qr in qrs:
                # print("QR:", qr)
                averageQrSize += qr[2] + qr[3]
                # print("AVG Loop:", averageQrSize)
                numQrs += 1
            # print("AVG POST Loop:", averageQrSize)
            self.measures_details = "Number of QRs detected: "+str(numQrs)+'\n'
            # print("Num Qrs:", numQrs)
            averageQrSize /= (numQrs*2)
            # print("AVG Qrs Size:", averageQrSize)
            self.scale = averageQrSize / QR_CM_SCALE
            # print("Scale:", self.scale)
            band = self.scale
            self.measures_details += "Mide qrs: " + str(band) + " cm"
            # print("Mide qrs", band)
        else:
            self.scale = 20.93
            band = self.scale
            self.measures_details += "Valor hardcodeado: " + str(band)
            # print("Valor hardcodeado", band)
    
    def getIntercantalWidth(self):
        left = getXValueOfIndex(self.df, INDEX_INTERCANTAL_LEFT)
        right = getXValueOfIndex(self.df, INDEX_INTERCANTAL_RIGHT)
        
        intercantalWidth = ((right - left) * self.w) / self.scale
        # print("Intercantal Width:", intercantalWidth, "cm")
        return round(intercantalWidth, 4)

    def getBiocularWidth(self):
        left = getXValueOfIndex(self.df, INDEX_BIOCULAR_LEFT)
        right = getXValueOfIndex(self.df, INDEX_BIOCULAR_RIGHT)
        
        biocularWidth = ((right - left) * self.w) / self.scale
        # print("Biocular Width:", biocularWidth, "cm")
        return round(biocularWidth, 4)

    def getJawWidth(self):
        left = getXValueOfIndex(self.df, INDEX_JAW_LEFT)
        right = getXValueOfIndex(self.df, INDEX_JAW_RIGHT)
        
        jawWidth = ((right - left) * self.w) / self.scale
        # print("Jaw Width:", jawWidth, "cm")
        return round(jawWidth, 4)
        
        
    def getFaceWidth(self):
        left = getXValueOfIndex(self.df, INDEX_EAR_LEFT)
        right = getXValueOfIndex(self.df, INDEX_EAR_RIGHT)
        faceWidth = ((right - left) * self.w) / self.scale
        
        # print("Face Width:", faceWidth, "cm")
        return round(faceWidth, 4)

    '''
    def getFaceWidth(self):
        left = getXValueOfIndex(self.df, INDEX_EAR_LEFT)
        right = getXValueOfIndex(self.df, INDEX_EAR_RIGHT)
        faceWidth = ((right - left) * self.w) / self.scale
        
        # print("Face Width:", faceWidth, "cm")
        return round(faceWidth, 4)
    '''

    def getFaceWidthAngle(self):
        leftX = getXValueOfIndex(self.df, INDEX_NOSE_LEFT)
        leftY = getYValueOfIndex(self.df, INDEX_NOSE_LEFT)
        
        rightX = getXValueOfIndex(self.df, INDEX_NOSE_RIGHT)
        rightY = getYValueOfIndex(self.df, INDEX_NOSE_RIGHT)
        
        middleX = getXValueOfIndex(self.df, INDEX_NOSE_MIDDLE)
        middleY = getYValueOfIndex(self.df, INDEX_NOSE_MIDDLE)
        
        vectorAx = leftX - middleX
        vectorAy = leftY - middleY
        vectorBx = rightX - middleX
        vectorBy = rightY - middleY
        
        left = np.array([vectorAx, vectorAy], float)
        right = np.array([vectorBx, vectorBy], float)
        
        dot = np.dot(left, right)
        mod = modular(vectorAx, vectorAy, vectorBx, vectorBy)
        maxilarAngle = getAngle(dot/mod)
        
        # print("Angulo Ancho de cara:", maxilarAngle, " degrees")
        return round(maxilarAngle, 4)
    
    def get_mandibular_nasion_angle(self):
        leftX = getXValueOfIndex(self.df, INDEX_NOSE_LEFT)
        leftY = getYValueOfIndex(self.df, INDEX_NOSE_LEFT)
        
        rightX = getXValueOfIndex(self.df, INDEX_NOSE_RIGHT)
        rightY = getYValueOfIndex(self.df, INDEX_NOSE_RIGHT)
        
        middleX = getXValueOfIndex(self.df, INDEX_NOSE_MIDDLE)
        middleY = getYValueOfIndex(self.df, INDEX_NOSE_MIDDLE)
        
        vectorAx = leftX - middleX
        vectorAy = leftY - middleY
        vectorBx = rightX - middleX
        vectorBy = rightY - middleY
        
        left = np.array([vectorAx, vectorAy], float)
        right = np.array([vectorBx, vectorBy], float)
        
        dot = np.dot(left, right)
        mod = modular(vectorAx, vectorAy, vectorBx, vectorBy)
        maxilarAngle = getAngle(dot/mod)
        
        # print("Angulo Ancho de cara:", maxilarAngle, " degrees")
        return round(maxilarAngle, 4)

    def getAreaMaxilarTriangle(self):
        leftX = (getXValueOfIndex(self.df, INDEX_EAR_LEFT) * self.w) / self.scale
        leftY = (getYValueOfIndex(self.df, INDEX_EAR_LEFT) * self.h) / self.scale
        
        rightX = (getXValueOfIndex(self.df, INDEX_EAR_RIGHT) * self.w) / self.scale
        rightY = (getYValueOfIndex(self.df, INDEX_EAR_RIGHT) * self.h) / self.scale
        
        middleX = (getXValueOfIndex(self.df, INDEX_NOSE_MIDDLE) * self.w) / self.scale
        middleY = (getYValueOfIndex(self.df, INDEX_NOSE_MIDDLE) * self.h) / self.scale
        
        areaT = areaTriangle(leftX, leftY, rightX, rightY, middleX, middleY)

        # print("Area de Triangulo Maxilar:", areaT, " cm2")
        return round(areaT, 4)

    def getAreaCranialFossa(self):
        upperNoseX = (getXValueOfIndex(self.df, INDEX_NOSE_UPPER) * self.w) / self.scale
        upperNoseY = (getYValueOfIndex(self.df, INDEX_NOSE_UPPER) * self.h) / self.scale
        
        earX = (getXValueOfIndex(self.df, INDEX_T_EAR) * self.w) / self.scale
        earY = (getYValueOfIndex(self.df, INDEX_T_EAR) * self.h) / self.scale
        
        lowerNoseX = (getXValueOfIndex(self.df, INDEX_NOSE_RIGHT) * self.w) / self.scale
        lowerNoseY = (getYValueOfIndex(self.df, INDEX_NOSE_RIGHT) * self.h) / self.scale
        
        areaT = areaTriangle(upperNoseX, upperNoseY, earX, earY, lowerNoseX, lowerNoseY)

        # print("Area de Fosa Cranial:", areaT, " cm2")
        return round(areaT, 4)

    def getCervicomentalAngle(self):
        leftX = getXValueOfIndex(self.df, INDEX_JAW_MIDDLE)
        leftY = getYValueOfIndex(self.df, INDEX_JAW_MIDDLE)
        
        rightX = getXValueOfIndex(self.df, INDEX_NOSE_RIGHT)
        rightY = getYValueOfIndex(self.df, INDEX_NOSE_RIGHT)
        
        middleX = getXValueOfIndex(self.df, INDEX_NECK)
        middleY = getYValueOfIndex(self.df, INDEX_NECK)
        
        vectorAx = leftX - middleX
        vectorAy = leftY - middleY
        vectorBx = rightX - middleX
        vectorBy = rightY - middleY
        
        left = np.array([vectorAx, vectorAy], float)
        right = np.array([vectorBx, vectorBy], float)
        
        dot = np.dot(left, right)
        mod = modular(vectorAx, vectorAy, vectorBx, vectorBy)
        cervicomentalAngle = 180 - getAngle(dot/mod)
        
        # print("Angulo Cervicomental:", cervicomentalAngle, " degrees")
        return round(cervicomentalAngle, 4)
    
    def get_nose_width(self) -> float:
        left = getXValueOfIndex(self.df, INDEX_NOSE_LEFT)
        right = getXValueOfIndex(self.df, INDEX_NOSE_RIGHT)
        
        nose_width = ((right - left) * self.w) / self.scale
        # print("Nose Width:", nose_width, "cm")
        return round(nose_width, 4)
    
    def get_mandibular_width_angle(self) -> float:
        leftX = getXValueOfIndex(self.df, INDEX_JAW_LEFT)
        leftY = getYValueOfIndex(self.df, INDEX_JAW_LEFT)
        
        rightX = getXValueOfIndex(self.df, INDEX_JAW_RIGHT)
        rightY = getYValueOfIndex(self.df, INDEX_JAW_RIGHT)
        
        middleX = getXValueOfIndex(self.df, INDEX_JAW_MIDDLE)
        middleY = getYValueOfIndex(self.df, INDEX_JAW_MIDDLE)
        
        vectorAx = leftX - middleX
        vectorAy = leftY - middleY
        vectorBx = rightX - middleX
        vectorBy = rightY - middleY
        
        left = np.array([vectorAx, vectorAy], float)
        right = np.array([vectorBx, vectorBy], float)
        
        dot = np.dot(left, right)
        mod = modular(vectorAx, vectorAy, vectorBx, vectorBy)
        mandibular_angle = getAngle(dot/mod)
        
        # print("Mandibylar Width Angel:", mandibular_angle, " degrees")
        return round(mandibular_angle, 4)
# -----------------------------------------------------------------------------
# ----------------------------- LATERAL MEASURES ------------------------------
# -----------------------------------------------------------------------------

    def get_mandibular_nasion_angle(self) -> float:
        leftX = getXValueOfIndex(self.df, INDEX_N_POINT)
        leftY = getYValueOfIndex(self.df, INDEX_N_POINT)
        
        rightX = getXValueOfIndex(self.df, INDEX_GNS_POINT)
        rightY = getYValueOfIndex(self.df, INDEX_GNS_POINT)
        
        middleX = getXValueOfIndex(self.df, INDEX_GO_POINT)
        middleY = getYValueOfIndex(self.df, INDEX_GO_POINT)
        
        vectorAx = leftX - middleX
        vectorAy = leftY - middleY
        vectorBx = rightX - middleX
        vectorBy = rightY - middleY
        
        left = np.array([vectorAx, vectorAy], float)
        right = np.array([vectorBx, vectorBy], float)
        
        dot = np.dot(left, right)
        mod = modular(vectorAx, vectorAy, vectorBx, vectorBy)
        mandibular_nasion_angle = getAngle(dot/mod)
        
        # print("Mandibular Nasion Angle:", mandibular_nasion_angle, " degrees")
        return round(mandibular_nasion_angle, 4)
    
    def get_mandibular_subnasion_angle(self) -> float:
        leftX = getXValueOfIndex(self.df, INDEX_A_POINT)
        leftY = getYValueOfIndex(self.df, INDEX_A_POINT)
        
        rightX = getXValueOfIndex(self.df, INDEX_GNS_POINT)
        rightY = getYValueOfIndex(self.df, INDEX_GNS_POINT)
        
        middleX = getXValueOfIndex(self.df, INDEX_GO_POINT)
        middleY = getYValueOfIndex(self.df, INDEX_GO_POINT)
        
        vectorAx = leftX - middleX
        vectorAy = leftY - middleY
        vectorBx = rightX - middleX
        vectorBy = rightY - middleY
        
        left = np.array([vectorAx, vectorAy], float)
        right = np.array([vectorBx, vectorBy], float)
        
        dot = np.dot(left, right)
        mod = modular(vectorAx, vectorAy, vectorBx, vectorBy)
        mandibular_subnasion_angle = getAngle(dot/mod)
        
        # print("Mandibular Sub-Nasion Angle:", mandibular_subnasion_angle, " degrees")
        return round(mandibular_subnasion_angle, 4)
    
    def get_anb_angle(self) -> float():
        leftX = getXValueOfIndex(self.df, INDEX_N_POINT)
        leftY = getYValueOfIndex(self.df, INDEX_N_POINT)
        
        rightX = getXValueOfIndex(self.df, INDEX_A_POINT)
        rightY = getYValueOfIndex(self.df, INDEX_A_POINT)
        
        middleX = getXValueOfIndex(self.df, INDEX_B_POINT)
        middleY = getYValueOfIndex(self.df, INDEX_B_POINT)
        
        vectorAx = leftX - middleX
        vectorAy = leftY - middleY
        vectorBx = rightX - middleX
        vectorBy = rightY - middleY
        
        left = np.array([vectorAx, vectorAy], float)
        right = np.array([vectorBx, vectorBy], float)
        
        dot = np.dot(left, right)
        mod = modular(vectorAx, vectorAy, vectorBx, vectorBy)
        anb_angle = getAngle(dot/mod)
        
        # print("ANB Angle:", anb_angle, " degrees")
        return round(anb_angle, 4)

    def get_sm_gns(self) -> float:
        left = getXValueOfIndex(self.df, INDEX_SM_POINT)
        right = getXValueOfIndex(self.df, INDEX_GNS_POINT)
        
        sm_gns = ((right - left) * self.w) / self.scale
        # print("Nose Width:", sm_gns, "cm")
        return round(sm_gns, 4)

    def get_middle_ranial_fossa_volume(self) -> float:
        leftX = (getXValueOfIndex(self.df, INDEX_N_POINT) * self.w) / self.scale
        leftY = (getYValueOfIndex(self.df, INDEX_N_POINT) * self.h) / self.scale
        
        rightX = (getXValueOfIndex(self.df, INDEX_A_POINT) * self.w) / self.scale
        rightY = (getYValueOfIndex(self.df, INDEX_A_POINT) * self.h) / self.scale
        
        middleX = (getXValueOfIndex(self.df, INDEX_T_POINT) * self.w) / self.scale
        middleY = (getYValueOfIndex(self.df, INDEX_T_POINT) * self.h) / self.scale
        
        areaT = areaTriangle(leftX, leftY, rightX, rightY, middleX, middleY)

        # print("Middle Cranial fossa volume:", areaT, " cm2")
        return round(areaT, 4)

def getXValueOfIndex(df, index):
    return df.loc[[index]].iloc[0]['X']

def getYValueOfIndex(df, index):
    return df.loc[[index]].iloc[0]['Y']

def modular(Ax, Ay, Bx, By):
    A = math.sqrt(pow(Ax,2) + pow(Ay, 2))
    B = math.sqrt(pow(Bx,2) + pow(By, 2))
    return A*B
    
def getAngle(a):
    return abs(math.degrees(np.arccos(a)))

def areaTriangle(x1, y1, x2, y2, x3, y3):
    return abs((0.5)*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2)))
