from bottle import route, run
import eppystuff
# idf = eppystuff.makeanidf()

@route('/hello')
def hello():
    return "Hello World!"

@route('/idf')
def idf():
    idf = eppystuff.getidf()
    lines = idf.idfstr().splitlines()
    return '<br>'.join(lines)

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
    

run(host='localhost', port=8080, debug=True)

