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