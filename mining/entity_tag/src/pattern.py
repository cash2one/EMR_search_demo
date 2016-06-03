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

        
   
        #血常规(22)    
        self.patternList.append(Atom("wbc", u"(?:[Ww]+[Bb]+[Cc]+|血?白细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[，×xX,\*]\W*?(:?[0-9]+(?:[eE\^][0-9]*)?)\D*?[Ll]", 1, "KV", "/L")) 
        self.patternList.append(Atom("neut#", u"(?:[Nn]+[Ee]+[Uu]?[Tt]?#?|中性粒细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[，×xX,\*]\W*?(:?[0-9]+(?:[eE\^][0-9]*)?)\D*?[Ll]", 1, "KV", "/L")) 
        self.patternList.append(Atom("ly#", u"(?:[Ll]+[Yy]+[Mm]?[Pp]?[Hh]?#?|淋巴细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[，×xX,\*]\W*?(:?[0-9]+(?:[eE\^][0-9]*)?)\D*?[Ll]", 1, "KV", "/L")) 
        self.patternList.append(Atom("mo#", u"(?:[Mm]+[Oo]+[Nn]?[Oo]?#?|单核细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[，×xX,\*]\W*?(:?[0-9]+(?:[eE\^][0-9]*)?)\D*?[Ll]", 1, "KV", "/L")) 
        self.patternList.append(Atom("eo#", u"(?:[Ee]+[Oo]+[Ss]?#?|嗜酸性粒细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[，×xX,\*]\W*?(:?[0-9]+(?:[eE\^][0-9]*)?)\D*?[Ll]", 1, "KV", "/L")) 
        self.patternList.append(Atom("baso#", u"(?:[Bb]+[Aa]+[Ss]+[Oo]+#?|嗜碱性粒细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[，×xX,\*]\W*?(:?[0-9]+(?:[eE\^][0-9]*)?)\D*?[Ll]", 1, "KV", "/L")) 
        self.patternList.append(Atom("neut%", u"(?:[Nn]+[Ee]+[Uu]?[Tt]?%?|中性粒细胞百分比|中性粒细胞比率)\W*?([0-9]+(?:[\.,][0-9]*)?)", 1, "KV", "%")) 
        self.patternList.append(Atom("ly%", u"(?:[Ll]+[Yy]+[Mm]?[Pp]?[Hh]?%?|淋巴细胞百分比|淋巴细胞比率)\W*?([0-9]+(?:[\.,][0-9]*)?)", 1, "KV", "%")) 
        self.patternList.append(Atom("mo%", u"(?:[Mm]+[Oo]+[Nn]?[Oo]?%?|单核细胞百分比|单核细胞比率)\W*?([0-9]+(?:[\.,][0-9]*)?)", 1, "KV", "%")) 
        self.patternList.append(Atom("eo%", u"(?:[Ee]+[Oo]+[Ss]?%?|嗜酸性粒细胞百分比|嗜酸性粒细胞比率)\W*?([0-9]+(?:[\.,][0-9]*)?)", 1, "KV", "%")) 
        self.patternList.append(Atom("baso%", u"(?:[Bb]+[Aa]+[Ss]+[Oo]+%?|嗜碱性粒细胞百分比|嗜碱性粒细胞比率)\W*?([0-9]+(?:[\.,][0-9]*)?)", 1, "KV", "%")) 
        self.patternList.append(Atom("rbc", u"(?:[Rr]+[Bb]+[Cc]+|血?红细胞计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[，×xX,\*]\W*?(:?[0-9]+(?:[eE\^][0-9]*)?)\D*?[Ll]", 1, "KV", "/L")) 
        self.patternList.append(Atom("hb", u"(?:[Hh]+[Gg]?[Bb]|血?白细胞计?数?)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "g/L")) 
        self.patternList.append(Atom("hct", u"(?:[Hh]+[Cc]+[Tt]+|红细胞比容)\W*?([0-9]+(?:\.[0-9]*)?)", 1, "KV", "L/L")) 
        self.patternList.append(Atom("mcv", u"(?:[Mm]+[Cc]+[Vv]+|红细胞平均体积)\W*?([0-9]+(?:\.[0-9]*)?)\W*?[Ff]+[Ll]+", 1, "KV", "fL")) 
        self.patternList.append(Atom("mch", u"(?:[Mm]+[Cc]+[Hh]+|平均红细胞血红蛋白量|平均血红蛋白量)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Pp]+[Gg]+", 1, "KV", "fL")) 
        self.patternList.append(Atom("mchc", u"(?:[Mm]+[Cc]+[Hh]+[Cc]+|平均红细胞血红蛋白量|平均血红蛋白量)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "fL")) 
        self.patternList.append(Atom("rdw", u"(?:[Rr]+[Dd]+[Ww]+|红细胞体积分布宽度)\W*?([0-9]+(?:\.[0-9]*)?)", 1, "KV", "%")) 
        self.patternList.append(Atom("plt", u"(?:[Pp]+[Ll]+[Tt]+|血小板计?数?)\W*?([0-9]+(?:[\.,][0-9]*)?)\W*?[，×xX,\*]\W*?(:?[0-9]+(?:[eE\^][0-9]*)?)\D*?[Ll]", 1, "KV", "/L")) 
        self.patternList.append(Atom("mpv", u"(?:[Mm]+[Pp]+[Vv]+|红细胞平均体积)\W*?([0-9]+(?:\.[0-9]*)?)", 1, "KV", "fL")) 
        self.patternList.append(Atom("pct", u"(?:[Pp]+[Cc]+[Tt]+|血小板比积|血小板比容)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[lL]", 1, "KV", "ng/ml")) 
        self.patternList.append(Atom("pdw", u"(?:[Pp]+[Dd]+[Ww]+|血小板分布宽度)\W*?([0-9]+(?:\.[0-9]*)?)", 1, "KV", "%")) 

        #生化,肝肾功(32)  
        self.patternList.append(Atom("alt", u"(?:[Aa]+[Ll]+[Tt]+|[Gg]+[Pp]+[Tt]+|血?清?丙氨酸氨基转换酶测?定?|血?清?谷丙转氨酶测?定?)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Uu]+/[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("ast", u"(?:[Aa]+[Ss]+[Tt]+|[Gg]+[Oo]+[Tt]+|血?清?天门冬酸氨基转换酶测?定?|血?清?谷草转氨酶测?定?)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("ggt", u"(?:[Gg]+[Gg]+[Tt]+|[γr]+-[Gg]+[Tt]+|血?清?谷酰转肽酶测?定?|血?清?谷氨酰基转移酶测?定?)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("alp", u"(?:[Aa]+[Ll]+[Pp]+|血?清?碱性磷酸酶测?定?)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("tp", u"(?:[Tt]+[Pp]+|总蛋白)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "g/L")) 
        self.patternList.append(Atom("alb", u"(?:[Aa]+[Ll]+[Bb]+|白蛋白)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "g/L")) 
        self.patternList.append(Atom("glb", u"(?:[Gg]+[Ll]+[Bb]+|球蛋白)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "g/L")) 
        #self.patternList.append(Atom("A/G", u"(?:A/G)\W*?([0-9]+(?:\.[0-9]*)?)", 1, "KV", "")) 
        self.patternList.append(Atom("tbil", u"(?:[Tt]+[Bt]+[Ii]+[Ll]+|总胆红素)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "umol/l")) 
        self.patternList.append(Atom("dbil", u"(?:[Dd]+[Bt]+[Ii]+[Ll]+|直接胆红素|结合胆红素)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "umol/l")) 
        self.patternList.append(Atom("pa", u"(?:[Pp]+[Aa]+|前白蛋白)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "g/l")) 
        #self.patternList.append(Atom("ALT/AST", u"(?:ALT/AST)\W*?([0-9]+(?:\.[0-9]*)?)", 1, "KV", "")) 
        self.patternList.append(Atom("tc", u"(?:[Tt]+[Cc]+|总胆固醇)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/L")) 
        self.patternList.append(Atom("tg", u"(?:[Tt]+[Gg]+|甘油三酯)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/L")) 
        self.patternList.append(Atom("hdl-c", u"(?:[Hh]+[Dd]+[Ll]-?[Cc]|高密度脂蛋白胆固醇)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/L")) 
        self.patternList.append(Atom("ldl-c", u"(?:[Ll]+[Dd]+[Ll]-?[Cc]|低密度脂蛋白胆固醇)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/L")) 
        self.patternList.append(Atom("ApoA1", u"(?:ApoA1|载脂蛋白A1)\W+?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/L")) 
        self.patternList.append(Atom("ApoB", u"(?:ApoB|载脂蛋白B)\W*?([0-9]+()(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/L")) 
        self.patternList.append(Atom("ApoA", u"(?:ApoA|载脂蛋白A)\W*?([0-9]+()(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/L")) 
        self.patternList.append(Atom("ApoA1/ApoB", u"(?:ApoA1/ApoB)\W*?([0-9]+()(?:\.[0-9]*)?)", 1, "KV", "")) 
        self.patternList.append(Atom("bnu", u"(?:[Bb]+[Uu]+[Nn]+|尿素氮)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/l")) 
        self.patternList.append(Atom("cr", u"(?:[Cc]+[Rr]+|肌酐)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "umol/l")) 
        self.patternList.append(Atom("ua", u"(?:[Uu]+[Aa]+|尿酸)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "umol/l")) 
        self.patternList.append(Atom("hco3", u"(?:[Hh]+[Cc]+[Oo]+3|血?清?碳酸氢盐测?定?)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/l")) 
        self.patternList.append(Atom("ldh", u"(?:[Ll]+[Dd]+[Hh]+|乳酸脱氢酶)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("ck", u"(?:[Cc]+[Kk]+|肌酸激酶)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("ckmb", u"(?:[Cc]+[Kk]+-?[Mm]+[Bb]+|肌酸激酶同工酶)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("hbdh", u"(?:α?-?[Hh]+[Bb]+[Dd]+[Hh]+|α?-?羟基?丁酸脱氢酶)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "U/L")) 
        self.patternList.append(Atom("K", u"(?:K|钾)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/l")) 
        self.patternList.append(Atom("Na", u"(?:Na|钠)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/l")) 
        self.patternList.append(Atom("Cl", u"(?:Cl|氯)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/l")) 
        self.patternList.append(Atom("Ca", u"(?:Ca|钙)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/l")) 
        self.patternList.append(Atom("glu", u"(?:[Gg]+[Ll]+[Uu]+|葡萄糖)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "mmol/l")) 
        self.patternList.append(Atom("co2", u"[Cc]+[Oo]+2\W*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "mmol/L")) 

        #尿常规(12)
        self.patternList.append(Atom("ph", u"(?:[Pp]+[Hh]+|酸碱度)\W*?([3-9]+(?:\.[0-9]*)?)", 1, "KV", "")) 
        self.patternList.append(Atom("sg", u"(?:[Ss]+[Gg]+|尿?比重)\W*?([0-9]+(?:\.[0-9]*)?)", 1, "KV", "")) 
        self.patternList.append(Atom("uro_1", u"(?:[Uu]+[Rr]+[Oo]+|[Uu]+[Bb]+[Gg]+|胆原)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "umol/l,")) 
        self.patternList.append(PolarityAtom("uro_2", u"(?:[Uu]+[Rr]+[Oo]+|[Uu]+[Bb]+[Gg]+|胆原)[^a-zA-Z]*?[+十阳]+", u"(?:[Uu]+[Rr]+[Oo]+|[Uu]+[Bb]+[Gg]+|胆原)[^a-zA-Z]*?[-阴]+", "P"))
        self.patternList.append(Atom("blo_1", u"(?:隐血)\W*?([0-9]+(?:\.[0-9]*)?)\D*?[Ll]+", 1, "KV", "/ul,")) 
        self.patternList.append(PolarityAtom("blo_2", u"(?:隐血)[^a-zA-Z]*?[+十阳]+", u"(?:隐血)[^a-zA-Z]*?[-阴]+", "P"))
        self.patternList.append(PolarityAtom("u_leu", u"(?:[Ll]+[Ee]+[Uu]+|尿白细胞)[^a-zA-Z]*?[+十阳]+", u"(?:[Ll]+[Ee]+[Uu]+|尿白细胞)[^a-zA-Z]*?[-阴]+", "P"))
        self.patternList.append(PolarityAtom("u_glu", u"(?:尿糖)[^a-zA-Z]*?[+十阳]+", u"(?:尿糖)[^a-zA-Z]*?[-阴]+", "P"))
        self.patternList.append(PolarityAtom("u_bil", u"(?:尿胆红素)[^a-zA-Z]*?[+十阳]+", u"(?:尿胆红素)[^a-zA-Z]*?[-阴]+", "P"))
        self.patternList.append(PolarityAtom("u_ket", u"(?:[Kk]+[Ee]+[Tt]+|酮体)[^a-zA-Z]*?[+十阳]+", u"(?:[Kk]+[Ee]+[Tt]+|酮体)[^a-zA-Z]*?[-阴]+", "P"))
        self.patternList.append(PolarityAtom("pro", u"(?:[Pp]+[Rr]+[Oo]+|尿蛋白)[^a-zA-Z]*?[+十阳]+", u"(?:[Pp]+[Rr]+[Oo]+|尿蛋白)[^a-zA-Z]*?[-阴]+", "P"))
        self.patternList.append(PolarityAtom("ery", u"(?:[Ee]+[Rr]+[Yy]+|尿红细胞)[^a-zA-Z]*?[+十阳]+", u"(?:[Ee]+[Rr]+[Yy]+|尿红细胞)[^a-zA-Z]*?[-阴]+", "P"))

   
        return self.patternList
'''

   
  
        #体液免疫   
        self.patternList.append(Atom("IgG", u"[Ii]+[Gg]+[Gg]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "g/L")) 
        self.patternList.append(Atom("IgA", u"[Ii]+[Gg]+[Aa]+\D*?([0-9]+(?:\.[0-9]*)?).*?[Ll]+", 1, "KV", "g/L")) 

  
'''
  
   



