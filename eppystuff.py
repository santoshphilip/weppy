"""just eppy stuff"""

import StringIO
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
iddfhandle = StringIO.StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

def makeanidf():
    """return an idf"""
    fname = '/Applications/EnergyPlus-8-3-0/ExampleFiles/5ZoneAirCooled.idf'
    idf = IDF(fname)
    return idf
