#!/usr/bin/python

import sys
import re
import urllib2
import sqlite3
from bs4 import BeautifulSoup

""" Hockey Players Team Picker program 1 of three
scrapeSPD.py - pulls name from website
hockeyPicker.py - pulls ratings from output.csv - only need to run when ratings change
hockeyTeamBuilerrev2.py - picks team and builds web page

Define the extract_names() function below and change main()
to call it.

"""

def createdb(player_ids, playings, pnames):
  """
 
  """
  # +++your code here+++
  conn1 = sqlite3.connect('spd.sqlite')
  cur1 =  conn1.cursor() 
  hockeyinput=[]
  sql1 = ''' INSERT OR IGNORE INTO users(id,name,status,waitlist)
              VALUES(?,?,?,?) ''' 
  hockeyinput.insert(0,int(player_ids))
  hockeyinput.insert(1,pnames)
  hockeyinput.insert(2,playings)
  if playings == 'drop' and int(player_ids) <= 1900:
    hockeyinput.insert(3,1)
  else:
    hockeyinput.insert(3,0)
  #hockeyinput
  try:
    cur1.execute(sql1, hockeyinput)
    print "Sucess. Fulltimers were updated."
  except:
    print "Something went wrong with Full timers. ", hockeyinput
  conn1.commit()
  conn1.close() 
  return

def waitlistrankings(subnames,subrank):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # +++your code here+++
  conn2 = sqlite3.connect('spd.sqlite')
  cur2 =  conn2.cursor() 
  print subnames,subrank
  try:
    #cur2.execute("UPDATE users SET waitlist = subrank WHERE name = snames")
    cur2.execute('UPDATE users SET waitlist = ? WHERE name = ?', [subrank, subnames])
    print "Sucess. Sub ranking were updated."
  except:
    print "Something went wrong with Sub Rankings. "
  conn2.commit()
  conn2.close() 
  return




def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  #BeautifulSoup([your markup], "html.parser")
  player_id=[]
  player_ids=[]
  sub_id=[]
  sub_ids=[]
  subplaying=[]
  subplayings=[]
  subpnames=[]  
  playing=[]
  playings=[]
  pnames=[]
  waitlist=[]
  waitlists=[]
  playerstatus={}
  filename = './form.txt'
  count = 0
  urlcount = 0
  subrank = 0
  #url = "http://www.nezumi.us/SPD/fulltime/status.php"
  #urls = ["http://www.nezumi.us/SPD/subs/signup.php", "http://www.nezumi.us/SPD/fulltime/status.php"] 
  urls = ["http://www.nezumi.us/SPD/fulltime/status.php", "http://www.nezumi.us/SPD/subs/signup.php"]  
  for url in urls:
    urlcount += 1
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read(),"html.parser")
    cities = soup.find_all('form')
    states = soup.find_all('td')
    # used for pulling the lines zips = soup.find_all('li')
    zips = soup.find_all('td')
    '''
  		cities pulls the USER ID from the form tag on the URL.  Also on that line is the player status to add or drop
  		states pulls the USER Name from the table data row when there is a name in that row.  We have to skip a TD because two are read and
  		only one contains the name. 
    '''  
    with open(filename, 'w') as handle:
      for city in cities:
        #print city
        #handle.write(str(city)+ '\n')
        line = str(city)
        player_id = re.findall(r'([0-9]+)',line)
        player_ids.extend(player_id)
        
        # next Section finds add or drop and automatically puts it into playing
        
        if re.findall(r'type="hidden" value="([ad]\w+)"',line):
          playing = re.findall(r'type="hidden" value="([ad]\w+)"',line)
          playings.extend(playing)
      
        if player_id:
          #print player_id, playing
          tempOne = str(player_id) + ' ' + str(playing) + '\n'
          print tempOne
          handle.write(tempOne)
      #handle.write(' '.join((str(len(player_ids)), str(len(player_ids)))))
      
    for state in states:
      str_state = str(state)
      pname = re.findall(r'([A-Za-z]+ [A-Za-z]+)',str_state)
      if count % 2:
        pnames.append(pname[1])
      count +=1
    #print "These are the waitlisted subs: "
    '''
    # start to pull waitlisted checkins
    for sub in cities:
      line = str(sub)
      if urlcount == 2:
        sub_id = re.findall(r'([0-9]+)',line)
        sub_ids.extend(sub_id)
        if re.findall(r'name=action value=([d]\w+)',line):
          subplaying = re.findall(r'name=action value=([d]\w+)',line)
        #playing = ['drop'] 
        #else:
          #playing = ['add']
          subplayings.extend(subplaying)
      
        if sub_id:
          print sub_id, subplaying
        print len(sub_ids), len(subplayings)
      
      #print city
    for state in states:
      str_state = str(state)
      if urlcount == 2:
        subpname = re.findall(r'([A-Za-z]+ [A-Za-z]+)',str_state)
        if count % 2:
          #print pname[1]
          subpnames.append(subpname[1])
        count +=1
  
    '''
    # this is required to get the name on the sub list page
    
    for zip in zips:
      str_zip = str(zip)
      if urlcount == 2:
        waitlist = re.findall(r'class="in">([A-Za-z]+ [A-Za-z]+)',str_zip)
        try:
         #print "you are right here: ", waitlist[0]
         waitlists.append(waitlist[0])
        except:
          continue 
      else:
        continue
    
      
  conn = sqlite3.connect('spd.sqlite')
  cur =  conn.cursor()
  cur.executescript('''
   DROP TABLE IF EXISTS users;


   CREATE TABLE users (
   id	INTEGER NOT NULL PRIMARY KEY UNIQUE,
   name TEXT UNIQUE,
   status TEXT,
   waitlist INTEGER 
   ); 
 
  ''')    
  numid = len(player_ids)
  #with open(filename, 'a') as f:
  for x in range(0,numid):   
    #print player_ids[x], playings[x], pnames[x]
    createdb(player_ids[x], playings[x], pnames[x]);
  
  # for loop to pull sub names who are checked in and have been add in already
    
  for subnames in waitlists:
    subrank = 1
    waitlistrankings(subnames,subrank)

  
if __name__ == '__main__':
  main()
