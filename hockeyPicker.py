#!/usr/bin/python
 
import sys
import csv
import re
import urllib2
import sqlite3
from collections import defaultdict

""" Hockey Players Team rank table builder in SQLLITE
    input from output.csv will pull ratings from users and build rank table    


scrapeSPD.py - pulls name from website
hockeyPicker.py - pulls ratings from outputwithRankings.csv - only need to run when ratings change
hockeyTeamBuilerrev2.py - picks team and builds web page

"""

def create_connection(db_file):
  """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
  """
  try:
    conn = sqlite3.connect(db_file)
    return conn
  except Error as e:
    print(e)
 
  return None
 
 
def select_all_tasks(conn):
  """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
  """
  cur = conn.cursor()
  cur.execute("SELECT * FROM users")
  #cur.execute("SELECT * FROM users WHERE id > 2000 AND waitlist >=1")
 
  rows = cur.fetchall()
  with open('output.csv', 'wb') as f:
    writer = csv.writer(f)
    #writer.writerow(['Column 1', 'Column 2', ...])
    writer.writerows(rows) 
  #for row in rows:
    #print(row)
 
 
def select_task_by_priority(conn):
  """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
  """
  cur = conn.cursor()
  cur.execute("SELECT * FROM users")
  #cur.execute("SELECT * FROM users WHERE id < 2000 AND waitlist >=1")
  rows = cur.fetchall()
  print len(rows) 
  with open('output.csv', 'ab') as f:
    writer = csv.writer(f)
    #writer.writerow(['Column 1', 'Column 2', ...])
    writer.writerows(rows)
  
  #for row in rows:
    #print(row)
 
def hockeyrankingCSV(conn):
  rankingfile = 'outputwithRankings.csv'
  hockeyinput = []
  columns = defaultdict(list)
  with open(rankingfile,'rb') as f:
    reader = csv.DictReader(f)
    for row in reader:
      for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

  #print(columns['id'])
  #print(columns['rank'])

  cur = conn.cursor()
  cur.executescript('''
   DROP TABLE IF EXISTS rank;


   CREATE TABLE rank (
   id	INTEGER NOT NULL PRIMARY KEY UNIQUE,
   rank INTEGER, 
   FOREIGN KEY(id) REFERENCES users(id)
   ); 
 
  ''')

  sql = ''' INSERT OR IGNORE INTO rank(id,rank)
              VALUES(?,?) ''' 
  x = len(columns['id'])
  for i in range(0,x):
    hockeyinput = (columns['id'][i]),(columns['rank'][i])
    try:
      cur.execute(sql, hockeyinput)
      #print hockeyinput
    except:
      print "Something is wrong."
      continue
      
def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  '''
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]
  '''  
  database = "spd.sqlite"

    # create a database connection
  conn = create_connection(database)
  with conn:
    print "Your hockey rankings functions are running"
    hockeyrankingCSV(conn)

  
    

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  
if __name__ == '__main__':
  main()
