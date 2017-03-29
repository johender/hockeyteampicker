#!/usr/bin/python

import sys
import csv
import re
import urllib2
import sqlite3
from collections import defaultdict
import random
import HTML
from datetime import date


""" Hockey Players Team Picker


scrapeSPD.py - pulls name from website
hockeyPicker.py - pulls ratings from output.csv - only need to run when ratings change
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
 
 
def pullFullTimePlayers(conn):
  """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
  """
  ranks =[]
  cur = conn.cursor()
  #cur.execute("SELECT * FROM users")
  #cur.execute("SELECT users.id,users.name,rank.rank FROM users INNER JOIN rank ON users.id=rank.id WHERE users.id < 2000 AND users.waitlist >=1")
  cur.execute("SELECT users.id,users.name,rank.rank FROM users INNER JOIN rank ON users.id=rank.id WHERE users.waitlist >=1")
  rows = cur.fetchall() 
  return rows 

def pullSubPlayers(conn):
  ranks =[]
  cur = conn.cursor()
  #cur.execute("SELECT * FROM users")
  cur.execute("SELECT users.id,users.name,rank.rank,users.waitlist FROM users INNER JOIN rank ON users.id=rank.id WHERE users.id > 2000 AND users.waitlist >=1")
  rows = cur.fetchall() 
  return rows 

def satandsun(input):
  d = input.toordinal()
  last = d + 7
  sunday = last - (last % 7)
  saturday = sunday + 6
  nextskate = str(date.fromordinal(sunday))
  #print date.fromordinal(saturday)
  return nextskate
  
def createHTML(tabledata):
  # open an HTML file to show output in a browser  
  sunskate = satandsun(date.today())
  HTMLFILE = 'SPD_Teams.html'
  f = open(HTMLFILE, 'w')
  '''
  table_data = [
        ['Smith',       'John',         30],
        ['Carpenter',   'Jack',         47],
        ['Johnson',     'Paul',         62],
    ]
  '''
  htmlcode = HTML.table(tabledata,
      header_row=['Dark Team',   'White Team'])
  print htmlcode
  f.write('<p>Hockey Night in Heartland, %s </p>' % sunskate)
  f.write(htmlcode)
  f.write('<p>')
  print '-'*79
  return
  
def rankPlayers(roster):
  highestrank = 0
  lowesetrank = 0
  randomness = random.randint(0,1)
  randomplayer3 = random.randint(0,1)
  randomaveplay = random.randint(0,25)
  counter = 1
  darks=[]
  whites=[]
  darkstotal = 0
  whitestotal = 0
  playerrank={}
  sortedplayerrank={}
  players=[]
  totalplayers = 0
  for line in roster:
    playerrank[line[1]] = int(line[2])
  print "You have ",len(playerrank)," players."
  totalplayers = len(playerrank)
  totaldarkplayers = totalplayers/2
  print totaldarkplayers
  for key, value in sorted(playerrank.items(), key=lambda t:t[1], reverse=True):
    #print "%s: %s" % (key, value)
    if randomness == 1 and counter == 1:
      darks.append(key)
      counter += 1
      darkstotal += value
      #print "you are here"
    elif randomness == 0 and counter == 1:
      whites.append(key)
      #print "you are there"
      counter += 1
      whitestotal += value
    elif randomness == 1 and counter == 2:
      whites.append(key)
      counter += 1
      #print "you are here"
      whitestotal += value
    elif randomness == 0 and counter == 2:
      darks.append(key)
      #print "you are there"
      counter += 1
      darkstotal += value
    elif counter == 3:
      if randomplayer3 == 0:
        darks.append(key)
        counter += 1
        darkstotal += value
        fourthplayer = True
      else:
        whites.append(key)
        counter += 1
        whitestotal += value
        fourthplayer = False
    elif counter == 4:
      if fourthplayer == True:
        whites.append(key)
        counter += 1
        whitestotal += value
      else:
        darks.append(key)
        counter += 1
        darkstotal += value
    elif  4 < counter < 19:
      players.append(key)
      counter += 1
    elif counter == 19:
      darks.append(key)
      counter += 1
    elif counter == 20:
      whites.append(key)
      counter += 1  
    elif counter == 21:
      darks.append(key)
      #print key
      counter += 1
    elif counter == 22:
      whites.append(key)
      counter += 1
    elif counter == 23:
      darks.append(key)
      #print key
      counter += 1
    elif counter == 24:
      whites.append(key)
      counter += 1
      #print "Here is right here ",key  
    else:
      counter += 1    

  print "Step 1 complete"
  print darks
  print whites
  
  while len(darks) !=  totaldarkplayers:
    print len(darks), totaldarkplayers
    print "Step 2 complete"
    #darks.append('Steve Keranen')
    #darks.append('Rob Kowalski')
    draft1 =random.choice(players)
    if draft1 not in darks:
      darks.append(draft1)
   
  for y in players:
    if y not in darks:
      whites.append(y)
      
  
  print "     Darks                 Whites"
  darkstotal = 0
  whitestotal = 0
  for k in darks:
    if k in playerrank:
      darkstotal += playerrank[k]
      print k, playerrank[k]
  for k in whites:
    if k in playerrank:
      whitestotal += playerrank[k]    
  darkstotal = 0
  whitestotal = 0
  

  for a in darks:
    darkstotal = darkstotal + int(playerrank[a])
    print a, playerrank[a]
  print "White Team"
  for b in whites:
    whitestotal = whitestotal + int (playerrank[b])
    #print b
  #print "Darks Skill: ",darkstotal, "Whites Skill: ",whitestotal 
  print "Step 3 complete"
  
  newHtmlList=[]
  #print "Here are the darks:", darks, "Total points: ", darkstotal
  #print "Here are the whites:", whites, "Total points: ", whitestotal
  #print random.choice(players)
  lengthDark = len(darks)
  lengthWhite = len(whites)
  
  darks = sorted(darks)
  whites = sorted(whites)
  print "This is the sorted Dark: ", darks
  print "This is the sored White: ", whites
  
  if (lengthDark >> lengthWhite):
    print "the length of darks is ",len(darks)
    for jh in range(0,len(darks)):
      try:
        newHtmlList.append([darks[jh],whites[jh]])
      except:
        newHtmlList.append([darks[jh],''])
    newHtmlList.append([darkstotal, whitestotal])
  
  if (lengthDark << lengthWhite):
    print "the length of darks is class b ",len(darks)
    for jh in range(0,len(whites)):
      try:
        newHtmlList.append([whites[jh],darks[jh]])
      except:
        newHtmlList.append([whites[jh],''])
    newHtmlList.append([whitestotal, darkstotal])  
  print "Dark Team", darks
  print "White Team", whites
  print newHtmlList
  createHTML(newHtmlList)
  

  
  '''
  for z in range(0,12):
    darkstotal = darkstotal + int(playerrank[darks[z]])
    whitestotal = whitestotal + int (playerrank[whites[z]])
    print z+1,". ",darks[z],  ": ",  playerrank[darks[z]]," : ", whites[z], ": ", playerrank[whites[z]]
    
  print "Darks Skill: ",darkstotal, "Whites Skill: ",whitestotal
  '''
    	
  return

 
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
    print("You have chose to build the team")
    # pulling the roster from full timer players
    roster = pullFullTimePlayers(conn)
    
    print "You have made it out of the function and have ", len(roster), " players."
    '''
    if len(roster) < 22:
      subroster = pullSubPlayers(conn)
      print subroster
    if len(roster) >= 22:
      for players in roster:
        print players[0],players[1], players[2]
    '''
    rankPlayers(roster)
    
   
   
   
   
if __name__ == '__main__':
  main()
