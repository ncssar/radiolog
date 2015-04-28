#'FingerTabs' - Horizontal Text, Horizontal Tabs in PyQt
# This [trivial fingertab gist](https://gist.github.com/LegoStormtroopr/5075267)
# is released as Public Domain, but boy would it be swell if you could credit me,
# or tweet me [@LegoStormtoopr](http://www.twitter.com/legostormtroopr) to say thanks!

# minimal syntax changes to port to PyQt5 TMG 3-9-15

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class FingerTabBarWidget(QTabBar):
    def __init__(self, parent=None, *args, **kwargs):
        self.tabSize = QSize(kwargs.pop('width',100), kwargs.pop('height',25))
        QTabBar.__init__(self, parent, *args, **kwargs)

    def paintEvent(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionTab()

        for index in range(self.count()):
            self.initStyleOption(option, index)
            tabRect = self.tabRect(index)
            tabRect.moveLeft(10)
            painter.drawControl(QStyle.CE_TabBarTabShape, option)
            painter.drawText(tabRect, Qt.AlignVCenter |\
                             Qt.TextDontClip, \
                             self.tabText(index));
        painter.end()
    def tabSizeHint(self,index):
        return self.tabSize

# Shamelessly stolen from this thread:
#   http://www.riverbankcomputing.com/pipermail/pyqt/2005-December/011724.html
class FingerTabWidget(QTabWidget):
    """A QTabWidget equivalent which uses our FingerTabBarWidget"""
    def __init__(self, parent, *args):
        QTabWidget.__init__(self, parent, *args)
        self.setTabBar(FingerTabBarWidget(self))