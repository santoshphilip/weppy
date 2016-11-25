# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
from sys import argv

from bottle import route, run
from bottle import static_file
import eppystuff
import eppy.idf_helpers as idf_helpers
from eppy.bunch_subclass import EpBunch
import documentationurls
from documentationurls import getdoclink
IMGFOLDER = "temporary_images"

aspace = "&emsp;"
abullet = "&bull;"
def codetag(txt):
    """put code tags around the txt"""
    return "<code>%s<code>"  % (txt, )
    
def putfilenameontop(idf, lines):
    """put the idf file name on top of page"""
    openfile = '<%s>%s</%s>' % ('h4', idf.idfname, 'h4')
    lines = [openfile, '<hr>'] + lines
    return lines
    
@route('/hello')
def hello():
    return "Hello World!"

@route('/static/<filepath:path>')
def server_static(filepath):
    imgpath = static_file(filepath, root='./%s' % (IMGFOLDER, ))
    return imgpath

@route('/')
def homepage():
    line1 = '<a href=readme>Readme</a>' 
    line2 = '<a href=idf>view idf files</a>' 
    line3 = '<img src="/static/a.png">'
    lines = [line1] + [line2]
    return '<BR>'.join(lines)

@route('/readme')
def readmepage():
    import readme
    return readme.txt

@route('/idf')
def idflist():
    idfs = eppystuff.getidfs()
    urls = ["idf/%s" % (i, ) for i in range(len(idfs))]
    lines = ['%s %s <a href=%s>%s</a>' % (i, abullet, url, idf.idfname)
                    for i, (url, idf) in enumerate(zip(urls, idfs))]
    lines.insert(0, "<h3>IDF files you can view</h3>")
    return '<br>'.join(lines)

@route('/idf/<idfindex:int>')
def idf(idfindex):
    idf, edges = eppystuff.an_idfedges(idfindex)
    objnames = idf_helpers.idfobjectkeys(idf)
    allidfobjects = [idf.idfobjects[objname.upper()] for objname in objnames]
    numobjects = [len(idfobjects) for idfobjects in allidfobjects]
    objsnums = [(i, objname, num)
            for i, (objname, num) in enumerate(zip(objnames, numobjects))
            if num > 0]
    urls = ["%s/%s" % (idfindex,i, ) for i, objname, num in objsnums]
    # siteurl ="http://bigladdersoftware.com/epx/docs/8-3/input-output-reference/"
    docurls = [getdoclink(objname.upper()) for i, objname, num in objsnums]
    durltags = [' <a href=%s target="_blank">docs</a>' % (url, ) 
                    for url in docurls]
    linktags = ['<a href=%s>%03d Items</a>' % (url, num, ) for (i, objname, num), url in zip(objsnums, urls)]
    lines = ["""%s -> id:%03d - (%s) - %s""" % (linktag, i, durltag, objname) 
            for (i, objname, num), linktag, durltag in zip(objsnums, linktags, durltags)]
    # openfile = 'open file = %s' % (idf.idfname, )
    # lines = [openfile, '<hr>'] + lines
    url = "show_all/%s" % (idfindex, )
    showmore = '<a href=%s>show more</a>' % (url, )
    lines = [showmore, ""] + lines
    lines = putfilenameontop(idf, lines)
    html = "<br>".join(lines)
    return html
    
@route('/idf/show_all/<idfindex:int>')
def idf_all(idfindex):
    idf, edges = eppystuff.an_idfedges(idfindex)
    objnames = idf_helpers.idfobjectkeys(idf)
    allidfobjects = [idf.idfobjects[objname.upper()] for objname in objnames]
    numobjects = [len(idfobjects) for idfobjects in allidfobjects]
    objsnums = [(i, objname, num)
            for i, (objname, num) in enumerate(zip(objnames, numobjects))
            if num >= 0]
    urls = ["../%s/%s" % (idfindex,i, ) for i, objname, num in objsnums]
    # siteurl ="http://bigladdersoftware.com/epx/docs/8-3/input-output-reference/"
    docurls = [getdoclink(objname.upper()) for i, objname, num in objsnums]
    durltags = [' <a href=%s target="_blank">docs</a>' % (url, ) 
                    for url in docurls]
    linktags = []
    for (i, objname, num), url in zip(objsnums, urls):
        if num:
            linktag = '<a href=%s>%03d Items</a>' % (url, num, )
        else:
            linktag = '%03d Items' % (num, )
            linktag = '_' * (len(linktag)-1)
        linktags.append(linktag)
    # linktags = ['<a href=%s>%03d Items</a>' % (url, num, ) for (i, objname,num), url in zip(objsnums, urls)]
    lines = ["""%s -> id:%03d - (%s) - %s""" % (linktag, i, durltag, objname) 
            for (i, objname, num), linktag, durltag in zip(objsnums, linktags, durltags)]
    # openfile = 'open file = %s' % (idf.idfname, )
    # lines = [openfile, '<hr>'] + lines
    url = "../%s" % (idfindex, )
    showless = '<a href=%s>show less</a>' % (url, )
    lines = [showless, ""] + lines
    lines = putfilenameontop(idf, lines)
    html = "<br>".join(lines)
    return html

@route('/idf/<idfindex:int>/<keyindex:int>')
def theidfobjects(idfindex, keyindex):
    idf, edges = eppystuff.an_idfedges(idfindex)
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    objnames = [(i, str(idfobject.obj[1])) for i, idfobject in enumerate(idfobjects)]
    linklines = ['<a href="%s/%s">%s %s %s</a>' % (keyindex, i, i, abullet, line, ) for i, line in objnames]
    titledoc = '<a href="%s" target="_blank">docs</a>' % (getdoclink(objname.upper()))
    justtitle = "ALL %sS" % (objname, )
    title = '%s (%s)' % (justtitle, titledoc)
    lines = [title, '='*len(justtitle)] + linklines
    lines = putfilenameontop(idf, lines)
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
    funcssimple = [(func, value) 
        for func, value in funcsresults if not isinstance(value, list)]
    funcslist = [(func, value) 
        for func, value in funcsresults if isinstance(value, list)]
    funcsbunchlist = [(func, values) for func, values in funcslist if values]
    funcsbunchlist = [(func, epbunchlist2html(values)) 
                for func, values in funcsbunchlist 
                    if isinstance(values[0], EpBunch)]
    cleanfuncsresults = funcssimple + funcsbunchlist
    lines = ["%s = %s" % (func, value) for func, value in cleanfuncsresults]
    return lines
    
def getreferingobjs(idfindex, idfobject):
    """return html of referingobjs"""
    idf, edges = eppystuff.an_idfedges(idfindex)
    refobjs = idfobject.getreferingobjs() 
    keys = [refobj.key for refobj in refobjs]   
    objnames = [refobj.obj[1] for refobj in refobjs] 
    idfkeys = idf_helpers.idfobjectkeys(idf)
    keysobjsindexes = [(idfkeys.index(refobj.key.upper()), 
                        idf.idfobjects[refobj.key.upper()].index(refobj))
                            for refobj  in refobjs] 
    urls = ["../../%s/%s" % (idfkey, objkey) 
                for idfkey, objkey in keysobjsindexes]
    urllinks = ['<a href=%s>%s</a>' % (url, name) 
        for url, name in zip(urls, objnames)]
    lines = ["%s->%s" % (refobj.key, urllink) 
        for refobj, urllink in zip(refobjs, urllinks)]
    return ', '.join(lines)
    
def getmentioningobjs(idfindex, idfobject):
    """return the html of mentioning objs"""
    idf, edges = eppystuff.an_idfedges(idfindex)
    mentioningobjs = idf_helpers.getanymentions(idf, idfobject)
    keys = [mentioningobj.key for mentioningobj in mentioningobjs]   
    objnames = [mentioningobj.obj[1] for mentioningobj in mentioningobjs] 
    idfkeys = idf_helpers.idfobjectkeys(idf)
    keysobjsindexes = [(idfkeys.index(mentioningobj.key.upper()), 
                idf.idfobjects[mentioningobj.key.upper()].index(mentioningobj))
                                for mentioningobj  in mentioningobjs] 
    urls = ["../../%s/%s" % (idfkey, objkey) 
                for idfkey, objkey in keysobjsindexes]
    urllinks = ['<a href=%s>%s</a>' % (url, name) 
        for url, name in zip(urls, objnames)]
    lines = ["%s->%s" % (mentioningobj.key, urllink) 
        for mentioningobj, urllink in zip(mentioningobjs, urllinks)]
    return ', '.join(lines)

@route('/idf/<idfindex:int>/<keyindex:int>/<objindex:int>')
def theidfobject(idfindex, keyindex, objindex):
    idf, edges = eppystuff.an_idfedges(idfindex)
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
    iddinfos = ['<a href=%s/iddinfo>%s</a>' % (url, '?')  
                        for url in urls]
    lines = ["%s %s %s %s %s" % (linktag, aspace, field, abullet, iddinfo) 
                for linktag, field, iddinfo in zip(linktags, fields, iddinfos)]
    # ---
    lines.pop(0)
    url = 'showlinks/%s' % (objindex, )
    showlinkslink = '<a href=%s>show links to other objects</a>' % (url, )
    url = 'nodementions/%s' % (objindex, )
    showmentionslink = '<a href=%s>show node connections</a> <hr>' % (url, )
    
    url = 'objfunctions/%s' % (objindex, )
    objfunctionslink = '<hr> <a href=%s>run functions of this object</a>' % (url, )
    lines.append(objfunctionslink)
    url = 'refferingobjs/%s' % (objindex, )
    refferingobjslink = '<a href=%s>Show objects that refer to this object</a> ->this runs slow :-(' % (url, )
    lines.append(refferingobjslink)
    url = 'mentioningobjs/%s' % (objindex, )
    mentioningobjslink = '<a href=%s>Show objects that mention this object</a>' % (url, )
    lines.append(mentioningobjslink)
    # - hvac links
    url = 'hvacprevnext/%s' % (objindex, )
    hvacprevnextlink = 'HVAC object in loop -> <a href=%s>prev objects & next objects</a> (broken at zone level :-(' % (url, )
    lines.append(hvacprevnextlink)
    # - 
    heading = '%s <a href=%s/key/iddinfo> %s</a>' % (objkey, objindex, '?')
    headingdoc = '<a href="%s" target="_blank">docs</a>' % (getdoclink(objkey.upper()))
    headingwithdoc = '%s (%s)' % (heading, headingdoc)
    lineswithtitle = [headingwithdoc, "=" * len(objkey)] + lines
    lineswithtitle.insert(0, showmentionslink)
    lineswithtitle.insert(0, showlinkslink)
    lineswithtitle = putfilenameontop(idf, lineswithtitle)
    html = '<br>'.join(lineswithtitle)
    return html

@route('/idf/<idfindex:int>/<keyindex:int>/showlinks/<objindex:int>')
def theidfobjectshowlinks(idfindex, keyindex, objindex):
    idf, edges = eppystuff.an_idfedges(idfindex)
    objkeys = idf_helpers.idfobjectkeys(idf)
    objkey = objkeys[keyindex]
    idfobjects = idf.idfobjects[objkey]
    idfobject = idfobjects[objindex]
    fields = idfobject.objls
    values = idfobject.obj
    refobjs = [idfobject.get_referenced_object(fieldname) 
                        for fieldname in idfobject.objls]
    # nrefobjs -> objects that are not referenced, so use the previous field
    nrefobjs = [idf_helpers.getobject_use_prevfield(idf, idfobject, fieldname) 
                        for fieldname in idfobject.fieldnames]
    # merge nrefobjs inot refobjs
    for i, (obj1, obj2) in enumerate(zip(refobjs, nrefobjs)):
        if not obj1:
            refobjs[i] = obj2
    valuesfields = [(value, field) for value, field in zip(values, fields)]
    urls = ["../%s/%s" % (objindex, field) for field in fields]
    linktags = ['<a href=%s>%s %s %s</a>' % (url, i, abullet, value,) 
                    for i, (url, value) in enumerate(zip(urls, values))]
    refobjtxts = [refobjlink(idf, refobj) for refobj in refobjs]
    lines = ["%s %s %s %s" % (linktag, aspace, field, refobjtxt) 
                for linktag, field, refobjtxt in zip(linktags, 
                                                        fields, 
                                                        refobjtxts)]
    lines.pop(0)
    lineswithtitle = [objkey, '='*len(objkey)] + lines
    lineswithtitle = putfilenameontop(idf, lines)
    html = '<br>'.join(lineswithtitle)
    return html
    
def makenodeobjtxts(idf, nodeobjlist):
    """html of all the mentioned nodes"""
    idfobjectkeys = idf_helpers.idfobjectkeys(idf)
    nodeobjtxts = []
    for nodeobjs in nodeobjlist:
        if nodeobjs:
            nodeobjtxtlist = []
            for nodeobj in nodeobjs:
                keyindex = idfobjectkeys.index(nodeobj.key.upper())
                idfobjects = idf.idfobjects[nodeobj.key.upper()]
                objindex = idfobjects.index(nodeobj)
                url = "../%s/%s" % (keyindex, objindex)
                nodeobjtxt = '%s->%s' % (nodeobj.key, nodeobj.Name)
                linktag = '%s%s %s-><a href=../%s>%s</a>' % (aspace, 
                                                abullet, 
                                                nodeobj.key, 
                                                url, nodeobj.Name)
                nodeobjtxtlist.append(linktag)
            nodeobjtxtlist.insert(0, "%s this node connects to:" % (abullet, ))
            nodeobjtxtlist.insert(0, "")
            sepr = "<br> %s " % (aspace, )
            atxt = sepr.join([item for item in nodeobjtxtlist])
            nodeobjtxts.append(str(atxt))
        else:
            nodeobjtxts.append("")
    return nodeobjtxts
        

@route('/idf/<idfindex:int>/<keyindex:int>/nodementions/<objindex:int>')
def theidfobjectnodementions(idfindex, keyindex, objindex):
    idf, edges = eppystuff.an_idfedges(idfindex)
    objkeys = idf_helpers.idfobjectkeys(idf)
    objkey = objkeys[keyindex]
    idfobjects = idf.idfobjects[objkey]
    idfobject = idfobjects[objindex]
    fields = idfobject.objls
    values = idfobject.obj
    nodekeys = eppystuff.getnodekeys()
    nodeobjs = []
    for value, fieldname in zip(values, fields):
        nodeobj = idf_helpers.getobjectswithnode(idf, nodekeys, value)
        nodeobjs.append(nodeobj)
    valuesfields = [(value, field) for value, field in zip(values, fields)]
    urls = ["../%s/%s" % (objindex, field) for field in fields]
    linktags = ['<a href=%s>%s %s %s</a>' % (url, i, abullet, value,)
                    for i, (url, value) in enumerate(zip(urls, values))]
    nodeobjtxts = makenodeobjtxts(idf, nodeobjs)
    lines = ["%s %s %s %s" % (linktag, aspace, field, refobjtxt) 
                for linktag, field, refobjtxt in zip(linktags, 
                                                        fields, 
                                                        nodeobjtxts)]
    lines.pop(0)
    lineswithtitle = [objkey, '='*len(objkey)] + lines
    lineswithtitle = putfilenameontop(idf, lines)
    html = '<br>'.join(lineswithtitle)
    return html

@route('/idf/<idfindex:int>/<keyindex:int>/objfunctions/<objindex:int>')
def theidfobjectobjfunctions(idfindex, keyindex, objindex):
    idf, edges = eppystuff.an_idfedges(idfindex)
    objkeys = idf_helpers.idfobjectkeys(idf)
    objkey = objkeys[keyindex]
    idfobjects = idf.idfobjects[objkey]
    idfobject = idfobjects[objindex]
    fields = idfobject.objls
    values = idfobject.obj
    valuesfields = [(value, field) for value, field in zip(values, fields)]
    urls = ["../%s/%s" % (objindex, field) for field in fields]
    linktags = ['<a href=%s>%s %s %s</a>' % (url, i, abullet, value,) 
                    for i, (url, value) in enumerate(zip(urls, values))]
    lines = ["%s %s %s" % (linktag, aspace, field) 
                for linktag, field in zip(linktags, fields)]
    # ---
    lines.pop(0)
    lineswithtitle = [objkey, '='*len(objkey)] + lines
    funcsresults = bunch__functions(idfobject)
    funclines = funcsresults2lines(funcsresults)
    lineswithtitle = putfilenameontop(idf, lineswithtitle)
    html = '<br>'.join(lineswithtitle + ["<hr>", ] + funclines)
    return html

@route('/idf/<idfindex:int>/<keyindex:int>/refferingobjs/<objindex:int>')
def theidfobjectrefferingobjs(idfindex, keyindex, objindex):
    idf, edges = eppystuff.an_idfedges(idfindex)
    objkeys = idf_helpers.idfobjectkeys(idf)
    objkey = objkeys[keyindex]
    idfobjects = idf.idfobjects[objkey]
    idfobject = idfobjects[objindex]
    fields = idfobject.objls
    values = idfobject.obj
    valuesfields = [(value, field) for value, field in zip(values, fields)]
    urls = ["../%s/%s" % (objindex, field) for field in fields]
    linktags = ['<a href=%s>%s %s %s</a>' % (url, i, abullet, value,) 
                    for i, (url, value) in enumerate(zip(urls, values))]
    lines = ["%s %s %s" % (linktag, aspace, field) 
                for linktag, field in zip(linktags, fields)]
    # ---
    lines.pop(0)
    lineswithtitle = [objkey, '='*len(objkey)] + lines
    referingobjsline = getreferingobjs(idfindex, idfobject)
    lineswithtitle = putfilenameontop(idf, lineswithtitle)
    html = '<br>'.join(lineswithtitle + ["<hr>", ] + [referingobjsline, ])
    return html

@route('/idf/<idfindex:int>/<keyindex:int>/mentioningobjs/<objindex:int>')
def theidfobjectmentioningobjs(idfindex, keyindex, objindex):
    idf, edges = eppystuff.an_idfedges(idfindex)
    objkeys = idf_helpers.idfobjectkeys(idf)
    objkey = objkeys[keyindex]
    idfobjects = idf.idfobjects[objkey]
    idfobject = idfobjects[objindex]
    fields = idfobject.objls
    values = idfobject.obj
    valuesfields = [(value, field) for value, field in zip(values, fields)]
    urls = ["../%s/%s" % (objindex, field) for field in fields]
    linktags = ['<a href=%s>%s %s %s</a>' % (url, i, abullet, value,) 
                    for i, (url, value) in enumerate(zip(urls, values))]
    lines = ["%s %s %s" % (linktag, aspace, field) 
                for linktag, field in zip(linktags, fields)]
    # ---
    lines.pop(0)
    lineswithtitle = [objkey, '='*len(objkey)] + lines
    mentioningobjsline = getmentioningobjs(idfindex, idfobject)
    html = '<br>'.join(lineswithtitle + ["<hr>", ] + ['Mentioning Objects', mentioningobjsline, ])
    return html

@route('/idf/<idfindex:int>/<keyindex:int>/<objindex:int>/<field>')
def theidfobjectfield(idfindex, keyindex, objindex, field):
    idf, edges = eppystuff.an_idfedges(idfindex)
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    idfobject = idfobjects[objindex]
    html = "%s <- %s . <i>Editable in the future</i>"  % (idfobject[field], field)
    return codetag(html)

@route('/idf/<idfindex:int>/<keyindex:int>/<objindex:int>/<field>/iddinfo')
def theiddinfo(idfindex, keyindex, objindex, field):
    idf, edges = eppystuff.an_idfedges(idfindex)
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    idfobject = idfobjects[objindex]
    iddinfo = idfobject.getfieldidd(field)
    lines = []
    for key, val in iddinfo.items():
        if isinstance(val, set):
            lines.append('%s = %s' % (key, val))
        elif len(val) == 1:
            if val[0] == '':
                lines.append('%s' % (key, ))
            else:
                lines.append('%s = %s' % (key, val[0]))
        else:
            lines.append('%s = %s' % (key, val))
    heading = '%s%s%s' % (idfobject.key.upper(), abullet, field)
    heading = heading.strip()
    lines.insert(0, "=" * (len(heading)-len(abullet)+1))
    lines.insert(0, heading)
    html = '<br>'.join(lines)
    return codetag(html)

@route('/idf/<idfindex:int>/<keyindex:int>/hvacprevnext/<objindex:int>')
def theidfobjectmentioningobjs(idfindex, keyindex, objindex):
    """hvac previous and next object"""
    idf, edges = eppystuff.an_idfedges(idfindex)
    objnames = idf_helpers.idfobjectkeys(idf)
    objname = objnames[keyindex]
    idfobjects = idf.idfobjects[objname]
    idfobject = idfobjects[objindex]
    from eppy import walk_hvac
    nextnodes = walk_hvac.nextnode(edges, idfobject.Name)
    nextobjs = [idf_helpers.name2idfobject(idf, nnode) for nnode in nextnodes]
    keyobjids = [eppystuff.idfobjectindices(idf, nobj) for nobj in nextobjs]
    nurls = ["../../%s/%s" % (key_id, obj_id) for key_id, obj_id in keyobjids]
    nextlinks = ['<a href=%s>%s</a>' % (url, nnode)
                    for nnode, url in zip(nextnodes, nurls)]
    firstlines = [
    "HVAC connections from %s named '%s'" % (objname, idfobject.Name),
    "",
    "Next Objects",
    ]
    betweenlines = ["", "Previous Objects"]
    prevnodes = walk_hvac.prevnode(edges, idfobject.Name)
    prevobjs = [idf_helpers.name2idfobject(idf, pnode) for pnode in prevnodes]
    keyobjids = [eppystuff.idfobjectindices(idf, nobj) for nobj in prevobjs]
    try:
        purls = ["../../%s/%s" % (key_id, obj_id) 
                    for key_id, obj_id in keyobjids]
    except TypeError as e:
        purls = []
    prevlinks = ['<a href=%s>%s</a>' % (url, pnode)
                    for pnode, url in zip(prevnodes, purls)]
    # image snippet
    onlythis = [idfobject.Name, ] + nextnodes + prevnodes
    trimmed = eppystuff.trimedges(edges, onlythis)
    from eppy.useful_scripts import loopdiagram
    imgname = '%s_%s_%s' % (idfindex, keyindex, objindex)
    eppystuff.save_imagesnippets(IMGFOLDER,imgname, trimmed)
    imgline = ['<img src="../../../../../static/%s.png" alt="snippet">' % (imgname, )]
    html = '<br>'.join(firstlines + nextlinks + betweenlines + prevlinks + imgline)
    return html
    
    
run(host='localhost', port=8080, debug=True)

try:
    run(host='0.0.0.0', port=argv[1]) # to run on heroku
except IndexError as e:
    run(host='localhost', port=8080, debug=True) # runs locally

