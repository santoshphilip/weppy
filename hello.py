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
    objsnums = [(i, "%s - %s -> %s" % (i, objname, num)) 
            for i, (objname, num) in enumerate(zip(objnames, numobjects))
            if num > 0]
    linklines = ['<a href="0/%s">%s</a>' % (i, line, ) for i, line in objsnums]
    html = "<br>".join(linklines)
    return html # codetag(html)
    
@route('/idf/0/<keyindex:int>')
def theidfobjects(keyindex):
    # try keyindex 84
    idf = eppystuff.getidf()
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    objnames = [(i, str(idfobject.obj[1])) for i, idfobject in enumerate(idfobjects)]
    linklines = ['<a href="%s/%s">%s</a>' % (keyindex, i, line, ) for i, line in objnames]
    lines = [objname, '='*len(objname)] + linklines
    html = "<br>".join(lines)
    return html # codetag(html)

@route('/idf/0/<keyindex:int>/<objindex:int>')
def theidfobject(keyindex, objindex):
    # try keyindex 84
    idf = eppystuff.getidf()
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    idfobject = idfobjects[objindex]
    idfobjstr = str(idfobject)
    lines = idfobjstr.splitlines()
    lines.pop(0) # there is a blank line here
    linesfields = [(idfobject.objls[i+1], line) for i, line in enumerate(lines[1:])]
    linklines = ['<a href="%s/%s">%s</a>' % (objindex, fieldname, line, ) 
                        for i, (fieldname, line) in enumerate(linesfields)]
    linklineswithtitle = [objname, '='*len(objname)] + linklines
    html = '<br>'.join(linklineswithtitle)
    # return '<code>%s</code>' % (html, )
    return html

@route('/idf/0/<keyindex:int>/<objindex:int>/<field>')
def theidfobjectfield(keyindex, objindex, field):
    # try keyindex 84
    idf = eppystuff.getidf()
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    idfobject = idfobjects[objindex]
    html = "%s <- %s"  % (idfobject[field], field)
    return codetag(html)

run(host='localhost', port=8080, debug=True)

