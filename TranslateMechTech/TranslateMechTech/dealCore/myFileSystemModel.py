#-*-coding:utf-8-*-
from PySide6.QtWidgets import QFileSystemModel

class myFileSystemModel(QFileSystemModel):

    def columnCount(self, parent):

        return super().columnCount(parent) + 1

    def data(self, index, role):
        return super().data(index, role)
    """description of class"""


