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

class Atom:
    def __init__(self, field_name, range_pattern, index, type_name, unit=""):
        self.name = field_name
        self.range_pattern = range_pattern
        self.digital_index = index
        self.type_ = type_name
        self.unit = unit
    
class MultiAtom:
    def __init__(self, field_name, regex, index1, index2, type_name, unit=""):
        self.name = field_name
        self.regex = regex
        self.digital_index1 = index1
        self.digital_index2 = index2
        self.type_ = type_name
        self.unit = unit
    

class Pattern:
    def __init__(self):
        self.patternList = []
    
    def getPattern(self):
        self.patternList.append(PolarityAtom("dbqx", u"(大便)*潜血(.)*[(+)阳]+", u"(大便)*潜血(.)*[(-)阴]+", "P"))
        self.patternList.append(Atom("dbcs", u".*便.*([0-9]+).*([0-9]+).*次.*天", -1, "R")) 
        self.patternList.append(Atom("tmn", u"[Tt]+\w+[Nn]+\w+[Mm]+[01]+", -1, "KV", "")) 
        self.patternList.append(Atom("dukes", u"[Dd]+[Uu]+[Kk]+[Ee]+[Ss]*.*[ABCD]+\d*期", -1, "KV", "")) 
        self.patternList.append(Atom("cea", u"(?:[Cc]+[Ee]+[Aa]+|癌胚抗原)\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "ng/ml")) 
        self.patternList.append(Atom("CA19-9", u"(?:糖链抗原|[Cc]+[Aa]+)\D*?19\-9\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "U/ml")) 
        #self.patternList.append(MultiAtom("wbc", u"WBC\D.*?([0-9]+(?:[\.,][0-9]*)?)[xX,*]([0-9]+(?:[e\^][0-9]+)?).*?L", 1, 2, "KVS", "/L")) 
        self.patternList.append(MultiAtom("wbc", u"WBC\D*?([0-9]+(?:[\.,][0-9]*)?)\D*?[xX,\*]\D*?([0-9]+(?:[e\^][0-9]*)?).*?L", 1, 2, "KVS", "/L")) 
        return self.patternList



