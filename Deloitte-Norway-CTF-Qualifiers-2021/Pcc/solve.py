#!/usr/bin/python3
import math
import socket
import re
import time

HOST = '136.243.68.77'
PORT = 17001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
data = ""

# Receiving initial communication:
while 1==1:
    tmp = s.recv(1024)
    data += str(tmp)
    print(data)
    if "original position: " in str(data):
        break


# Regex-matching and extracting coordinates:
# First dataload is a special case as it includes 2 coordinate positions
# Regex breakdown:
# re.findall -> gives back a list of all substrings that matches our string, or the specified capture groups
# ([0-9]+) -> the parentheses marks what is in them as a capture group (what we want to process.) [0-9] == match numbers between 0-9, and + means "at least one time"
parentheses = re.findall("\(x: ([0-9]+), y: ([0-9]+)\)", str(data))

x1=int(parentheses[0][0])
y1=int(parentheses[0][1])
x2=int(parentheses[1][0])
y2=int(parentheses[1][1])

# 2d point-point Distance calculation
# sqrt( (x2 - x1)^2 + (y2 - y1)^2)
result= ((((x2 - x1 )**2) + ((y2-y1)**2) )**0.5)

# Sending first result:
s.send((str(round(result)) + "\n").encode())

# Looping for all subsequent results:
data = ""
while 1==1:
    print("RECEIVING NEXT LINE\n")
    tmp = s.recv(512)
    data += (str(tmp)).replace("b\'", "")
    print(str(data))
    if "original position: " in (str(data)):
        # Saving previous coords:
        x1 = x2
        y1 = y2

        # extracting new coordinates - same as before
        parentheses = re.findall("\(x: ([0-9]+), y: ([0-9]+)\)", str(data))
        x2=int(parentheses[0][0])
        y2=int(parentheses[0][1])

        # Calculating distance - same as before
        result= ((((x2 - x1 )**2) + ((y2-y1)**2) )**0.5)

        print("\n\n\n SENDING RESULT\n" + str(result) + ":" + str(round(result)) + "\n\n\n")
        s.send((str(round(result)) + "\n").encode())
        data = ""
    elif "Processing error" in str(data): # response if answer sent is wrong
       break
    elif "Timeout in response..." in str(data): # response if our answer was too slow (very low threshold)
        break
    elif "flag" in str(data):
        break

# Closing socket like a nice person
s.close()

