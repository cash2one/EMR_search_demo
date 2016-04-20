# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("/home/cihang/word-seg/src")
from entity_dict import *
from text_feature import *
from word_seg import *
from jpype import *
import os
from bs4 import BeautifulSoup
from parse_yx import *

ws = WordSeg()
terms = ws.seg_word(sys.argv[1].decode("utf8").encode("gbk"))
term_utf8 = []
for t in terms:
    term_utf8.append(t.decode("gbk"))
print u" ".join(term_utf8)
