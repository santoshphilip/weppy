from bottle import route, run
import eppystuff
import eppy.idf_helpers as idf_helpers
# idf = eppystuff.makeanidf()

def codetag(txt):
    """put code tags around the txt"""
    return "<code>%s<code>"  % (txt, )

@route('/hello')
def hello():
    return "Hello World!"

@route('/idf')
def idf():
    idf = eppystuff.getidf()
    lines = idf.idfstr().splitlines()
    return '<br>'.join(lines)

@route('/idf/0')
def idf():
    idf = eppystuff.getidf()
    objnames = idf_helpers.idfobjectkeys(idf)
    allidfobjects = [idf.idfobjects[objname.upper()] for objname in objnames]
    numobjects = [len(idfobjects) for idfobjects in allidfobjects]
    objsnums = ["%s -> %s" % (objname, num) 
            for objname, num in zip(objnames, numobjects)
            if num > 0]
    html = "<br>".join(objsnums)
    return codetag(html)
    
@route('/page1')
def page1():
    objnames = eppystuff.objnames()
    [objname for objname in objnames]
    return '<br>'.join(objnames)

@route('/page2')
def page2():
    nlens = eppystuff.page2()
    nlens = ['%s -> %s' % (name, ln) for name, ln in nlens]
    return '<br>'.join(nlens)
    

@route('/idf/0/<keyindex:int>')
def idfobject(keyindex):
    # try keyindex 84
    idf = eppystuff.getidf()
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    numobjects = len(idfobjects)
    html = "%s -> %s" % (objname, numobjects)
    return codetag(html)

@route('/idf/0/<keyindex:int>/<objindex:int>')
def idfobject(keyindex, objindex):
    # try keyindex 84
    idf = eppystuff.getidf()
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    idfobject = idfobjects[objindex]
    idfobjstr = str(idfobject)
    lines = idfobjstr.splitlines()
    html = '<br>'.join(lines)
    # return '<code>%s</code>' % (html, )
    return codetag(html)

@route('/idf/0/<keyindex:int>/<objindex:int>/<field>')
def idfobjectfield(keyindex, objindex, field):
    # try keyindex 84
    idf = eppystuff.getidf()
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    idfobject = idfobjects[objindex]
    html = "%s <- %s"  % (idfobject[field], field)
    return codetag(html)

run(host='localhost', port=8080, debug=True)

