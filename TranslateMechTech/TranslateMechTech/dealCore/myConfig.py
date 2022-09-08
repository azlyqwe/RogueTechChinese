#-*-coding:utf-8-*-
import os
import json
from collections import OrderedDict

'''
modPath mod文件目录,从此生成汉化文件
huanHuaOutputPath  存放生成汉化文本文件的目录
huanHuaInputPath  存放生成完成汉化文本文件的目录
midModPath 存放中间汉化文件目录以Localiztdef.json格式
distModPath 存放最终汉化文件目录
'''
class MyConfig(object):
    instance = None

    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args)
        return cls.instance

    def __init__(self):
        self.__configPath="config.json"
        if not os.path.exists(self.__configPath):
            self.__config = {"modPath":None,
                               "huanHuaOutputPath":"./build/output",
                               "huanHuaInputPath":"./input",
                               "midModPath":"./build/mid",
                               "distModPath":"./CN"
                               }
            self.save()
        with open(self.__configPath, "r+", encoding="utf-8") as f:  
            self.__config = json.load(f, object_pairs_hook=OrderedDict)
       


    def save(self):
        with open(self.__configPath, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.__config, indent=4, ensure_ascii=False))

    @property
    def modPath(self):
        return self.__config["modPath"]

    @modPath.setter
    def modPath(self, value):
        self.__config["modPath"] = value

    @property
    def huanHuaOutputPath(self):
        return self.__config["huanHuaOutputPath"]

    @huanHuaOutputPath.setter
    def huanHuaOutputPath(self, value):
        self.__config["huanHuaOutputPath"] = value


    @property
    def huanHuaInputPath(self):
        return self.__config["huanHuaInputPath"]

    @huanHuaInputPath.setter
    def huanHuaInputPath(self, value):
        self.__config["huanHuaInputPath"] = value

    @property
    def midModPath(self):
        return self.__config["midModPath"]

    @midModPath.setter
    def midModPath(self, value):
        self.__config["midModPath"] = value

    @property
    def distModPath(self):
        return self.__config["distModPath"]

    @distModPath.setter
    def distModPath(self, value):
        self.__config["distModPath"] = value



            


