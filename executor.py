# -*- coding: utf-8 -*-  

#import model
import json
import os

import threading
import time
import cx_Oracle

#############

con = cx_Oracle.connect('wsyj/wsyj@127.0.0.1/test')   # ToDo: The connection string should be placed in a configuration file.
exitFlag = 0
threads = []

###
class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print "Starting " + self.name
        process_data(self.name)
        print "Exiting " + self.name

def process_data(threadName):
    global con

    while not exitFlag:
        #print "doing sth."
        # No! You should not remove the time.sleep here! To place it at the
        # beginning of the while could spare us some uncomfortable "if ...
        # time.sleep ... continue" and use some compact "if ... continue"
        # instead.
        time.sleep(1)   # 1 second
        
        # fetch a job
        cur = con.cursor()
        cur.execute('select * from as_tasks order by id')
        row = cur.fetchone()
        print row

        if row is None:
            print "No tasks yet."
            continue

        task_id = row[0]
        sql = row[1]
        
        # execute the job
        try:
            print 'going to execute sql:"%s"' % sql
            cur.execute(sql)
        except cx_Oracle.DatabaseError, msg:
            #logger.log(logging.WARN, "(remote) %s" % msg)  # ToDo: 引入logger
            print msg

        # delete the job
        cur.execute('delete from as_tasks where id = %d' % task_id)
        con.commit()

        
###

def create_threads():
    global threads
    threadList = ["Thread-1"]
    nameList = ["One", "Two", "Three", "Four", "Five"]

    threadID = 1

    # Create new threads
    for tName in threadList:
        thread = myThread(threadID, tName)
        thread.start()
        threads.append(thread)
        threadID += 1

def notify_end(threads):
    global exitFlag

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print "Exiting Main Thread"


def init_tasks():
    global con
    cur = con.cursor()
    cur.execute("insert into as_tasks (description) values('hi')")
    con.commit()
    cur.close() # Careful! con or cur!


def main():
    global threads
    init_tasks()
    create_threads()

    while True:
        s = raw_input()
        if "q" == s or "quit" == s:
            break

    notify_end(threads)

if __name__ == '__main__':
    main()