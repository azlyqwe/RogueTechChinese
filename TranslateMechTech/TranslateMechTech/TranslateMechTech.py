# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QApplication
import sys
sys.path.append("./dealCore")
#sys.path.append("./")
from dealCore.myWindow import myWindow


app = QApplication(sys.argv)

w = myWindow()
w.show()

app.exec()
