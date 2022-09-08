# -*- coding: utf-8 -*-




from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout, QWidget, QAbstractItemView, QTreeView, QFileSystemModel, QMenu, QListView, QLineEdit, QSpacerItem, QSizePolicy
from PySide6 import QtCore, QtGui
from translateCore import TranslateCore


class MyDrapListView(QListView):

    def __init__(self, parent=None):
        super(MyDrapListView, self).__init__(parent)

    #def dropEvent(self, event: PySide6.QtGui.QDropEvent) -> None:
    #return super().dropEvent(event)
    def dropEvent(self, event):
        pos=event.pos()  #获取拖入事件的坐标
        aimIndex=self.indexAt(pos)  #获取当前坐标下的index
        aimRow=aimIndex.row()  #获取行数
        if aimRow == -1: #处理拖拽到最末尾
            aimRow = self.model().rowCount()

        sorIndex  = self.selectedIndexes()[0] #获取源index
        sorRow = sorIndex.row() #获取源行
        if sorIndex == aimIndex: #处理不拖拽
            return
        text = self.model().data(sorIndex, QtCore.Qt.DisplayRole)
        
        self.model().insertRow(aimRow)
        newIndex = self.model().index(aimRow)
        self.model().setData(newIndex, text)

        if aimRow < sorRow:
            self.model().removeRow(sorRow + 1)
        else:
            self.model().removeRow(sorRow)


class sortElementDialog(QDialog):
    def __init__(self, parent = None):
        super(sortElementDialog, self).__init__(parent)
        self._buttonWidget = QWidget(self)
        self._bLoadFromFile = QPushButton("从文件载入", self._buttonWidget)
        self._editLine = QLineEdit("", self._buttonWidget)
        self._recompile = QtGui.QRegularExpressionValidator("[\w\.]*", self._editLine)
        self._editLine.setValidator(self._recompile)
        self._bAdd = QPushButton("添加", self._buttonWidget)
        self._bDelete = QPushButton("删除", self._buttonWidget)
        self._bSave = QPushButton("保存", self._buttonWidget)
        self._spacerItem = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Fixed);
        self._buttonLayout = QHBoxLayout(self._buttonWidget)

        self._bLoadFromFile.clicked.connect(self.loadFromSelectFile)
        self._bAdd.clicked.connect(self.add)
        self._bDelete.clicked.connect(self.delete)
        self._bSave.clicked.connect(self.saveAndExit)


        self._buttonLayout.addWidget(self._editLine)
        self._buttonLayout.addWidget(self._bAdd)
        self._buttonLayout.addSpacerItem(self._spacerItem)
        self._buttonLayout.addWidget(self._bDelete)
        self._buttonLayout.addWidget(self._bLoadFromFile)
        self._buttonLayout.addWidget(self._bSave)
        self._buttonWidget.setLayout(self._buttonLayout)

        self._listView = MyDrapListView(self)
        self._listModel = QtCore.QStringListModel()
        self._listView.setDropIndicatorShown(True)
        self._listView.setDefaultDropAction(QtCore.Qt.MoveAction)
        self._listView.setDragEnabled(True)
        self._listView.setAcceptDrops(True)
        self._listView.setDragDropMode(QListView.InternalMove)
        #QListView.inter
        
        #self._listView.setDragDropOverwriteMode(True)
        #self._listView.viewport().setAcceptDrops(True)

        self._listView.setModel(self._listModel)

        self._itemDict = {}

        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.addWidget(self._listView)
        self._mainLayout.addWidget(self._buttonWidget)

        self.setLayout(self._mainLayout)

    def isHasElement(self, path):
        print(path)
        return (path in self._itemDict.keys())

    def delete(self):
        index = self._listView.currentIndex()

        if index.row() == -1:
            return

        text = self._listModel.data(index, QtCore.Qt.DisplayRole)
        self._itemDict.pop(text)
        self._listModel.removeRow(index.row())

    def add(self):
        text = self._editLine.text()
        if text == "":
            return
        if self.isHasElement(text):
            return
        print("addd")
        self._itemDict[text] = 99
        self.addListData(text)
        self._editLine.setText("")

    def saveAndExit(self):
        maxRowCount = self._listModel.rowCount()
        elementList = []
        for row in range(maxRowCount):
            index = self._listModel.index(row)
            elementList.append(self._listModel.data(index, QtCore.Qt.DisplayRole))
        TranslateCore.instance.applyDefaultElement(elementList)
        self.hide()


    def loadFromSelectFile(self):
        #path = QFileDialog(self, "选择汉化元素文件", ".", )
        path = QFileDialog.getOpenFileName(self, "选择汉化元素文件", ".", "*.json")
        if path[0] == '':
            return
        fileElementList = TranslateCore.instance.getElementFromFile(path[0])
        for var in fileElementList:
            if not self.isHasElement(var):
                self._itemDict[var] = 99
                self.addListData(var)

    def showSortElementDialog(self):
        self._itemDict = TranslateCore.instance.getDefautlSelectElement()
        print(self._itemDict)

        tempList = self._itemDict.keys()
        sorted(tempList, key=lambda x:self._itemDict[x])

        self._listModel.removeRows(0, self._listModel.rowCount())

        for var in tempList:
            self.addListData(var)

        self.show()

    def addListData(self, content):
        row = self._listModel.rowCount()
        self._listModel.insertRow(row)
        index = self._listModel.index(row)
        self._listModel.setData(index, content)


class selectElementDialog(QDialog):
    def __init__(self, parent = None):
        super(selectElementDialog, self).__init__(parent)

        self._sortDict = {}



        self._buttonWidget = QWidget(self)
        #self._bMoveLeft = QPushButton("<<", self)
        #self._bMOveRight = QPushButton(">>", self)
        self._bSaveAndClose = QPushButton("保存", self._buttonWidget)

        self._buttonLayout = QHBoxLayout(self._buttonWidget)
        #self._buttonLayout.addWidget(self._bMoveLeft)
        #self._buttonLayout.addWidget(self._bMOveRight)
        self._buttonLayout.addWidget(self._bSaveAndClose)
        self._buttonWidget.setLayout(self._buttonLayout)

        self._bSaveAndClose.clicked.connect(self.dealSaveAndClose)
        
        self._listViewWidget = QWidget(self)
        self._listViewNotSelect = QListView(self._listViewWidget)
        self._listViewSetect = QListView(self._listViewWidget)
        self._modelNotSelect = QtGui.QStandardItemModel(0, 1, self)
        self._modelSelect = QtGui.QStandardItemModel(0, 1, self)
        self.configListView()

        
        self._listViewLayout = QHBoxLayout(self._listViewWidget)
        self._listViewLayout.addWidget(self._listViewNotSelect)
        self._listViewLayout.addWidget(self._listViewSetect)
        self._listViewWidget.setLayout(self._listViewLayout)

        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.addWidget(self._listViewWidget)
        self._mainLayout.addWidget(self._buttonWidget)

        self.setLayout(self._mainLayout)

        self.setMinimumSize(680, 870)

    def configListView(self):
        self._listViewNotSelect.setModel(self._modelNotSelect)
        self._listViewSetect.setModel(self._modelSelect)
        self._listViewNotSelect.clicked.connect(self.addToSelect)
        self._listViewSetect.clicked.connect(self.removeFromSelect)

    def addNotSelectListData(self, str, weight):
        row = self._modelNotSelect.rowCount()
        self._modelNotSelect.insertRow(row)
        index = self._modelNotSelect.index(row, 0)
        self._modelNotSelect.setData(index, str)
        self._modelNotSelect.setData(index, weight, QtCore.Qt.UserRole)

    def addSelectListData(self, str, weight):
        row = self._modelSelect.rowCount()
        self._modelSelect.insertRow(row)
        index = self._modelSelect.index(row, 0)
        self._modelSelect.setData(index, str)
        self._modelSelect.setData(index, weight, QtCore.Qt.UserRole)

    def showSelectElementDialog(self, selectPath):

        self._modelNotSelect.removeRows(0, self._modelNotSelect.rowCount())
        self._modelSelect.removeRows(0, self._modelSelect.rowCount())


        self._sortDict = TranslateCore.instance.getDefautlSelectElement()
        self._selectPath =  TranslateCore.instance.getRelativePath(selectPath)
        selectElement = TranslateCore.instance.getSelectElement(self._selectPath)
        print(selectElement)

        NotselectElement = set(self._sortDict.keys()) - set(selectElement)

        for var in NotselectElement:
            if var in self._sortDict.keys():
                self.addNotSelectListData(var, self._sortDict[var])
            else:
                raise KeyError()

        for var in selectElement:
            if var in self._sortDict.keys():
                self.addSelectListData(var, self._sortDict[var])
            else:
                raise KeyError()

        #self._modelNotSelect
        self._modelNotSelect.setSortRole(QtCore.Qt.UserRole)
        self._modelSelect.setSortRole(QtCore.Qt.UserRole)
        self._modelNotSelect.sort(0)
        self._modelSelect.sort(0)

        self.show()

    def addToSelect(self):
        index = self._listViewNotSelect.currentIndex()
        if -1 == index.row():
            return
        self.addSelectListData(index.data(QtCore.Qt.DisplayRole), index.data(QtCore.Qt.UserRole))
        print(index.data(QtCore.Qt.DisplayRole))
        self._modelNotSelect.removeRow(index.row())
        self._modelSelect.sort(0)

    def removeFromSelect(self):
        index = self._listViewSetect.currentIndex()
        if -1 == index.row():
            return   
        self.addNotSelectListData(index.data(QtCore.Qt.DisplayRole), index.data(QtCore.Qt.UserRole))
        print(index.data(QtCore.Qt.DisplayRole))
        self._modelSelect.removeRow(index.row())
        self._modelNotSelect.sort(0)


    def dealSaveAndClose(self):
        selectElements = []

        for row in range(self._modelSelect.rowCount()):
            index = self._modelSelect.index(row, 0)
            selectElements.append(self._modelSelect.data(index, QtCore.Qt.DisplayRole))
        #return selectElements
        TranslateCore.instance.setNewSelectElements(self._selectPath, selectElements)
        self.hide()
        


class configDialog(QDialog):
    def __init__(self, parent=None):
        super(configDialog, self).__init__(parent)
        self._lModPath = QLabel("mod路径:", self)
        self._lhuanHuaInputPath = QLabel("译文路径:", self)
        self._ldistModPath = QLabel("汉化生成路径:", self)

        pathList = TranslateCore.instance.getPaths()
        self._lModPathP = QLabel(pathList[0], self)
        self._lhuanHuaInputPathP = QLabel(pathList[1], self)
        self._ldistModPathP = QLabel(pathList[2], self)

        self._lModPath.setAlignment(QtCore.Qt.AlignLeft)
        self._lhuanHuaInputPath.setAlignment(QtCore.Qt.AlignLeft)
        self._ldistModPath.setAlignment(QtCore.Qt.AlignLeft)

        self._lModPathP.setAlignment(QtCore.Qt.AlignLeft)
        self._lhuanHuaInputPathP.setAlignment(QtCore.Qt.AlignLeft)
        self._ldistModPathP.setAlignment(QtCore.Qt.AlignLeft)

        self._bModPathP = QPushButton("配置", self)
        self._bhuanHuaInputPathP = QPushButton("配置", self)
        self._bdistModPathP = QPushButton("配置", self)

        self._bModPathP.clicked.connect(self.setModPath)
        self._bhuanHuaInputPathP.clicked.connect(self.setHuanHuaInputPath)
        self._bdistModPathP.clicked.connect(self.setDistModPath)

        self._hlayout = QHBoxLayout(self)

        self._widgets1 = QWidget(self)
        self._widgets2 = QWidget(self)
        self._widgets3 = QWidget(self)

        self._lLabelList1 = QVBoxLayout(self._widgets1)
        self._lLabelList2 = QVBoxLayout(self._widgets2)
        self._lLabelList3 = QVBoxLayout(self._widgets3)



        self._lLabelList1.addWidget(self._lModPath)
        self._lLabelList1.addWidget(self._lhuanHuaInputPath)
        self._lLabelList1.addWidget(self._ldistModPath)

        self._lLabelList2.addWidget(self._lModPathP)
        self._lLabelList2.addWidget(self._lhuanHuaInputPathP)
        self._lLabelList2.addWidget(self._ldistModPathP)

        self._lLabelList3.addWidget(self._bModPathP)
        self._lLabelList3.addWidget(self._bhuanHuaInputPathP)
        self._lLabelList3.addWidget(self._bdistModPathP)

        self._widgets1.setLayout(self._lLabelList1)
        self._widgets1.setLayout(self._lLabelList2)
        self._widgets1.setLayout(self._lLabelList3)

        self._hlayout.addWidget(self._widgets1)
        self._hlayout.addWidget(self._widgets2)
        self._hlayout.addWidget(self._widgets3)


        self.setLayout(self._hlayout)

    def setPathContent(self, modPath, huanHuaInputPath, distModPath):
        self._lModPathP.setText(modPath)
        self._lhuanHuaInputPathP.setText(huanHuaInputPath)
        self._ldistModPathP.setText(distModPath)

    def setModPath(self):
        path = QFileDialog.getExistingDirectory(self, "选择路径", self._lModPathP.text(), QFileDialog.ShowDirsOnly)
        self._lModPathP.setText(path)
        TranslateCore.instance.saveModPath(path)

    def setHuanHuaInputPath(self):
        path = QFileDialog.getExistingDirectory(self, "选择路径", self._lhuanHuaInputPathP.text(), QFileDialog.ShowDirsOnly)
        self._lhuanHuaInputPathP.setText(path)
        TranslateCore.instance.saveHuanHuaInputPath(path)

    def setDistModPath(self):
        path = QFileDialog.getExistingDirectory(self, "选择路径", self._lhuanHuaInputPathP.text(), QFileDialog.ShowDirsOnly)
        self._ldistModPathP.setText(path)
        TranslateCore.instance.saveDistModPath(path)


class myWindow(QDialog):
    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)
        TranslateCore()
        TranslateCore.instance.init()

        self.__dirModel = QFileSystemModel()
        self.__dirTreeView = QTreeView(self)
        self.__configSelectElementDialog = sortElementDialog(self)
        
        
        self.setTreeeView()
        

        self._configDialog = configDialog(self)
        self._selectElementDialog = selectElementDialog(self)
        self._bConfingPath = QPushButton("配置文件路径", self)
        self._bDefaultElement = QPushButton("配置默认元素", self)
        self._bGetTranslateFiles = QPushButton("获取中间汉化文件", self)
        self._bGetFinalFiles = QPushButton("获取汉化文件", self)

        self._bGetTranslateFiles.clicked.connect(TranslateCore.instance.getTranslateFiles)
        self._bDefaultElement.clicked.connect(self.__configSelectElementDialog.showSortElementDialog)
        self._bConfingPath.clicked.connect(self.showConfigDialog)
        self._bGetFinalFiles.clicked.connect(TranslateCore.instance.getFinalFiles)

        self._buttonWidget = QWidget(self)
        self._vButtonListLayout = QVBoxLayout(self._buttonWidget)
        self._buttonWidget.setLayout(self._vButtonListLayout)

        self._hMainLayout = QHBoxLayout(self)
        self._hMainLayout.addWidget(self._buttonWidget)
        self._hMainLayout.addWidget(self.__dirTreeView)

        #button
        self._vButtonListLayout.addWidget(self._bConfingPath)
        self._vButtonListLayout.addWidget(self._bDefaultElement)
        self._vButtonListLayout.addWidget(self._bGetTranslateFiles)
        self._vButtonListLayout.addWidget(self._bGetFinalFiles)

        self.setLayout(self._hMainLayout)
        
        self.setMinimumSize(1200, 900)


    def setTreeeView(self):
        path = TranslateCore.instance.getModPath()
        print(path)
        self.__dirModel.setRootPath(path)
        self.__dirModel.setFilter(QtCore.QDir.Dirs|QtCore.QDir.NoDotAndDotDot)

        self.__dirTreeView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.__dirTreeView.setModel(self.__dirModel)
        self.__dirTreeView.setRootIndex(self.__dirModel.index(path))
        self.__dirTreeView.setColumnHidden(1, True)
        self.__dirTreeView.setColumnHidden(2, True)
        self.__dirTreeView.setColumnHidden(3, True)
        self.__dirTreeView.setColumnWidth(0, 70)
        self.__dirTreeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.__dirTreeView.customContextMenuRequested.connect(self.showTreeRightMenu)
        
        self.__treeMenu = QMenu(self)
        self.__treeConfig = self.__treeMenu.addAction("修改配置")
        self.__treeMark = self.__treeMenu.addAction("标记输出")
        self.__treeUnMark = self.__treeMenu.addAction("移除标记")
        self.__treeMarkExcept = self.__treeMenu.addAction("标记除外")

        self.__treeConfig.triggered.connect(self.dealTreeConfig)
        self.__treeMark.triggered.connect(self.dealTreeMark)
        self.__treeUnMark.triggered.connect(self.dealTreeUnMark)
        self.__treeMarkExcept.triggered.connect(self.dealTreeMarkExcept)


    def dealTreeConfig(self):
        index = self.__dirTreeView.currentIndex()
        path = self.__dirModel.filePath(index)
        #TranslateCore.instance.configPath(path)
        self._selectElementDialog.showSelectElementDialog(path)

    def dealTreeMark(self):
        index = self.__dirTreeView.currentIndex()
        path = self.__dirModel.filePath(index)
        TranslateCore.instance.treeMark(path)

    def dealTreeUnMark(self):
        index = self.__dirTreeView.currentIndex()
        path = self.__dirModel.filePath(index)
        TranslateCore.instance.treeUnMark(path)

    def dealTreeMarkExcept(self):
        index = self.__dirTreeView.currentIndex()
        path = self.__dirModel.filePath(index)
        TranslateCore.instance.treeUnMark(path)

    def showTreeRightMenu(self, pos):
        index = self.__dirTreeView.currentIndex()
        path = self.__dirModel.filePath(index)
        rank = TranslateCore.instance.getElementRank(path)
        isShowMark = not TranslateCore.instance.isMarked(path)
        
        if rank > 1:
            self.__treeMark.setVisible(False)
            self.__treeUnMark.setVisible(False)
            self.__treeMarkExcept.setVisible(True)
        else:
            self.__treeMark.setVisible(True)
            self.__treeUnMark.setVisible(True)
            if isShowMark:
                self.__treeMark.setEnabled(True)
                self.__treeUnMark.setEnabled(False)
            else:
                self.__treeMark.setEnabled(False)
                self.__treeUnMark.setEnabled(True)

            self.__treeMarkExcept.setVisible(False)


        self.__treeMenu.move(QtGui.QCursor().pos())
        self.__treeMenu.show()




    def showConfigDialog(self):
        self._configDialog.show()

    




