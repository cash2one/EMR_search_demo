#coding:utf-8
  
import sys
reload(sys)
sys.setdefaultencoding("utf8")
from jpype import *

startJVM(getDefaultJVMPath(), "-Djava.class.path=/home/cihang/HanLP/hanlp.jar:/home/cihang/HanLP")
dp = JClass("com.hankcs.hanlp.dependency.CRFDependencyParser")
print dp.compute(sys.argv[1])
