import cv2

def grayScaleImage(image):
    return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

def getImageContours(grayImage):
    edged = cv2.Canny(grayImage, 30, 200)
    contours,hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    return contours

def drawContoursOnImage(image, contours):
    return cv2.drawContours(image,contours,-1,(0,255,0),2) 

def processCountoursOnImage(image):
	contours = getImageContours(grayScaleImage(image))
	drawContoursOnImage(image, contours)
 
if __name__ == "__main__":
    pass