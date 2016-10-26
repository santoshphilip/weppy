"""just eppy stuff"""

import StringIO
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
iddfhandle = StringIO.StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)
idf = IDF(StringIO.StringIO(""))
fname = '/Applications/EnergyPlus-8-3-0/ExampleFiles/5ZoneAirCooled.idf'
idf = IDF(fname)

def getidf():
    """return an idf"""
    return idf
    
def objnames():
    """return obj names"""
    return [anobj[0]['idfobj'] for anobj in idf.idd_info]   

def page2():
    idf = getidf()
    onames = objnames()
    n_len = [(objname, len(idf.idfobjects[objname.upper()])) for objname in onames]
    nlen = [(name, ln)for name, ln in n_len if ln > 0]
    return nlen


