"""module to control the opening and closing go file. 
\Have only a limited number of files open. 
Once the limit is hit, close a file to open a file"""

from eppy.modeleditor import IDF
from eppy.EPlusInterfaceFunctions.eplusdata import removecomment
from eppy.useful_scripts import loopdiagram
import eppy.idf_helpers as idf_helpers
from Queue import Queue

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
    idfs[idfindex] = idf
    alledges[idfindex] = alledge
    
def popidf(idfindex, fnames, idfs, alledges, nodekeys):
    """pop a file from the list"""
    idfs[idfindex] = None
    alledges[idfindex] = None

class IdfQ(Queue, object):
    # Queue is an old style class.
    # see http://stackoverflow.com/questions/11527921/python-inheriting-from-old-style-classes
    # on how to inherit a new style class from it
    def __init__(self, maxsize=0, putfunc=None, getfunc=None, **kwargs):
        super(IdfQ, self).__init__(maxsize)
        self.putfunc = putfunc
        self.getfunc = getfunc
        self.kwargs = kwargs
    def put(self, item, block=True, timeout=None):
        """over ride put"""
        if item not in self.queue:
            if self.full():
                self.get()
                super(IdfQ, self).put(item, block=block, timeout=timeout)
                if self.putfunc:
                    return self.putfunc(item, **self.kwargs)
            else:
                super(IdfQ, self).put(item, block=block, timeout=timeout)
                if self.putfunc:
                    return self.putfunc(item, **self.kwargs)
    def get(self, block=True, timeout=None):
        """over ride get"""
        got = super(IdfQ, self).get(block=block, timeout=timeout)
        if self.getfunc:
            self.getfunc(got, **self.kwargs)
        return got
        
                
        
