#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../lib/")

from esindex import ESIndex
from mongo import Mongo
from index_xml_parser import IndexXmlParser, Field
from config import Config
import traceback

class Index:
    def __init__(self, conf, xmlConf=""):
        config = Config(conf)
        es_host = config.get("es", "host")
        es_batch = config.get("es", "batch")
        es_type = config.get("es", "type")
        self.es = ESIndex(es_host, es_batch, es_type)

        mongo_host = config.get("mongo", "host")
        mongo_port = int(config.get("mongo", "port"))
        mongo_db = config.get("mongo", "db")
        mongo_table = config.get("mongo", "table")
        self.mongo = Mongo(db=mongo_db, host=mongo_host, port=mongo_port, table=mongo_table)

        self.step = int(config.get("mongo", "step"))

        if xmlConf == "":
            self.fields = None
        else :
            self.fields = IndexXmlParser(xmlConf)

    def setIndex(self):
        self.es.create()
        for doc_type in index.fields.keys():
            mapping = {}
            for field in index.fields[doc_type]:
                mapping[field.name] = field.attrs()
            self.es.putMapping({"properties":mapping}, doc_type = doc_type)

    def run(self):
        size = self.mongo.size()
        iterNum = size / self.step
        actualSize = 0
        while (actualSize < size):
            dataset = self.fetchMongo(skip = actualSize, limit = self.step)
            actualSize += self.step
            try:
                for row in self.es.bulk(list(dataset)):
                    if row[0] == False:
                        print "%s write to es falied" %(row[1]["index"]["_id"])
            except:
                print traceback.format_exc()

    def fetchMongo(self, skip = 0, limit = 0):
        return self.mongo.find().skip(skip).limit(limit)


if __name__ == "__main__":
    #field= Index("../conf/index.conf")
    index = Index("../conf/index.conf", "../conf/index_field.xml")
    index.setIndex()
    print "create Index Success"
    index.run()
    print "build index Finished"

