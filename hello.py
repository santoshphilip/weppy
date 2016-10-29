from bottle import route, run
import eppystuff
import eppy.idf_helpers as idf_helpers
from eppy.bunch_subclass import EpBunch

# idf = eppystuff.makeanidf()
aspace = "&emsp;"
abullet = "&bull;"
def codetag(txt):
    """put code tags around the txt"""
    return "<code>%s<code>"  % (txt, )

@route('/hello')
def hello():
    return "Hello World!"

@route('/idf')
def idftext():
    idf = eppystuff.getidf()
    lines = idf.idfstr().splitlines()
    return '<br>'.join(lines)

@route('/idf/0')
def idf():
    idf = eppystuff.getidf()
    objnames = idf_helpers.idfobjectkeys(idf)
    allidfobjects = [idf.idfobjects[objname.upper()] for objname in objnames]
    numobjects = [len(idfobjects) for idfobjects in allidfobjects]
    objsnums = [(i, objname, num)
            for i, (objname, num) in enumerate(zip(objnames, numobjects))
            if num > 0]
    urls = ["0/%s" % (i, ) for i, objname, num in objsnums]
    linktags = ['<a href=%s>%03d Items</a>' % (url, num, ) for (i, objname, num), url in zip(objsnums, urls)]
    lines = ["""%s -> id:%03d - %s""" % (linktag, i, objname) for (i, objname, num), linktag in zip(objsnums, linktags)]
    html = "<br>".join(lines)
    return html
    
@route('/idf/0/<keyindex:int>')
def theidfobjects(keyindex):
    # try keyindex 84
    idf = eppystuff.getidf()
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    objnames = [(i, str(idfobject.obj[1])) for i, idfobject in enumerate(idfobjects)]
    linklines = ['<a href="%s/%s">%s %s %s</a>' % (keyindex, i, i, abullet, line, ) for i, line in objnames]
    title = "ALL %sS" % (objname, )
    lines = [title, '='*len(title)] + linklines
    html = "<br>".join(lines)
    return html # codetag(html)

def refobjlink(idf, obj):
    if obj:
        idfobjects = idf.idfobjects[obj.key.upper()]
        objindex = idfobjects.index(obj)
        objkeys = idf_helpers.idfobjectkeys(idf)
        keyindex = objkeys.index(obj.key.upper())
        txt = "link to object %s %s" % (obj.key, objindex)
        url = "../%s/%s" % (keyindex, objindex)
        linktag = '<a href=../%s>%s</a>' % (url, txt)
        return linktag
    else:
        return ""
        
def bunch__functions(idfobject):
    """return function name and result"""        
    funcdct = idfobject.__functions
    funcsresults = [(key, funcdct[key](idfobject)) for key in funcdct.keys()]
    return funcsresults
    
def epbunchlist2html(epbunchlist):
    """convert funcsbunchlist to lines"""
    def epbunch2html(epbunch):
        lines = epbunch.obj[:2]
        return '->'.join(lines)
    lines = [epbunch2html(epbunch) for epbunch in epbunchlist]
    return ", ".join(lines)
    
def funcsresults2lines(funcsresults):
    """return lines of funcsresults"""
    funcssimple = [(func, value) for func, value in funcsresults if not isinstance(value, list)]
    funcslist = [(func, value) for func, value in funcsresults if isinstance(value, list)]
    funcsbunchlist = [(func, values) for func, values in funcslist if values]
    funcsbunchlist = [(func, epbunchlist2html(values)) 
                for func, values in funcsbunchlist if isinstance(values[0], EpBunch)]
    cleanfuncsresults = funcssimple + funcsbunchlist
    lines = ["%s = %s" % (func, value) for func, value in cleanfuncsresults]
    return lines
    
def getreferingobjs(idfobject):
    """return html of referingobjs"""
    idf = eppystuff.getidf()
    refobjs = idfobject.getreferingobjs() 
    keys = [refobj.key for refobj in refobjs]   
    objnames = [refobj.obj[1] for refobj in refobjs] 
    idfkeys = idf_helpers.idfobjectkeys(idf)
    keysobjsindexes = [(idfkeys.index(refobj.key.upper()), idf.idfobjects[refobj.key.upper()].index(refobj))
                    for refobj  in refobjs] 
    urls = ["../../%s/%s" % (idfkey, objkey) 
                for idfkey, objkey in keysobjsindexes]
    urllinks = ['<a href=%s>%s</a>' % (url, name) for url, name in zip(urls, objnames)]
    lines = ["%s->%s" % (refobj.key, urllink) for refobj, urllink in zip(refobjs, urllinks)]
    return ', '.join(lines)
    
def getmentioningobjs(idfobject):
    """return the html of mentioning objs"""
    idf = eppystuff.getidf()
    mentioningobjs = idf_helpers.getanymentions(idf, idfobject)
    print idfobject.Name
    print mentioningobjs
    keys = [mentioningobj.key for mentioningobj in mentioningobjs]   
    objnames = [mentioningobj.obj[1] for mentioningobj in mentioningobjs] 
    idfkeys = idf_helpers.idfobjectkeys(idf)
    keysobjsindexes = [(idfkeys.index(mentioningobj.key.upper()), 
                            idf.idfobjects[mentioningobj.key.upper()].index(mentioningobj))
                                for mentioningobj  in mentioningobjs] 
    urls = ["../../%s/%s" % (idfkey, objkey) 
                for idfkey, objkey in keysobjsindexes]
    urllinks = ['<a href=%s>%s</a>' % (url, name) for url, name in zip(urls, objnames)]
    lines = ["%s->%s" % (mentioningobj.key, urllink) for mentioningobj, urllink in zip(mentioningobjs, urllinks)]
    return ', '.join(lines)

@route('/idf/0/<keyindex:int>/<objindex:int>')
def theidfobject(keyindex, objindex):
    # try keyindex 84
    idf = eppystuff.getidf()
    objkeys = idf_helpers.idfobjectkeys(idf)
    objkey = objkeys[keyindex]
    idfobjects = idf.idfobjects[objkey]
    idfobject = idfobjects[objindex]
    fields = idfobject.objls
    values = idfobject.obj
    valuesfields = [(value, field) for value, field in zip(values, fields)]
    urls = ["%s/%s" % (objindex, field) for field in fields]
    linktags = ['<a href=%s>%s %s %s</a>' % (url, i, abullet, value,) 
                    for i, (url, value) in enumerate(zip(urls, values))]
    lines = ["%s %s %s" % (linktag, aspace, field) 
                for linktag, field in zip(linktags, fields)]
    # ---
    lines.pop(0)
    url = 'showlinks/%s' % (objindex, )
    showlinkslink = '<a href=%s>show links to other objects</a> <hr>' % (url, )
    
    url = 'andmore/%s' % (objindex, )
    andmorelink = '<hr> <a href=%s>run functions of this object</a>' % (url, )
    lines.append(andmorelink)
    url = 'refferingobjs/%s' % (objindex, )
    refferingobjslink = '<a href=%s>Show objects that refer to this object</a>' % (url, )
    lines.append(refferingobjslink)
    url = 'mentioningobjs/%s' % (objindex, )
    mentioningobjslink = '<a href=%s>Show objects that mention this object</a>' % (url, )
    lines.append(mentioningobjslink)
    lineswithtitle = [objkey, '='*len(objkey)] + lines
    lineswithtitle.insert(0, showlinkslink)
    html = '<br>'.join(lineswithtitle)
    return html

@route('/idf/0/<keyindex:int>/showlinks/<objindex:int>')
def theidfobjectshowlinks(keyindex, objindex):
    # try keyindex 84
    idf = eppystuff.getidf()
    objkeys = idf_helpers.idfobjectkeys(idf)
    objkey = objkeys[keyindex]
    idfobjects = idf.idfobjects[objkey]
    idfobject = idfobjects[objindex]
    fields = idfobject.objls
    values = idfobject.obj
    refobjs = [idfobject.get_referenced_object(fieldname) for fieldname in idfobject.objls]
    valuesfields = [(value, field) for value, field in zip(values, fields)]
    urls = ["%s/%s" % (objindex, field) for field in fields]
    linktags = ['<a href=%s>%s %s %s</a>' % (url, i, abullet, value,) 
                    for i, (url, value) in enumerate(zip(urls, values))]
    refobjtxts = [refobjlink(idf, refobj) for refobj in refobjs]
    lines = ["%s %s %s %s" % (linktag, aspace, field, refobjtxt) 
                for linktag, field, refobjtxt in zip(linktags, fields, refobjtxts)]
    lines.pop(0)
    lineswithtitle = [objkey, '='*len(objkey)] + lines
    html = '<br>'.join(lineswithtitle)
    return html

@route('/idf/0/<keyindex:int>/andmore/<objindex:int>')
def theidfobjectandmore(keyindex, objindex):
    idf = eppystuff.getidf()
    objkeys = idf_helpers.idfobjectkeys(idf)
    objkey = objkeys[keyindex]
    idfobjects = idf.idfobjects[objkey]
    idfobject = idfobjects[objindex]
    fields = idfobject.objls
    values = idfobject.obj
    valuesfields = [(value, field) for value, field in zip(values, fields)]
    urls = ["%s/%s" % (objindex, field) for field in fields]
    linktags = ['<a href=%s>%s %s %s</a>' % (url, i, abullet, value,) 
                    for i, (url, value) in enumerate(zip(urls, values))]
    lines = ["%s %s %s" % (linktag, aspace, field) 
                for linktag, field in zip(linktags, fields)]
    # ---
    lines.pop(0)
    lineswithtitle = [objkey, '='*len(objkey)] + lines
    funcsresults = bunch__functions(idfobject)
    funclines = funcsresults2lines(funcsresults)
    # for line in funclines:
    #     print line
    html = '<br>'.join(lineswithtitle + ["<hr>", ] + funclines)
    # return '<code>%s</code>' % (html, )
    return html

@route('/idf/0/<keyindex:int>/refferingobjs/<objindex:int>')
def theidfobjectrefferingobjs(keyindex, objindex):
    idf = eppystuff.getidf()
    objkeys = idf_helpers.idfobjectkeys(idf)
    objkey = objkeys[keyindex]
    idfobjects = idf.idfobjects[objkey]
    idfobject = idfobjects[objindex]
    fields = idfobject.objls
    values = idfobject.obj
    valuesfields = [(value, field) for value, field in zip(values, fields)]
    urls = ["%s/%s" % (objindex, field) for field in fields]
    linktags = ['<a href=%s>%s %s %s</a>' % (url, i, abullet, value,) 
                    for i, (url, value) in enumerate(zip(urls, values))]
    lines = ["%s %s %s" % (linktag, aspace, field) 
                for linktag, field in zip(linktags, fields)]
    # ---
    lines.pop(0)
    lineswithtitle = [objkey, '='*len(objkey)] + lines
    referingobjsline = getreferingobjs(idfobject)
    html = '<br>'.join(lineswithtitle + ["<hr>", ] + [referingobjsline, ])
    return html

@route('/idf/0/<keyindex:int>/mentioningobjs/<objindex:int>')
def theidfobjectmentioningobjs(keyindex, objindex):
    idf = eppystuff.getidf()
    objkeys = idf_helpers.idfobjectkeys(idf)
    objkey = objkeys[keyindex]
    idfobjects = idf.idfobjects[objkey]
    idfobject = idfobjects[objindex]
    fields = idfobject.objls
    values = idfobject.obj
    valuesfields = [(value, field) for value, field in zip(values, fields)]
    urls = ["%s/%s" % (objindex, field) for field in fields]
    linktags = ['<a href=%s>%s %s %s</a>' % (url, i, abullet, value,) 
                    for i, (url, value) in enumerate(zip(urls, values))]
    lines = ["%s %s %s" % (linktag, aspace, field) 
                for linktag, field in zip(linktags, fields)]
    # ---
    lines.pop(0)
    lineswithtitle = [objkey, '='*len(objkey)] + lines
    mentioningobjsline = getmentioningobjs(idfobject)
    html = '<br>'.join(lineswithtitle + ["<hr>", ] + ['Mentioning Objects', mentioningobjsline, ])
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

