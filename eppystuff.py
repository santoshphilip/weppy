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
from eppy.useful_scripts import loopdiagram
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
alledges = [loopdiagram.getedges(idf.idfname, iddfile) for idf in idfs]
nodekeys = idf_helpers.getidfkeyswithnodes()


def getidfs():
    """return an idf"""
    return idfs
    
def getalledges():
    """return edges"""
    return alledges
    
def idfsandedges():
    """return idfs and edges"""
    return idfs, alledges
    
def an_idfedges(index):
    """return a specific idf and it's edges"""
    idfs, alledges = idfsandedges()
    return idfs[index], alledges[index]
    
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

def idfobjectindices(idf, idfobj):
    """return indices to construct the url for weppy"""
    objkey = idfobj.key
    key_id = idf_helpers.idfobjectkeys(idf).index(objkey.upper())
    idfobjs = idf.idfobjects[objkey.upper()]
    obj_id = idfobjs.index(idfobj)
    return key_id, obj_id