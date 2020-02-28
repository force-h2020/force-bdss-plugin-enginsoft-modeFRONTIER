
# importing os module  
import os
# importing shutil module  
import shutil 
import time
import math
from subprocess import check_call
import re

def main():
       
    startBDSSPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))))
    print "startBDSSPath =", startBDSSPath
    
    print 'r=', r 
    print 'h=', h 
    
    file_name = "data.txt"
    d = dict()
    d["force.Y"] = r
    d["force.X"] = h
    file = open(file_name, "w")
    content = dictToString(d)
    file.write(content)
    file.close()
    
    #copy the .bat file to start force_bdss in the current directory
    source = '..'
    shutil.copy(os.path.join(startBDSSPath,"startBDSS.bat"), os.getcwd())
    batPath = os.path.join(os.getcwd(),"startBDSS.bat")
    #call force_bdss
    check_call( [batPath], cwd=os.getcwd() )
  
    #read the output data file created by force_bdss
    file = open("data_out.txt", "r")
    ret = dict()
    lines = file.readlines()
    for line in lines:
        ret.update(parseLine(line))
    file.close()
    T = ret["force.T"]
    S = ret["force.S"]
    V = ret["force.V"]
        
    return V, S, T
    
def parseLine(line):
    regex = r"(.*)=(.*)"
    matches = re.finditer(regex, line, re.MULTILINE)
    ret = dict()
    for matchNum, match in enumerate(matches):
        value = match.groups()[1]
        if isfloat(value):
            value = float(value)
        ret[match.groups()[0]] = value
    return ret
    
def dictToString(dict):
    ret = ""
    first = True
    for item in dict:
        if not first:
            ret = ret + "\n"
        ret = ret + item + "=" + str(dict[item])
        first = False
    return ret
    
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    V, S, T = main()