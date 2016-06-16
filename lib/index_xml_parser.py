#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from xml.etree import ElementTree  

class Field:
    def __init__(self):
        self.name = ""
        self.type = "string"
        self.analyzer = None
        self.store = False

    @property
    def name(self):
        return self.name
    @name.setter
    def name(self, name_):
        self.name = name_

    @property
    def type(self):
        return self.type
    @type.setter
    def type(self, type_):
        self.type = type_

    @property
    def analyzer(self):
        return self.analyzer
    @analyzer.setter
    def analyzer(self, analyzer_):
        self.analyzer = analyzer_

    @property
    def store(self):
        return self.store
    @analyzer.setter
    def analyzer(self, store_):
        self.store = store_

    def __str__(self):
        return "name:%s, type:%s, analyzer:%s, store:%s" %\
            (self.name, self.type, self.analyzer, self.store)


class IndexXmlParser:
    def __init__(self, xml):
        self.index = {}
        self.root = ElementTree.parse(xml)
        self._parse()

    def __getitem__(self, key):
        return self.index[key]

    def keys(self):
        return self.index.keys()

    def _parse(self): 
        node = self.root.getiterator("index")
        for n in node:
            name = n.attrib["name"]
            fields = []
            child = n.getchildren()
            for c in child:
                field = Field()
                for attr in c.getchildren():
                    if hasattr(field, attr.tag):
                        setattr(field, attr.tag, attr.text)

                fields.append(field)
            self.index[name] = fields
             
if __name__ == "__main__":
    indexXml = IndexXmlParser("../conf/test.xml")
    print indexXml["abc"]
