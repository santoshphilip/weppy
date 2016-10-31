# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""just eppy stuff"""

import StringIO
from eppy.iddcurrent import iddcurrent
import eppy.idf_helpers as idf_helpers
from eppy.modeleditor import IDF
from eppy.EPlusInterfaceFunctions.eplusdata import removecomment
iddfile = './Energy+.idd'

def getfnames(fnametxt='./idffilenames.txt'):
    """return the idf filenames"""
    fhandle = open(fnametxt, 'r')
    lines = (removecomment(line.strip(), "#") for line in fhandle)
    lines = (line for line in lines if line)
    for line in lines:
        yield line

fnames = getfnames()
if IDF.getiddname() == None:
    IDF.setiddname(iddfile)
idfs = [IDF(fname) for fname in fnames]
nodekeys = idf_helpers.getidfkeyswithnodes()


def getidf():
    """return an idf"""
    return idfs
    
def getnodekeys():
    """return keys that have node fields"""
    return nodekeys
    
def objnames():
    """return obj names"""
    return idf_helpers.idfobjectkeys(idf)

def page2():
    idf = getidf()
    onames = objnames()
    n_len = [(objname, len(idf.idfobjects[objname.upper()])) for objname in onames]
    nlen = [(name, ln)for name, ln in n_len if ln > 0]
    return nlen


