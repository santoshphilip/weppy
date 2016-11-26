"""py.test for eppy_stuff.py"""


import StringIO

from eppy.modeleditor import IDF
from eppy.iddcurrent import iddcurrent
# from eppy.pytest_helpers import almostequal
import eppy.idf_helpers as idf_helpers

iddfhandle = StringIO.StringIO(iddcurrent.iddtxt)
  
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

import eppystuff    

def test_idfobjectindices():
    """py.test for idfobjectindices"""
    idf = IDF(StringIO.StringIO(""))
    data = (
    ('ZONE', 1, 0), # objkey, num_makes, obj_id
    ('ZONELIST', 3, 2), # objkey, num_makes, obj_id
    ('BRANCH', 13, 12), # objkey, num_makes, obj_id
    )
    for objkey, num_makes, obj_id in data:
        key_id = idf_helpers.idfobjectkeys(idf).index(objkey.upper())
        for i in range(num_makes):
            idfobj = idf.newidfobject(objkey.upper(), Name="obj%s" % (i, ))
        result = eppystuff.idfobjectindices(idf, idfobj)
        assert result == (key_id, obj_id)
        
def test_trimedges():
    """py.test trimedges"""
    data = (
    (
        [('a', 'b'), ('c', 'd')],
        None,
        [('a', 'b'), ('c', 'd')],        
    ), # edges, onlythis, expected
    (
        [('a', 'b'), ('c', 'd')],
        ('a'),
        [('a', 'b')],        
    ), # edges, onlythis, expected
    (
        [('a', 'b'), ('c', 'd')],
        ('a', 'b'),
        [('a', 'b')],        
    ), # edges, onlythis, expected
    (
        [('a', 'b'), ('c', 'd')],
        ('f',),
        [],       
    ), # edges, onlythis, expected
    (
        [('a', 'b'), ('c', 'd')],
        ('a', 'd'),
        [('a', 'b'), ('c', 'd')],       
    ), # edges, onlythis, expected
    )        
    for edges, onlythis, expected in data:
        result = eppystuff.trimedges(edges, onlythis)
        assert result == expected
        
def test_hvacname2idfobj():
    """py.test for hvacname2idfobj"""
    idf = IDF(StringIO.StringIO(""))
    plantloopname = "plantloopname"
    branchname = "branchname"
    pumpname = "pumpname"
    zonename = "zonename"
    plantloop = idf.newidfobject('PlantLoop'.upper(), 
                    Name=plantloopname,
                    Plant_Side_Inlet_Node_Name='CW Supply Inlet Node')
    branch = idf.newidfobject('Branch'.upper(), 
                    Name=branchname,
                    Component_1_Inlet_Node_Name='CW Supply Inlet Node')
    pump = idf.newidfobject('Pump:VariableSpeed'.upper(), 
                    Name=pumpname,
                    Inlet_Node_Name='CW Supply Inlet Node')
    zone = idf.newidfobject('zone'.upper(), Name=zonename)
    simulation = idf.newidfobject('SimulationControl'.upper()) 
    # - test
    names = [plantloopname, branchname, pumpname, zonename]
    idfobjs = [plantloop, branch, pump, zone]
    for name, idfobj in zip(names, idfobjs):
        result = eppystuff.hvacname2idfobj(idf, name)
        assert result == idfobj
    # test when objkeys!=None
    objkey = 'ZoneHVAC:EquipmentConnections'.upper()
    equipconnections = idf.newidfobject(objkey,
                        Zone_Name=zonename)
    result = eppystuff.hvacname2idfobj(idf, zonename)
    assert result == equipconnections
