# -*- coding: utf-8 -*-
from ast import Lambda
from inspect import getmodule
from msilib import Directory
import os
import json
from collections import OrderedDict
import shutil
from types import CodeType
from typing import Dict
#from enum import Enum
from enum import IntEnum
from myDatabase import MyDatabase
from myConfig import MyConfig


########################################################################
##############################转移汉化
huanHuaPath = "G:/GitBin/private-file-storage/game/battleTech/BattleTechProject/BattleTech/zh-CN/newCore/CustomLocalization/Localization/RogueTech/RU"
huanHuaMap = {}
def filltempMap():

    count = 0
    for root, dirs, files in os.walk(huanHuaPath):
        for fileH in files:
            if fileH.endswith(".json"):
                fhuanPath = os.path.join(root, fileH)
                
                with open(fhuanPath, mode="r", encoding="utf-8") as ffh:
                    Jfh = json.load(ffh, object_pairs_hook=OrderedDict)
                    testFlag = True
                    #print(fhuanPath)
                    for eum in Jfh:
                        huanHuaMap[eum["id"]] = eum["content"]
                        if testFlag == True:
                            testFlag = False
                            #print(eum["id"])
                            #print(eum["content"])
                            #print(huanHuaMap[eum["id"]])
                        count +=1
    print("转换", count, "条")

#######################################################################





def loadJson(fileName):
    tempJson = None
    try:
        with open(fileName, "r", encoding="utf-8") as f:
            tempJson = json.load(f, object_pairs_hook=OrderedDict)
    except:
        print(fileName)
        input()
    return tempJson


def getMechEngineSetting (dealList, selectElement, baseFileName):

    selectRanEelem = selectElement.split(".")
    cotentList = []
    if "Settings" in dealList:
        for var in dealList["Settings"]:
            elemId = ""
            if "Bonus" not in var or selectRanEelem[2] not in var:
                continue

            elemId =  var["Bonus"]
            keyId = '.'.join((selectRanEelem[0], elemId, selectRanEelem[2]))

            content = var[selectRanEelem[2]]

            cotentList.append((keyId, content))

    return cotentList

def getSettingMechEngineEffect (dealList, selectElement, baseFileName):

    selectRanEelem = selectElement.split(".")
    cotentList = []
    if selectRanEelem[0] in dealList:
        for var in dealList[selectRanEelem[0]]:
            if selectRanEelem[1] not in var:
                continue

            Description = var[selectRanEelem[1]]
            if "Id" not in Description or selectRanEelem[2] not in Description:
                continue

            keyId = '.'.join((baseFileName, Description["Id"], "effect", selectRanEelem[2]))
            content = Description[selectRanEelem[2]]
            cotentList.append((keyId, content))

    return cotentList


def getOptionsDescription(dealList, selectElement, baseFileName):
    selectRanEelem = selectElement.split(".")
    cotentList = []
    if selectRanEelem[0] in dealList:   
        for var in dealList[selectRanEelem[0]]:
            if selectRanEelem[1] not in var:
                continue

            Description = var[selectRanEelem[1]]
            if "Id" not in Description or selectRanEelem[2] not in Description:
                continue

            Did = Description["Id"]
            index = Did.find('_')
            numStr = Did[index + 1:].replace('_', '.')
            keyId = '.'.join((baseFileName, Did, selectRanEelem[0] + numStr, selectRanEelem[2]))
            content = Description[selectRanEelem[2]]
            cotentList.append((keyId, content))
    return cotentList

def getObjectiveList(dealList, selectElement, baseFileName):
    selectRanEelem = selectElement.split(".")
    cotentList = []
    if selectRanEelem[0] in dealList:   
        for var in enumerate(dealList[selectRanEelem[0]]):
            if selectRanEelem[1] not in var[1]:
                continue

            keyId = '.'.join((baseFileName, selectRanEelem[0] + str(var[0]), selectRanEelem[1]))
            content = var[1][selectRanEelem[1]]
            cotentList.append((keyId, content))
    return cotentList

def getDialogueListdialogueContentWords(dealList, selectElement, baseFileName):
    selectRanEelem = selectElement.split(".")
    cotentList = []
    if selectRanEelem[0] in dealList:   
        for outvar in enumerate(dealList[selectRanEelem[0]]):
            if selectRanEelem[1] not in outvar[1]:
                continue
            for var in enumerate(outvar[1][selectRanEelem[1]]):
                if selectRanEelem[2] not in var[1]:
                    continue

                keyId = '.'.join((baseFileName, selectRanEelem[0] + str(outvar[0]), selectRanEelem[1] + str(var[0]), selectRanEelem[2]))
                content = var[1][selectRanEelem[2]]
                cotentList.append((keyId, content))
    return cotentList



def getOptionsResultSetsDescription(dealList, selectElement, baseFileName):
    selectRanEelem = selectElement.split(".")
    cotentList = []

    if selectRanEelem[0] in dealList:
        for outvar in dealList[selectRanEelem[0]]:
            if selectRanEelem[1] in outvar:
                for var in outvar[selectRanEelem[1]]:
                    if selectRanEelem[2] not in var:
                        continue
                    #print(var)
                    Description = var[selectRanEelem[2]]
                    if "Id" not in Description or selectRanEelem[3] not in Description:
                        continue

                    Did = Description["Id"]
                    index = Did.find('_')
                    numStr = Did[index + 1:].replace('_', '.')
                    keyId = '.'.join((baseFileName, Did, selectRanEelem[0] + numStr, selectRanEelem[3]))
                    content = Description[selectRanEelem[3]]
                    cotentList.append((keyId, content))
    return cotentList



def getStatusEffectsDescription(dealList, selectElement, baseFileName):
    selectRanEelem = selectElement.split(".")
    cotentList = []

    if selectRanEelem[0] in dealList and dealList[selectRanEelem[0]] is not None:   
        for var in enumerate(dealList[selectRanEelem[0]]):
            if selectRanEelem[1] not in var[1]:
                continue
            Description = var[1][selectRanEelem[1]]
            if "Id" not in Description or selectRanEelem[2] not in Description:
                continue

            Did = Description["Id"]

            keyId = '.'.join((baseFileName, Did,selectRanEelem[0] + str(var[0]), selectRanEelem[2]))
            content = Description[selectRanEelem[2]]
            cotentList.append((keyId, content))


    return cotentList

def getCustomActivatableComponent(dealList, selectElement, baseFileName):
    selectRanEelem = selectElement.split(".")
    cotentList = []
    if selectRanEelem[0] in dealList and selectRanEelem[1] in dealList[selectRanEelem[0]] and selectRanEelem[2] in dealList[selectRanEelem[0]][selectRanEelem[1]]:
        for var in enumerate(dealList[selectRanEelem[0]][selectRanEelem[1]][selectRanEelem[2]]):
            if selectRanEelem[3] not in var[1]:
                continue
            Description = var[1][selectRanEelem[3]]
            if "Id" not in Description or selectRanEelem[4] not in Description:
                continue

            Did = Description["Id"]

            keyId = '.'.join((baseFileName, Did,"CAE" + str(var[0]), selectRanEelem[4]))
            content = Description[selectRanEelem[4]]
            cotentList.append((keyId, content))

    return cotentList

def getDeferredEffectDtatusEffectsDescription(dealList, selectElement, baseFileName):
    selectRanEelem = selectElement.split(".")
    cotentList = []
    if selectRanEelem[0] in dealList and selectRanEelem[1] in dealList[selectRanEelem[0]]:
        for var in enumerate(dealList[selectRanEelem[0]][selectRanEelem[1]]):
            if selectRanEelem[2] not in var[1]:
                continue
            Description = var[1][selectRanEelem[2]]
            if "Id" not in Description or selectRanEelem[3] not in Description:
                continue

            Did = Description["Id"]

            keyId = '.'.join((baseFileName, Did + str(var[0]), selectRanEelem[3]))
            content = Description[selectRanEelem[3]]
            cotentList.append((keyId, content))

    return cotentList


def getObjectiveList(dealList, selectElement, baseFileName):
    selectRanEelem = selectElement.split(".")
    cotentList = []
    if selectRanEelem[0] in dealList:   
        for var in enumerate(dealList[selectRanEelem[0]]):
            if selectRanEelem[1] not in var[1]:
                continue

            keyId = '.'.join((baseFileName, selectRanEelem[0] + str(var[0]), selectRanEelem[1]))
            content = var[1][selectRanEelem[1]]
            cotentList.append((keyId, content))
    return cotentList

def getDialogueListdialogueContentWords(dealList, selectElement, baseFileName):
    selectRanEelem = selectElement.split(".")
    cotentList = []
    if selectRanEelem[0] in dealList:   
        for outvar in enumerate(dealList[selectRanEelem[0]]):
            if selectRanEelem[1] not in outvar[1]:
                continue
            for var in enumerate(outvar[1][selectRanEelem[1]]):
                if selectRanEelem[2] not in var[1]:
                    continue

                keyId = '.'.join((baseFileName, selectRanEelem[0] + str(outvar[0]), selectRanEelem[1] + str(var[0]), selectRanEelem[2]))
                content = var[1][selectRanEelem[2]]
                cotentList.append((keyId, content))
    return cotentList

selectMethodMap = {"MechEngineer.Settings.Full":getMechEngineSetting,
                   "MechEngineer.Settings.Long":getMechEngineSetting,
                   "MechEngineer.Settings.Short":getMechEngineSetting,
                   "Settings.Description.Details":getSettingMechEngineEffect,
                   "Settings.Description.Name":getSettingMechEngineEffect,
                   "Options.Description.Details":getOptionsDescription,
                   "Options.Description.Name":getOptionsDescription,
                   "Options.ResultSets.Description.Details":getOptionsResultSetsDescription,
                   "Options.ResultSets.Description.Name":getOptionsResultSetsDescription,
                   "objectiveList.description":getObjectiveList,
                   "objectiveList.title":getObjectiveList,
                   "dialogueList.dialogueContent.words":getDialogueListdialogueContentWords,
                   "statusEffects.Description.Details":getStatusEffectsDescription,
                   "statusEffects.Description.Name":getStatusEffectsDescription,
                   "Custom.ActivatableComponent.statusEffects.Description.Details":getCustomActivatableComponent,
                   "Custom.ActivatableComponent.statusEffects.Description.Name":getCustomActivatableComponent,
                   "Custom.ActivatableComponent.offlineStatusEffects.Description.Details":getCustomActivatableComponent,
                   "Custom.ActivatableComponent.offlineStatusEffects.Description.Name":getCustomActivatableComponent,
                   "deferredEffect.statusEffects.Description.Details":getDeferredEffectDtatusEffectsDescription,
                   "deferredEffect.statusEffects.Description.Name":getDeferredEffectDtatusEffectsDescription,
                   "EffectData.Description.Details":getStatusEffectsDescription,
                   "EffectData.Description.Name":getStatusEffectsDescription,
                   "effectData.Description.Details":getStatusEffectsDescription,
                   "effectData.Description.Name":getStatusEffectsDescription,
                   }

def getDeepContent(orgdict, selectElement, baseFileName):
    
    if selectElement in selectMethodMap:
        return selectMethodMap[selectElement](orgdict, selectElement, baseFileName)
    else:
        tempDict = orgdict
        keyId = None
        try:
            for select in selectElement.split("."): 
                if not isinstance(tempDict, Dict):
                    raise TypeError()

                if select not in tempDict:
                    return []
                tempDict = tempDict[select]
            keyId = baseFileName + "." + selectElement

        except TypeError as err:
            print('*' * 40)
            print(selectElement)
            print(baseFileName)
            print('*' * 40)
            raise err

        return [(keyId, tempDict)]


def getNormalEum(jsonObj, filename, selects = None, realSelectElements=None, distBuffer=None):
    #print(filename)

    baseFile = filename.split('.')[0]
    isHasContent = False
    for eum in selects:

        eumValueList = getDeepContent(jsonObj, eum, baseFile)

        for eumValue in eumValueList:
            if len(eumValue) > 0:
                if eumValue[1] == "":
                    continue
                tempId = eumValue[0]
                tempInnerDict = OrderedDict()
                tempInnerDict["id"] = tempId
                tempInnerDict["original"] = eumValue[1]


                tempInnerDict["prevOriginal"] = eumValue[1]

                #导出汉化
                if tempId in huanHuaMap:
                    tempInnerDict["content"] = huanHuaMap[tempId]
                    #print(baseFile)
                    input("inmsdfsdf")
                else:
                    tempInnerDict["content"] = eumValue[1]

                #tempInnerDict["content"] =  tempId
                tempInnerDict["localizatorComment"] = ""
                tempInnerDict["systemComment"] = ""
                tempInnerDict["backColor"] = "#FFFFFF"
                tempInnerDict["textColor"] = "#000000"
                tempInnerDict["filename"] = baseFile
                tempInnerDict["processor"] = eum
                isHasContent = True
                realSelectElements.add(eum)
                distBuffer["content"].append(tempInnerDict)
    if isHasContent:
        distBuffer["files"].append(filename)
    return isHasContent

class transFileDict(OrderedDict):
    def __init__(self):
        self["culture"] = 2
        self["files"] = []
        self["directories"] = []
        self["content"] = []


class UpdateMode(IntEnum):
    NO = 0
    INSERT = 1
    UPDATE = 2

class FileMode(IntEnum):
    NOT = 0
    MODEL_MIN = 1
    MODEL_MID = 2
    MODEL_MAX = 3

class MaxinUpdateMode(object):
    @property
    def updateMode(self):
        return self.__updateMode

    @updateMode.setter
    def updateMode(self, mode):
        if not isinstance(mode, UpdateMode):
            raise TypeError()
        self.__updateMode = mode

class MarkPathElement(MaxinUpdateMode):
    def __init__(self, fileMode, updateMode = UpdateMode.NO):
        if not isinstance(updateMode, UpdateMode):
            raise TypeError()
        self.__fileMode = fileMode
        self.updateMode = updateMode

    @property
    def fileMode(self):
        return self.__fileMode

    @fileMode.setter
    def fileMode(self, mode):
        if not isinstance(mode, FileMode):
            raise TypeError()
        self.__fileMode = mode





class MarkPath(Dict):
    
    def __init__(self, *args, **kwargs):
        super(MarkPath, self).__init__(*args, **kwargs)

    def getFromDatabase(self):
        for var in MyDatabase.instance.getMarkPath():
            self[var[0]] = MarkPathElement(FileMode(var[1]), UpdateMode.NO)

    def save(self):
        for key, value in self.items():
            if value.updateMode == UpdateMode.No:
                continue
            elif value.updateMode == UpdateMode.INSERT:
                MyDatabase.instance.insertMarkPath(key, int(value.fileMode))
            else:
                MyDatabase.instance.updateMarkPath(key, int(value.fileMode))

    def setMark(self, path, fileMode = FileMode.NOT):
        if path in self:
            MyDatabase.instance.updateMarkPath(path, int(fileMode)) 
        else:
            MyDatabase.instance.insertMarkPath(path, int(fileMode))
        self[path] = MarkPathElement(fileMode) 

    def __str__(self):
        tempStr = ("*" * 40) + "MarkPath" + ("*" * 40)
        for key,value in self.items():
            tempStr += f"{key} : {value.fileMode}\n"
        tempStr += "\n\n"
        return tempStr






class TranslateCore(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args)
        return cls.instance

    def __init__(self):
        MyConfig()
        MyDatabase()
        self.__markPath = MarkPath()
        self.__markPath.getFromDatabase()
        self.__defaultSelectElement = {key:value for key,value in MyDatabase.instance.getDefaultSelectEum()}
        self.__dictSelctElement = {key:json.loads(value.replace("##", "\"")) for key,value in MyDatabase.instance.getDictSelectElement()}

        

    def init(self):
        pass   
    #MyConfig().midModPath
   
    def makeMidFanYi(self):
        if os.path.exists(MyConfig.instance.huanHuaOutputPath):
            shutil.rmtree(MyConfig.instance.huanHuaOutputPath)
        for root, _, files in os.walk(MyConfig.instance.midModPath):
            for file in files:
                if file.endswith(".json"):
                    oldPath = os.path.join(root, file)
                    newPath = os.path.join(MyConfig.instance.huanHuaOutputPath, os.path.relpath(oldPath, MyConfig.instance.midModPath))
                    distStr = []
                    newDir = os.path.join(MyConfig.instance.huanHuaOutputPath, os.path.relpath(root, MyConfig.instance.midModPath))
                    if not os.path.exists(newDir):
                        os.makedirs(newDir)
                    if(file == "LocalizationDef.json"):
                        with open(oldPath, mode="r", encoding="utf-8") as f:

                            jsStr = json.load(f, object_pairs_hook=OrderedDict)
                            for eum in jsStr["content"]:
                                tempStr = OrderedDict()
                                try:
                                    tempStr["id"] = eum["id"]
                                    tempStr["content"] = eum["original"]
                                except KeyError:
                                    print(oldPath)
                                    print(eum)
                                distStr.append(tempStr)
                            print(newPath)
                            with open(newPath, mode="w", encoding="utf-8") as outfile:
                                outfile.write(json.dumps(distStr, indent=4))
                    else:
                        shutil.copy(oldPath, newPath)

    def getTranslateFiles(self):#生成中间翻译文件
        #filltempMap()

        #清理中间文件目录
        if os.path.exists(MyConfig.instance.midModPath):
            shutil.rmtree(MyConfig.instance.midModPath)

        #print(MyConfig.instance.modPath)


        for dealPath, isOutput in self.__markPath.items():
            if isOutput.fileMode == FileMode.MODEL_MIN:
                absDealPath = os.path.join(MyConfig.instance.modPath, dealPath)
                #print(absDealPath)
                if os.path.isdir(absDealPath):
                    self.dealInnerDir(absDealPath, dealPath)

        self.makeMidFanYi()

        print("finished!!!!!")

    def dealInnerDir(self,absDealPath,dealPath=""):
        for innerDir in os.listdir(absDealPath):
            innerPath = os.path.join(absDealPath, innerDir)
            #print(outDir, innerDir)
            #@TODO 实现排除目录

            if os.path.isdir(innerPath):
                midFileJsonBuffer = transFileDict()

                isMakeFile = False
                realSelectElement = set()

                for root, _, files in os.walk(innerPath):
                    for cFile in files:
                        if cFile.endswith(".json") and cFile != "Localization.json" and cFile != "mod.json":
                            cFilePath = os.path.join(root, cFile)

                            pathKey = os.path.relpath(root, MyConfig.instance.modPath)

                            currentSelectElement = self.getSelectReleaxElement(pathKey)
                            currentSelectElement = sorted(currentSelectElement, key=self.getElementWeigth)

                            if len(currentSelectElement) > 0 and getNormalEum(loadJson(cFilePath), cFile, currentSelectElement, realSelectElement,midFileJsonBuffer):
                                isMakeFile = True

                if isMakeFile:
                    realElementList = sorted(realSelectElement, key=self.getElementWeigth)
                    midFileJsonBuffer["directories"].append({"dir":[dealPath, innerDir], "processors":realElementList})
                    distDir = os.path.join(MyConfig.instance.midModPath, dealPath, innerDir)
                    distFilePath = os.path.join(distDir, "LocalizationDef.json")
                    print("output:", distFilePath)
                    if not os.path.exists(distDir):
                        os.makedirs(distDir)
                    with open(distFilePath, mode="w", encoding="utf-8") as locf:
                        locf.write(json.dumps(midFileJsonBuffer, indent=4, ensure_ascii=False))
    
    def getElementWeigth(self, key):
        if key in self.__defaultSelectElement:
            return self.__defaultSelectElement[key]
        else:
            raise ValueError()

    def getSelectReleaxElement(self, pathKey): #会根据路径一次向上级目录查找

        if pathKey in self.__dictSelctElement:
            return self.__dictSelctElement[pathKey]
        else:
            return []


        #############查询上级目录的作为替代,不使用
        rank = pathKey.split("\\")
        
        rankNum = len(rank)

        while rankNum > 0:
            selectKey = ""
            if rankNum == 0:
                selectKey = rank[0]
            else:
                selectKey = os.path.join(*rank[0:rankNum])

            if selectKey in self.__dictSelctElement:
                return self.__dictSelctElement[selectKey]

            rankNum -= 1

        return []
    
    def getPaths(self):
        tempV = MyConfig.instance.modPath
        if tempV is None:
            tempV = ""
        return tempV, MyConfig.instance.huanHuaInputPath ,MyConfig.instance.distModPath

    def getModPath(self):
        return MyConfig.instance.modPath

    def saveModPath(sefl, path):
        MyConfig.instance.modPath = path
        MyConfig.instance.save()

    def saveHuanHuaInputPath(sefl, path):
        MyConfig.instance.huanHuaInputPath = path
        MyConfig.instance.save()

    def saveDistModPath(sefl, path):
        MyConfig.instance.distModPath = path
        MyConfig.instance.save()

    def getRelativePath(self, path):
        return os.path.relpath(path, MyConfig.instance.modPath)

    def getElementRank(self, path):
        return len(self.getRelativePath(path).split('\\'))

    def treeMark(self, selectPath):
        rpath = os.path.relpath(selectPath, MyConfig.instance.modPath)
        self.__markPath.setMark(rpath, FileMode.MODEL_MIN)
    def isMarked(self, selectPath):
        rpath = os.path.relpath(selectPath, MyConfig.instance.modPath)
        markFlag = False
        #print(self.__markPath)
        if rpath in self.__markPath and self.__markPath[rpath].fileMode == FileMode.MODEL_MIN:
            markFlag = True
        #print(markFlag)
        return markFlag

    def treeUnMark(self, selectPath):
        rpath = os.path.relpath(selectPath, MyConfig.instance.modPath)
        self.__markPath.setMark(rpath)

    def getDefautlSelectElement(self):
        return self.__defaultSelectElement.copy()


    def getElementFromFile(self, path):
        tempJson = []
        with open(path, "r", encoding="utf-8") as f:
            tempJson = json.load(f)
        return tempJson

    def applyDefaultElement(self, elemList):
        #print(elemList)
        self.__defaultSelectElement.clear()
        for var in enumerate(elemList):
            self.__defaultSelectElement[var[1]] = var[0]

        MyDatabase.instance.setDefaultSelectEum([(key, weight) for key, weight in self.__defaultSelectElement.items()])

    def getSelectElement(self, rPath):
        if rPath in self.__dictSelctElement:
            return self.__dictSelctElement[rPath].copy()
        else:
            return []

    def setNewSelectElements(self, selectPath, elements):
        if selectPath in self.__dictSelctElement:
            self.__dictSelctElement[selectPath] = elements
            MyDatabase.instance.updateDictSelectElement(selectPath, json.dumps(self.__dictSelctElement[selectPath], ensure_ascii=False).replace("\"", "##"))
        else:
            self.__dictSelctElement[selectPath] = elements
            MyDatabase.instance.insertDictSelectElement(selectPath, json.dumps(self.__dictSelctElement[selectPath], ensure_ascii=False).replace("\"", "##"))

    def getFinalFiles(self):
        distPath = MyConfig.instance.distModPath
        if os.path.exists(distPath):
            shutil.rmtree(distPath)
        else:
            os.makedirs(distPath)
        for root, _, files in os.walk(MyConfig.instance.huanHuaInputPath):
            for file in files:
                if file.endswith(".json"):
                    fhuanPath = os.path.join(root, file)
                    #print(fhuanPath[fhuanPath.find("RU") + 3:])
                    metaPath = os.path.relpath(fhuanPath, MyConfig.instance.huanHuaInputPath)
                    fsor = os.path.join(MyConfig.instance.midModPath, metaPath)
                    fdst = os.path.join(distPath, metaPath)
                    print(fsor)
                    #print(fdst)
                    #print(metaPath)
                    #print(fhuanPath)
                    ffh = open(fhuanPath, mode="r", encoding="utf-8")
                    ffs = open(fsor, mode="r", encoding="utf-8")
                    Jfs = json.load(ffs, object_pairs_hook=OrderedDict)
                    Jfh = json.load(ffh, object_pairs_hook=OrderedDict)
                    print("处理:", root,file)
                    for eum in Jfh:
                        #print(eum)
                        #if "content" in Jfs.keys():
                        for selectKey in Jfs["content"]:
                            if selectKey["id"] == eum["id"]:
                                #print(eum["content"])
                                selectKey["content"] = eum["content"]
                                #print(selectKey["content"])
                                break
                        Jfs["culture"] = 2
            
                    distPathDir = os.path.dirname(fdst)
                    print(distPathDir)
                    if not os.path.exists(distPathDir):
                        os.makedirs(distPathDir)

                    with open(fdst, mode="w", encoding="utf-8") as fd:
                        fd.write(json.dumps(Jfs, indent=4, ensure_ascii=False))
            
                    ffh.close()
                    ffs.close()
        print("完成!!!")

