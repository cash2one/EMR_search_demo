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
        self.patternList.append(Atom("CA19-9", u"(?:糖链抗原|[Cc]+[Aa]+)\D*?19\-?9\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "U/ml")) 

        self.patternList.append(MultiAtom("wbc", u"WBC\D*?([0-9]+(?:[\.,][0-9]*)?)\D*?[×xX,\*]\D*?([0-9]+(?:[e\^][0-9]*)?).*?[Ll]", 1, 2, "KVS", "/L")) 
        '''
   
        #血常规    
        self.patternList.append(MultiAtom("wbc", u"[Ww]+[Bb]+[Cc]+\D*?([0-9]+(?:[\.,][0-9]*)?)\D*?[×xX,\*]\D*?([0-9]+(?:[e\^][0-9]*)?).*?[Ll]", 1, 2, "KVS", "/L")) 
        self.patternList.append(MultiAtom("rbc", u"[Rr]+[Bb]+[Cc]+\D*?([0-9]+(?:[\.,][0-9]*)?)\D*?[×xX,\*]\D*?([0-9]+(?:[e\^][0-9]*)?).*?[Ll]", 1, 2, "KVS", "/L")) 
        self.patternList.append(Atom("hgb", u"[Hh]+[Gg]+[Bb]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "g/L")) 
        self.patternList.append(Atom("hb", u"[Hh]+[Bb]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "g/L")) 
   
        #体液免疫   
        self.patternList.append(Atom("IgG", u"[Ii]+[Gg]+[Gg]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "g/L")) 
        self.patternList.append(Atom("IgA", u"[Ii]+[Gg]+[Aa]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "g/L")) 

        #生化,肝肾功  
        self.patternList.append(Atom("tbil", u"[Tt]+[Bb]+[Ii]+[Ll]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "μmol/L")) 
        self.patternList.append(Atom("dbil", u"[Dd]+[Bb]+[Ii]+[Ll]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "μmol/L")) 
        self.patternList.append(Atom("ast", u"[Aa]+[Ss]+[Tt]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("alt", u"[Aa]+[Ll]+[Tt}+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("ggt", u"[Gg]+[Gg]+[Tt}+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("alp", u"[Aa]+[Ll]+[Pp]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("alb", u"[Aa]+[Ll]+[Bb]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "G/L")) 
        self.patternList.append(Atom("glb", u"[Gg]+[Ll]+[Bb]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "G/L")) 
        self.patternList.append(Atom("Cr", u"[Cc]+[Rr]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "umol/L")) 
        self.patternList.append(Atom("bnu", u"[Bb]+[Nn]+[Uu]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "mmol/L")) 
        self.patternList.append(Atom("co2", u"[Cc]+[Oo]+2\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "mmol/L")) 
        self.patternList.append(Atom("p", u"P\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "mmol/L")) 
        self.patternList.append(Atom("k", u"K\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "mmol/L")) 
  
        '''
  
   
        return self.patternList



