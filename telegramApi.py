#!/usr/bin/env python3
from telethon import TelegramClient, events
from datetime import timedelta
import sys

# EDIT HERE ↓
api_id = api_id
api_hash = 'api_hash'
workers = 4
session_name = 'user_name'
# EDIT HERE ↑

def printDialog(d):
  print (d.id, " ", d.name," ", d.pinned)

def findDialog(dialogs, id):
  for d in dialogs:
    if d.id == id:
      return d
  return None

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

class DelayedDownload:
  """A class to store the data, for other methods to download media later"""
  message=None
  id=1
  def __init__(self, _id, msg):
    self.id = _id
    self.message = msg

# create connection
client = TelegramClient(session_name, api_id, api_hash, update_workers=workers, spawn_read_thread=True)
client.start()

me = client.get_me()
#get dialogs
dialogs = client.get_dialogs(limit=100)

print ("chats loaded. (" , len(dialogs), ")")
#print chats
for d in dialogs:
  printDialog(d)
get = int(input("Please Enter Chat ID: "))
selectedDialog = findDialog(dialogs, get)
if selectedDialog == None:
  print ("Unknown Chat ID!")
  exit(1)

print ("selected: ", selectedDialog.name, 'retriving chat!')

chat = client.get_messages(selectedDialog, limit=2000000)
print("retrived ", len(chat), " Messages.")

toDL = []#list of messages, where media should be downloaded

fout = open('out/chat.xml','x')
fout.write('<chat>\n')
for c in chat:
  dl = saveMessage(c, fout, len(toDL),me.id)
  if dl != None:
    if dl.media != None:
    #here is something to download later
      toDL.append(DelayedDownload(len(toDL),c))
fout.write('</chat>\n')
fout.close()

print('Chat structure stored. Downloading Media - this may take a while!')
for dl in toDL:
  print ('.', end='')
  client.download_media(dl.message, "out/media/" + str(dl.id))
print('\n', len(toDL), " Media Files Downloaded.")
print ('End.')
