# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Entity:
    def __init__(self, d_name):
        self.type_ = d_name
        self.entity_name = ""
        self.entrance_word = []

class EntityDict:
    def __init__(self, d_name):
        self.type_ = d_name
        self.words = set()
        self.entities = []
        self.ridx = {}

    def load_file(self, d_file):
        concept_col = [0,1,2]
        entrance_col = 3

        fp = open(d_file)
        if fp == None:
            return None
        fp.readline()
        for line in fp:
            f = line.rstrip("\r\n").split(",")
            be = Entity(self.type_)
            for i in concept_col:
                if f[i] != "":
                    sf = f[i].split("/")
                    for w in sf:
                        be.entrance_word.append(w.decode("gbk"))
                        be.entity_name = w.decode("gbk")
                    break
            if be.entrance_word == []:
                continue
            if f[entrance_col] != None and f[entrance_col] != "":
                sf = f[entrance_col].split("/")
                for w in sf:
                    be.entrance_word.append(w.decode("gbk"))
            
            self.entities.append(be)
            self.words.update(be.entrance_word)
            self.add_ridx(be.entrance_word, be)

    def add_ridx(self, words, be):
        for w in words:
            if w not in self.ridx:
                self.ridx[w] = []
            self.ridx[w].append(be)

if __name__ == "__main__":
    be_dict = EntityDict("symp")
    be_dict.load_file("../data/zhichangai_symp.csv")
    print len(be_dict.words)
    print len(be_dict.entities)
    print len(be_dict.ridx)
