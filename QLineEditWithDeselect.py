from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QLineEditWithDeselect(QLineEdit):
    def __init__(self,parent=None):
        self.parent=parent
        self.lastKeyText=''
        super(QLineEditWithDeselect,self).__init__(parent)
    
    # for some reason, the entire existing text (if any) was always selected;
    #  use this method to deselect all and move the cursor to the end
    def focusInEvent(self,e):
        QLineEdit.focusInEvent(self,e) # do this to show the blinking cursor
        self.deselect()
        self.setCursorPosition(len(self.text()))

    # capture the text of the last key pressed, for use in messageChanged handling (#506)
    def keyPressEvent(self,e):
        self.lastKeyText=e.text()
        QLineEdit.keyPressEvent(self,e)
