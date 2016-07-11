# -*- coding: utf-8 -*-  

from bottle import Bottle, run, debug, template, route, static_file, request

import cx_Oracle
import json
import os

import time

app = Bottle()
debug(True) 
    
#############

con = cx_Oracle.connect('wsyj/wsyj@127.0.0.1/test')   # ToDo: The connection string should be placed in a configuration file.

def getApp():
    # called by index.wsgi
    return app
########################################################################################
#                                                               utility  <start>
@route('/app-debug.apk')
@app.route('/app-debug.apk')
def help():
    filename = 'app-debug.apk'
    #return static_file(filename, root='.', mimetype='application/vnd.android', download=filename)  #静态文件    
    return static_file(filename, root='.', mimetype='application/vnd.android.package-archive', download=filename)  #静态文件


@route('/')
@app.route('/')
def hello():
    return "Hello, world! - Bottle<br/>Click <a href=\"app-debug.apk\">here</a> to download GradeMonger(tentative)."
#                                                               utility  <end>

@route('/add_task', method = 'POST')
def add_task():
    global con

    print request.forms
    print str(request.forms)

    #for k in request.forms:
    #    print k
    #    print request.forms[k]

    key_for_task = "task"
    if key_for_task in request.forms:
        cur = con.cursor()
        cur.execute('insert into as_tasks (description) values(%s)' % (request.forms.get(key_for_task)))
        con.commit()

        return 'Got it.'
    else:
        return "'%s' missing" % key_for_task

def main():
    run(host='127.0.0.1', port=8080, reloader=True)

if __name__ == '__main__':
    main()