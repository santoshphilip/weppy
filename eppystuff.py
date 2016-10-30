"""just eppy stuff"""

import StringIO
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.EPlusInterfaceFunctions.eplusdata import removecomment
iddfile = './Energy+.idd'

def getfnames(fnametxt='./idffilenames.txt'):
    """return the idf filenames"""
    # with open(fnametxt, 'r') as fhandle:
    fhandle = open(fnametxt, 'r')
    lines = (removecomment(line.strip(), "#") for line in fhandle)
    lines = (line for line in lines if line)
    for line in lines:
        yield line

fnames = getfnames()
if IDF.getiddname() == None:
    IDF.setiddname(iddfile)
idfs = [IDF(fname) for fname in fnames]


# fname = '/Applications/EnergyPlus-8-3-0/ExampleFiles/5ZoneAirCooled.idf'
# idf = IDF(fname)

def getidf():
    """return an idf"""
    return idfs
    
def objnames():
    """return obj names"""
    # return [anobj[0]['idfobj'] for anobj in idf.idd_info]
    return idf_helpers.idfobjectkeys(idf)

def page2():
    idf = getidf()
    onames = objnames()
    n_len = [(objname, len(idf.idfobjects[objname.upper()])) for objname in onames]
    nlen = [(name, ln)for name, ln in n_len if ln > 0]
    return nlen


