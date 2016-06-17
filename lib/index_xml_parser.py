#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from xml.etree import ElementTree  
import json

class Field:
    def __init__(self):
        self.name = ""
        self.type = "string"
        self.analyzer = "not_analyzed"
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
        js = {}
        js[self.name] = self.attr()
        return json.dumps(js)

    def attrs(self):
        attrs = {}
        attrs["type"] = self.type
        attrs["index"] = self.analyzer
        attrs["store"] = self.store
        return attrs

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
                        setattr(field, attr.tag, attr.text.strip())

                fields.append(field)
            self.index[name] = fields
             
if __name__ == "__main__":
    indexXml = IndexXmlParser("../conf/index_field.xml")
    #print indexXml["abc"]
    for key in indexXml.keys():
        for field in indexXml[key]:
            a = field
            print a


            
