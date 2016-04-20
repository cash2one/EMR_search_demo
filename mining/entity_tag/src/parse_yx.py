# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import sys
from bs4 import BeautifulSoup

def parse_disease(p):
    return p.a.string

def parse_symp(p):
    ems = p.find_all(name="em")
    symp = []
    for em in ems:
        symp.append(em.string)
    return symp

def parse_his(p):
    return p.string

def parse_check(p):
    return p.string
