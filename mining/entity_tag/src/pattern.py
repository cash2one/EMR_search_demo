# -*- coding: utf-8 -*-
import sys

class PolarityAtom:
    def __init__(self, field_name, yang, ying, type_name):
        self.name = field_name
        self.yang = yang
        self.ying = ying
        self.type_ = type_name
''' 
    def getName(self):
        return self.name

    def getType(self):
        return self.type_

    def getYang(self):
        return self.yang

    def getYing(self):
        return self.ying
'''

class Pattern:
    def __init__(self):
        self.patternList = []
    
    def getPattern(self):
        self.patternList.append(PolarityAtom("dbqx", u"(大便)*潜血(.)*[(+)阳]+", u"(大便)*潜血(.)*[(-)阴]+", "P"))
        return self.patternList



