"""module to control the opening and closing go file. 
\Have only a limited number of files open. 
Once the limit is hit, close a file to open a file"""

from eppy.modeleditor import IDF
from eppy.EPlusInterfaceFunctions.eplusdata import removecomment
from eppy.useful_scripts import loopdiagram
import eppy.idf_helpers as idf_helpers

iddfile = './Energy+.idd'

def getfnames(fnametxt='./idffilenames.txt'):
    """return the idf filenames"""
    fhandle = open(fnametxt, 'r')
    lines = (removecomment(line.strip(), "#") for line in fhandle)
    lines = (line for line in lines if line)
    for line in lines:
        yield line

def readidfs(fnames):
    """read all the idfs"""
    # fnames = getfnames()
    # if IDF.getiddname() == None:
    #     IDF.setiddname(iddfile)
    # idfs = [IDF(fname) for fname in fnames]
    # alledges = [loopdiagram.getedges(idf.idfname, iddfile) for idf in idfs]
    # nodekeys = idf_helpers.getidfkeyswithnodes()
    numfiles = len(fnames)
    idfs, alledges, nodekeys = [None] * numfiles, [None] * numfiles, [None] * numfiles
    return idfs, alledges, nodekeys

def initidfs(fnames):
    """read all the idfs"""
    # fnames = getfnames()
    # if IDF.getiddname() == None:
    #     IDF.setiddname(iddfile)
    # idfs = [IDF(fname) for fname in fnames]
    # alledges = [loopdiagram.getedges(idf.idfname, iddfile) for idf in idfs]
    # nodekeys = idf_helpers.getidfkeyswithnodes()
    numfiles = len(fnames)
    idfs, alledges, nodekeys = [None] * numfiles, [None] * numfiles, [None] * numfiles
    return idfs, alledges, nodekeys

def readidf(idfindex, fnames, idfs, alledges, nodekeys):
    """add idf to the list of open idfs"""
    if idfs[idfindex]:
        return None
    if IDF.getiddname() == None:
        IDF.setiddname(iddfile)
    fname = fnames[idfindex]
    idf = IDF(fname)
    alledge = loopdiagram.getedges(idf.idfname, iddfile)
    nodekeys = idf_helpers.getidfkeyswithnodes()
    idfs.insert(idfindex, idf)
    alledges.insert(idfindex, alledge)
    # return idfs, alledges, nodekeys
