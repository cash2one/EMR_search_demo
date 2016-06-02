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

        #self.patternList.append(MultiAtom("wbc", u"WBC\D*?([0-9]+(?:[\.,][0-9]*)?)\D*?[×xX,\*]\D*?([0-9]+(?:[e\^][0-9]*)?).*?[Ll]", 1, 2, "KVS", "/L")) 
        
   
        #血常规    
        self.patternList.append(Atom("wbc", u"(:?[Ww]+[Bb]+[Cc]+|血?白细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[×xX,\*]\W*?(:?[0-9]+(?:[e\^][0-9]*)?)\D*?[Ll]", 2, "KV", "/L")) 
        self.patternList.append(Atom("neut#", u"(:?[Nn]+[Ee]+[Uu]?[Tt]?#?|中性粒细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[×xX,\*]\W*?(:?[0-9]+(?:[e\^][0-9]*)?)\D*?[Ll]", 2, "KV", "/L")) 
        self.patternList.append(Atom("ly#", u"(:?[Ll]+[Yy]+[Mm]?[Pp]?[Hh]?#?|淋巴细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[×xX,\*]\W*?(:?[0-9]+(?:[e\^][0-9]*)?)\D*?[Ll]", 2, "KV", "/L")) 
        self.patternList.append(Atom("mo#", u"(:?[Mm]+[Oo]+[Nn]?[Oo]?#?|单核细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[×xX,\*]\W*?(:?[0-9]+(?:[e\^][0-9]*)?)\D*?[Ll]", 2, "KV", "/L")) 
        self.patternList.append(Atom("eo#", u"(:?[Ee]+[Oo]+[Ss]?#?|嗜酸性粒细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[×xX,\*]\W*?(:?[0-9]+(?:[e\^][0-9]*)?)\D*?[Ll]", 2, "KV", "/L")) 
        self.patternList.append(Atom("baso#", u"(:?[Bb]+[Aa]+[Ss]+[Oo]+#?|嗜碱性粒细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[×xX,\*]\W*?(:?[0-9]+(?:[e\^][0-9]*)?)\D*?[Ll]", 2, "KV", "/L")) 
        self.patternList.append(Atom("neut%", u"(:?[Nn]+[Ee]+[Uu]?[Tt]?%?|中性粒细胞百分比|中性粒细胞比率)\W*?([0-9]+(?:[\.,][0-9]*)?)", 2, "KV", "%")) 
        self.patternList.append(Atom("ly%", u"(:?[Ll]+[Yy]+[Mm]?[Pp]?[Hh]?%?|淋巴细胞百分比|淋巴细胞比率)\W*?([0-9]+(?:[\.,][0-9]*)?)", 2, "KV", "%")) 
        self.patternList.append(Atom("mo%", u"(:?[Mm]+[Oo]+[Nn]?[Oo]?%?|单核细胞百分比|单核细胞比率)\W*?([0-9]+(?:[\.,][0-9]*)?)", 2, "KV", "%")) 
        self.patternList.append(Atom("eo%", u"(:?[Ee]+[Oo]+[Ss]?%?|嗜酸性粒细胞百分比|嗜酸性粒细胞比率)\W*?([0-9]+(?:[\.,][0-9]*)?)", 2, "KV", "%")) 
        self.patternList.append(Atom("baso%", u"(:?[Bb]+[Aa]+[Ss]+[Oo]+%?|嗜碱性粒细胞百分比|嗜碱性粒细胞比率)\W*?([0-9]+(?:[\.,][0-9]*)?)", 2, "KV", "%")) 
        self.patternList.append(Atom("rbc", u"(:?[Rr]+[Bb]+[Cc]+|血?红细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[×xX,\*]\W*?(:?[0-9]+(?:[e\^][0-9]*)?)\D*?[Ll]", 2, "KV", "/L")) 
        self.patternList.append(Atom("hb", u"(:?[Hh]+[Gg]?[Bb]|血?白细胞计?数?)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 2, "KV", "g/L")) 
        self.patternList.append(Atom("hct", u"(:?[Hh]+[Cc]+[Tt]+|红细胞比容)\W*?([0-9]+(?:\.[0-9]*)?)", 2, "KV", "L/L")) 
        self.patternList.append(Atom("mcv", u"(:?[Mm]+[Cc]+[Vv]+|红细胞平均体积)\W*?([0-9]+(?:\.[0-9]*)?)\W*?[Ff]+[Ll]+", 2, "KV", "fL")) 
        self.patternList.append(Atom("mch", u"(:?[Mm]+[Cc]+[Hh]+|平均红细胞血红蛋白量|平均血红蛋白量)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Pp]+[Gg]+", 2, "KV", "fL")) 
        self.patternList.append(Atom("mchc", u"(:?[Mm]+[Cc]+[Hh]+[Cc]+|平均红细胞血红蛋白量|平均血红蛋白量)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 2, "KV", "fL")) 
        self.patternList.append(Atom("rdw", u"(:?[Rr]+[Dd]+[Ww]+|红细胞体积分布宽度)\W*?([0-9]+(?:\.[0-9]*)?)", 2, "KV", "%")) 
        self.patternList.append(Atom("plt", u"(:?[Pp]+[Ll]+[Tt]+|血小板计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[×xX,\*]\W*?(:?[0-9]+(?:[e\^][0-9]*)?)\D*?[Ll]", 2, "KV", "/L")) 
        self.patternList.append(Atom("mpv", u"(:?[Mm]+[Pp]+[Vv]+|红细胞平均体积)\W*?([0-9]+(?:\.[0-9]*)?)", 2, "KV", "fL")) 
        self.patternList.append(Atom("pct", u"(:?[Pp]+[Cc]+[Tt]+|血小板比积|血小板比容)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[lL]", 2, "KV", "ng/ml")) 
        self.patternList.append(Atom("pdw", u"(:?[Pp]+[Dd]+[Ww]+|血小板分布宽度)\W*?([0-9]+(?:\.[0-9]*)?)", 2, "KV", "%")) 
   
        return self.patternList
'''
  1 WBC 34103 白细胞/血白细胞/白细胞计数/白细胞数
  2 Neu 1759  中性粒细胞百分比/中性粒细胞比率/NE%/Neu%/NEUT%
  3 LY 54 淋巴细胞百分比/淋巴细胞比率/LYM/LY%/Lymph%
  4 MON 463 单核细胞百分比/单核细胞比率/MONO/MONO%/MO%
  5 EO 8 嗜酸性粒细胞百分比/嗜酸性粒细胞比率/EOS/EOS%
  6 BASO 0 嗜碱性粒细胞百分比/嗜碱性粒细胞比率/BASO%
  7 Neu 1759  中性粒细胞数/中性粒细胞计数/NE#/Neu#/NEUT/NEUT#
  8 LY 54 淋巴细胞计数/淋巴细胞/LYM/LY#/Lymph#
  9 MO 463 单核细胞计数/MO#
 10 EO 8 嗜酸性粒细胞/嗜酸性粒细胞计数/EOS/EOS#
 11 BASO 0 嗜碱性粒细胞计数/嗜碱性粒细胞数/嗜碱性粒细胞/BASO#
 12 RBC 3158 红细胞/血红细胞/红细胞计数/红细胞数
 13 Hb 35769 HB/HGB/血红蛋白
 14 HCT 31 红细胞比容
 15 MCV 656 红细胞平均体积
 16 MCH 25 平均红细胞血红蛋白量/平均血红蛋白量
 17 MCHC 482 红细胞平均血红蛋白浓度/平均血红蛋白浓度
 18 RDW 0 红细胞体积分布宽度
 19 PLT 18981 血小板计数/血小板数/血小板
 20 MPV 1 平均血小板体积
 21 PCT 680 血小板比积/血小板比容
 22 PDW 0 血小板分布宽度


   
  
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
  
   



