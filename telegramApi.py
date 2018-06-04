#!/usr/bin/env python3
from telethon import TelegramClient, events
from datetime import timedelta
import configparser
import sys
import os

def printDialog(id , d):
#  print (d.id, " ", d.name," ", d.pinned)
  print('{0:2d} | {1:14d} | {2:30} | {3:1}'.format(id, d.id,d.name,d.pinned))

def saveMessage(message, file, dlid, ownid):
#  print(message)
  file.write('  <message>\n    <date>')
  file.write(message.date.strftime("%s"))
  file.write('</date>\n    <msg>')  
  file.write(message.message)
  file.write('</msg>\n    <me>')
  file.write(str(int(ownid==message.from_id)))
  file.write('</me>\n')
  #dl and write media if exist
  out = None
  if message.media != None:
    file.write('    <media>')
    file.write(str(dlid))
    file.write('</media>\n')
    out = message

  file.write('  </message>\n')
  return out

def createFolder(path):
  if not os.path.exists(path):
    os.makedirs(path)

class DelayedDownload:
  """A class to store the data, for other methods to download media later"""
  message=None
  id=1
  def __init__(self, _id, msg):
    self.id = _id
    self.message = msg


#==================================
#MAIN program

#read config
try:
  config = configparser.ConfigParser()
  config.read('config.ini')
  api_id = int(config.get('Main','api_id'))
  api_hash = config.get('Main','api_hash')
  workers = int(config.get('Main','workers'))
  session_name = config.get('Main','user')
except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
  print('invalid config.ini')
  exit(3)

# create connection
client = TelegramClient(session_name, api_id, api_hash, update_workers=workers, spawn_read_thread=True)
client.start()

me = client.get_me()
#get dialogs
dialogs = client.get_dialogs(limit=100)

print ("chats loaded. (" , len(dialogs), ")")
#print chats
id = 0

#table header
print ('ID | Internal ID    | Username                       | pinned\n———+————————————————+————————————————————————————————+———————')
#content
for d in dialogs:
  printDialog(id,d)
  id = id+1
get = int(input("Please Enter Chat ID: "))
if get < 0 or get >= id:
  print ("Unknown Chat ID!")
  exit(1) 

selectedDialog = dialogs[get]

print ("selected: ", selectedDialog.name, 'retriving chat!')

chat = client.get_messages(selectedDialog, limit=2000000)
print("retrived ", len(chat), " Messages.")

toDL = []#list of DelayedDownload

createFolder('out/')

while True:
  try:
    fout = open('out/chat.xml','x')
    break
  except FileExistsError:
    get = input("Override out/chat.xml [y/n]?")
    if get == 'y' or get == 'Y':
      #delete
      os.remove('out/chat.xml')
    elif get == 'n' or get == 'N':
      #exit
      print ("Bye.")
      exit(2)

fout.write('<chat>\n')
for c in chat:
  dl = saveMessage(c, fout, len(toDL),me.id)
  if dl != None:
    if dl.media != None:
    #here is something to download later
      toDL.append(DelayedDownload(len(toDL),c))
fout.write('</chat>\n')
fout.close()

createFolder('out/media/')
print('Chat structure stored. Downloading Media - this may take a while!')
for dl in toDL:
  print ('.', end='')
  client.download_media(dl.message, "out/media/" + str(dl.id))
print('\n', len(toDL), " Media Files Downloaded.")
print ('End.')
