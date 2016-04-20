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

startJVM(getDefaultJVMPath(), "-Djava.class.path=/home/cihang/HanLP/hanlp.jar:/home/cihang/HanLP")
ns = JClass("com.hankcs.hanlp.seg.NShort.NShortSegment")
ns_seg = ns()
ns_index_seg = ns().enableIndexMode(True)
term_list = ns_seg.seg(sys.argv[1])
word_list = []
for i in xrange(0, term_list.size()):
    word_list.append(term_list.get(i).word)
print " ".join(word_list)
