# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""just eppy stuff"""

import os

import StringIO
import eppy.idf_helpers as idf_helpers
from eppy.useful_scripts import loopdiagram

import openidf 


# fnames = getfnames()
# if IDF.getiddname() == None:
#     IDF.setiddname(iddfile)
# idfs = [IDF(fname) for fname in fnames]
# alledges = [loopdiagram.getedges(idf.idfname, iddfile) for idf in idfs]
# nodekeys = idf_helpers.getidfkeyswithnodes()

maxopen = 7
fnames = list(openidf.getfnames())
idfs, alledges, nodekeys = openidf.initidfs(fnames)
kwargs = dict(fnames=fnames, idfs=idfs, alledges=alledges, nodekeys=nodekeys)
idfqueue = openidf.IdfQ(maxopen, openidf.readidf, openidf.popidf, **kwargs)

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
    try:
        objkey = idfobj.key
    except AttributeError as e:
        return None
    key_id = idf_helpers.idfobjectkeys(idf).index(objkey.upper())
    idfobjs = idf.idfobjects[objkey.upper()]
    obj_id = idfobjs.index(idfobj)
    return key_id, obj_id
    
def trimedges(edges, onlythis=None):
    """trim the edges with onlythis"""
    if not onlythis:
        return edges
    trimmed = []    
    for item in edges:
        a, b = item
        if a in onlythis or b in onlythis:
            trimmed.append(item)
    return trimmed
    
def save_imagesnippets(imgfolder, imgname, trimmed):
    """save images if they do not exist"""
    imgpath = '%s/%s' % (imgfolder, imgname, )
    if os.path.exists('%s.png' % (imgpath, )):
        return True
    if not os.path.exists(imgfolder):
        os.mkdir(imgfolder)
    loopdiagram.save_diagram(imgpath, loopdiagram.makediagram(trimmed))
    
    
# idf_helpers.name2idfobject(idf, Name=nnode)
def hvacname2idfobj(idf, aname):
    """return the idf object given it's name
    does initial check on 'ZoneHVAC:EquipmentConnections.Zone_name'"""
    equipconnections = idf_helpers.name2idfobject(idf, 
        objkeys=['ZoneHVAC:EquipmentConnections'.upper(), ],
        Zone_Name=aname)
    if equipconnections:
        return equipconnections
    return idf_helpers.name2idfobject(idf, Name=aname)