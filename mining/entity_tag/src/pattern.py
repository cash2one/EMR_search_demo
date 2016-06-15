# -*- coding: utf-8 -*-
import sys

class JianyanKV:
    def __init__(self):
        self.jianyan = {}
        self.unit = {}

    def load_jianyan(self, file_in):
        for line in open(file_in):
            if line.startswith("#"):
                continue
            items = line.strip().split(" ")
            if len(items) != 3:
                continue
            key = items[0]
            name = items[1]
            u = items[2]
            if u == u"%":
                u = u""
            self.jianyan[key] = name.decode("utf8")
            self.unit[key] = u.decode("utf8")
        return self.jianyan, self.unit

class JianyanPolarity:
    def __init__(self):
        self.jianyan = {}

    def load_jianyan(self, file_in):
        for line in open(file_in):
            if line.startswith("#"):
                continue
            items = line.strip().split(" ")
            if len(items) != 2:
                continue
            key = items[0]
            name = items[1]
            self.jianyan[key] = name.decode("utf8")
        return self.jianyan


class PolarityAtom:
    def __init__(self, field_name, yang, ying, type_name):
        self.name = field_name
        self.yang = yang
        self.ying = ying
        self.type_ = type_name

class Atom:
    def __init__(self, field_name, range_pattern, index, type_name, unit=""):
        self.name = field_name
        self.range_pattern = range_pattern
        self.digital_index = index
        self.type_ = type_name
        self.unit = unit

class Pattern:
    def __init__(self):
        self.patternList = []
        self.exp1 = u"\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[，×xX,\*]\W*?(:?[0-9]+(?:[eE\^][0-9]*)?)\D*?"
        self.exp2 = u"\W*?([0-9]+(?:[\.,][0-9]*)?)"
        self.exp3 = u"\W*?([0-9]+(?:\.[0-9]*)?)\D*?"
        self.yang = u"[^a-zA-Z]*?[+十阳]+"
        self.ying = u"[^a-zA-Z]*?[-阴]+" 
   
    def get_exp(self, unit):
        if unit == u"%" or unit == u"":
            return self.exp2
        s = u"[" + unit[-1].lower() + unit[-1].upper() + u"]"
        if u"10" in unit:
            return self.exp1 + s
        else:
            return self.exp3 + s

    def getPattern(self):
        jianyan, unit = JianyanKV().load_jianyan("/home/yongsheng/EMR_search_demo/mining/entity_tag/data/jianyan.config")
        for key in jianyan:
            u = unit[key]
            regex = u"(?:" + jianyan[key] + u")" + self.get_exp(u)
            self.patternList.append(Atom(key, regex, 1, "KV", u))

        jianyan = JianyanPolarity().load_jianyan("/home/yongsheng/EMR_search_demo/mining/entity_tag/data/jianyan.config")
        for key in jianyan:
            regex_yang = u"(?:" + jianyan[key] + u")" + self.yang 
            regex_ying = u"(?:" + jianyan[key] + u")" + self.ying
            self.patternList.append(PolarityAtom(key, regex_yang, regex_ying, "P"))
             
        #self.patternList.append(Atom("dbcs", u".*便.*([0-9]+).*([0-9]+).*次.*天", -1, "R")) 
        #self.patternList.append(Atom("tmn", u"[Tt]+\w+[Nn]+\w+[Mm]+[01]+", -1, "KV", "")) 
        #self.patternList.append(Atom("dukes", u"[Dd]+[Uu]+[Kk]+[Ee]+[Ss]*.*[ABCD]+\d*期", -1, "KV", ""))
         
        return self.patternList


