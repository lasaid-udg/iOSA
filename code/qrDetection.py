import cv2
import numpy as np
from pyzbar import pyzbar

class QrCodes():
	def __init__(self):
		self.qrCoords = []

	def getBlackWhiteInvertedImage(self, image):
		mask = cv2.inRange(image,(0,0,0),(150,150,150)) # 255
		thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
		self.inverted = 255-thresholded # black-in-white
		return self.inverted

	def detectQR(self, image):
		self.qrs = (pyzbar.decode(image))
		return self.qrs

	def drawQRcodes(self):
		for qr in self.qrs: 
			x, y, w, h = drawRectangleOnQR(self.inverted, qr)
			drawTextOverImage(self.inverted, x, y)

	def getQrCords(self):
		for qr in self.qrs:
			self.qrCoords.append(qr.rect)
		return self.qrCoords

def processImageBlackWhiteInverted(image):
	mask = cv2.inRange(image,(0,0,0),(200,200,200))
	thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
	inverted = 255-thresholded # black-in-white
	return inverted

def detectQR(image):
	return (pyzbar.decode(image))

#def drawQRcodes(image, barcodes):
#	for barcode in barcodes: 
#		x, y, w, h = drawRectangleOnQR(image, barcode)
#		drawTextOverImage(image, x, y)

def drawRectangleOnQR(image, barcode):
	# extract the bounding box location of the barcode and draw the
	# bounding box surrounding the barcode on the image
	(x, y, w, h) = barcode.rect
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
	return x, y, w, h

def drawTextOverImage(image, x, y): 
	text = "{} ({})".format("Detected", "QR")
	cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 0, 255), 2)	
