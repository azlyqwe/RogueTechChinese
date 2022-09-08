# -*-coding:utf-8-*-

import sqlite3
import os
dataBaseName = "dataBase.db"

class MyDatabase(object):
    instance = None
    def __init__(self):
        initDataBaseFlag = not os.path.exists(dataBaseName)

        self.__dataBase = sqlite3.connect(dataBaseName)
        self.__cur = self.__dataBase.cursor()
        if initDataBaseFlag:
            self.__initDatabase()

    def __initDatabase(self):#初始化数据库
        self.__cur.execute("CREATE TABLE defaultSelectEum(eum TEXT PRIMARY KEY NOT NULL,\
        weight INTEGER NOT NULL)")
        self.__cur.execute("CREATE TABLE generatePath(\
        selectPath TEXT PRIMARY KEY NOT NULL,\
        mode INTEGER NOT NULL)")
        self.__cur.execute("CREATE TABLE analysisElement(\
        dir TEXT NOT NULL,\
        element TEXT NOT NULL)")

        self.__dataBase.commit()

    def getMarkPath(self):
        return self.__cur.execute("SELECT * FROM generatePath").fetchall()
    def insertMarkPath(self, path, mode):
        print(f"INSERT INTO generatePath(selectPath, mode) VALUES(\"{path}\", {mode})")
        self.__cur.execute(f"INSERT INTO generatePath(selectPath, mode) VALUES(\"{path}\", {mode})")
        self.__dataBase.commit()
    def updateMarkPath(self, path, mode):
        print(f"UPDATE generatePath SET mode={mode} WHERE selectPath = \"{path}\"")
        self.__cur.execute(f"UPDATE generatePath SET mode={mode} WHERE selectPath = \"{path}\"")
        self.__dataBase.commit()


    def getDefaultSelectEum(self):
        return self.__cur.execute("SELECT * FROM defaultSelectEum").fetchall()
    def setDefaultSelectEum(self, cotent):
        print(cotent)
        self.__cur.execute("DELETE FROM defaultSelectEum")
        for eum, weight in cotent:
            print(f"INSERT INTO defaultSelectEum(eum, weight) VALUES(\"{eum}\", {weight})")
            self.__cur.execute(f"INSERT INTO defaultSelectEum(eum, weight) VALUES(\"{eum}\", {weight})")
        self.__dataBase.commit()

    def getDictSelectElement(self):
        return self.__cur.execute("SELECT * FROM analysisElement").fetchall()

    def insertDictSelectElement(self, key, elements):
        #print(f"INSERT INTO analysisElement(dir, element) VALUES(\"{key}\", \"{elements}\")")
        self.__cur.execute(f"INSERT INTO analysisElement(dir, element) VALUES(\"{key}\", \"{elements}\")")
        self.__dataBase.commit()

    def updateDictSelectElement(self, key, elements):
        self.__cur.execute(f"UPDATE analysisElement SET element = \"{elements}\" WHERE dir = \"{key}\"")
        self.__dataBase.commit()

    def __del__(self):
        self.__dataBase.close()


    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args)
        return cls.instance
