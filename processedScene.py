from PyQt5.QtWidgets import QGraphicsScene

from moveablePoint import *

class ProcessedScene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self.points = []
        
    def setPixmap(self, pix, w, h):
        pixmap = self.addPixmap(pix.scaled(w, h, QtCore.Qt.KeepAspectRatio))
        self.width = pixmap.boundingRect().width()
        self.height = pixmap.boundingRect().height()
        self.update()
        
    def drawPoints(self, coordinates, tag):
        self.points = []
        for i in coordinates:
            x = int(i[0] * self.width)
            y = int(i[1] * self.height)
            
            self.points.append(MoveablePoint(int(i[3]), x, y, tag))
            self.addItem(self.points[-1])
            
        self.update()

        # print("---------- COORDS DRAW ----------")
        # print(coordinates)
