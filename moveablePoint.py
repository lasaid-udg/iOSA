from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import QPointF

RED = "#ff0000"
AQUA = "#00ffee"
PURPLE = "#9300ff"
YELLOW = "#edff00"
BLUE = "#0019ff"
TST = "#0019ff"
TSTC = "#00ffee"
# -------- FRONT POINTS --------
INDEX_ENR = 133
INDEX_ENL = 362
INDEX_EXR = 33
INDEX_EXL = 263
INDEX_GORF = 136
INDEX_GOLF = 365
INDEX_GNF = 152
INDEX_TR = 34
INDEX_TL = 264
INDEX_RAL = 64
INDEX_LAL = 294
INDEX_SNF = 2
# -------- LATERAL POINTS --------
INDEX_N_POINT = 168
INDEX_A_POINT = 294
INDEX_B_POINT = 362
INDEX_GNS_POINT = 152
INDEX_SM_POINT = 378
INDEX_GO_POINT = 365
INDEX_T_POINT = 454
# ---------- LATERAL COLORS ----------
N_POINT_COLOR = "#3f48cc"
A_POINT_COLOR = "#b83dba"
B_POINT_COLOR = "#ff7f27"
GNS_POINT_COLOR = "#ec1c24"
SM_POINT_COLOR = "#ffca18"
GO_POINT_COLOR = "#0ed145"
T_POINT_COLOR = "#8cfffb"
FRONT_IMG = "Perfil"
# ---------- FRONT COLORS ----------
ENR_POINT_COLOR = "#ff0000"
ENL_POINT_COLOR = "#0000ff"
EXR_POINT_COLOR = "#ffed00"
EXL_POINT_COLOR = "#00fff1"
GORF_POINT_COLOR = "#c200ff"
GOLF_POINT_COLOR = "#ff9a00"
GNF_POINT_COLOR = "#0096ff"
TR_POINT_COLOR = "#26ff00"
TL_POINT_COLOR = "#ff0077"
RAL_POINT_COLOR = "#574200"
LAL_POINT_COLOR = "#029720"
SNF_POINT_COLOR = "#a50040"
NOSE_UPPER_POINT_COLOR = "#"


class MoveablePoint(QGraphicsEllipseItem):
    def __init__(self, i, x, y, tag):
        r = 3
        super().__init__(x-(r/2), y-(r/2), r, r)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.index = i
        self.originalPosX = x
        self.originalPosY = y
        self.hasMoved = False
        self.isSelected = False
        self.setPens("yellow")
        if tag == FRONT_IMG:
            self.__add_lateral_color()
        else:
            self.__add_front_color()
        
    def setPens(self, color):
        pen = QPen(QColor(color))
        pen.setWidth(1)      
        self.setPen(pen)
    
    def mousePressEvent(self, event):
        pass
    
    def mouseMoveEvent(self, event):
        originalCursosPos = event.lastScenePos()
        updatedCursorPosition = event.scenePos()
        
        originalPosition = self.scenePos()
        
        ucX = updatedCursorPosition.x() - originalCursosPos.x() + originalPosition.x()
        ucY = updatedCursorPosition.y() - originalCursosPos.y() + originalPosition.y()
        
        #print('Scene Pos -> x:', ucX, 'y:', ucY)
        self.setPos(QPointF(ucX, ucY))    
    
    def mouseReleaseEvent(self, event):
        self.updatedPosX = self.originalPosX + self.pos().x()
        self.updatedPosY = self.originalPosY + self.pos().y()
        self.hasMoved = True
        #print('Scene Pos -> x:', self.scenePos().x(), 'y:', self.scenePos().y())
        #print('Original Pos -> x:', self.originalPosX, 'y:', self.originalPosY)
        #print('Updated Pos -> x:', self.updatedPosX, 'y:', self.updatedPosY)
        #print("x: ", self.pos().x(), "y:", self.pos().y())

    def __add_front_color(self) -> None:
        if self.index == INDEX_ENR:
            self.setPens(ENR_POINT_COLOR)
        
        elif self.index == INDEX_ENL:
            self.setPens(ENL_POINT_COLOR)
        
        elif self.index == INDEX_EXL:
            self.setPens(EXL_POINT_COLOR)

        elif self.index == INDEX_EXR:
            self.setPens(EXR_POINT_COLOR)
        
        elif self.index == INDEX_GOLF:
            self.setPens(GOLF_POINT_COLOR)
        
        elif self.index == INDEX_GORF:
            self.setPens(GORF_POINT_COLOR)
        
        elif self.index == INDEX_GNF:
            self.setPens(GNF_POINT_COLOR)
        
        elif self.index == INDEX_TR:
            self.setPens(TR_POINT_COLOR)
        
        elif self.index == INDEX_TL:
            self.setPens(TL_POINT_COLOR)
        
        elif self.index == INDEX_RAL:
            self.setPens(RAL_POINT_COLOR)
        
        elif self.index == INDEX_LAL:
            self.setPens(LAL_POINT_COLOR)
        
        elif self.index == INDEX_SNF:
            self.setPens(SNF_POINT_COLOR)
        
        else:
            pass

    def __add_lateral_color(self) -> None:
        if self.index == INDEX_GNS_POINT:
            self.setPens(GNS_POINT_COLOR)

        elif self.index == INDEX_N_POINT:
            self.setPens(N_POINT_COLOR)

        elif self.index == INDEX_A_POINT:
            self.setPens(A_POINT_COLOR)

        elif self.index == INDEX_SM_POINT:
            self.setPens(SM_POINT_COLOR)

        elif self.index == INDEX_T_POINT:
            self.setPens(T_POINT_COLOR)
        
        elif self.index == INDEX_B_POINT:
            self.setPens(B_POINT_COLOR)
        
        elif self.index == INDEX_GO_POINT:
            self.setPens(GO_POINT_COLOR)
            
        else:
            pass
