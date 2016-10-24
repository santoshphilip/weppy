from bottle import route, run
import eppystuff

@route('/hello')
def hello():
    return "Hello World!"

@route('/idf')
def idf():
    idf = eppystuff.makeanidf()
    lines = idf.idfstr().splitlines()
    return '<br>'.join(lines)

run(host='localhost', port=8080, debug=True)