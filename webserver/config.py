#encoding=utf8
import sys
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')

class Config:
    def __init__(self, confFile):
        self.conf = ConfigParser.ConfigParser()
        self.file = confFile
        self.conf.read(confFile)

    def getSections(self):
        return self.conf.sections()

    def getOption(self, key):
        return self.conf.options(key)

    def getValues(self, key):
        return self.conf.items(key)

    def get(self, section, key):
        return self.conf.get(section, key)

    def set(self, section, key, value):
        self.conf.set(section, key, value)

    def save(self):
        self.conf.write(open(self.file, 'r+'))

if __name__ == "__main__":
    config = Config('conf/search.conf')
    config.set('search', 'batch', 'test')
    config.save()

