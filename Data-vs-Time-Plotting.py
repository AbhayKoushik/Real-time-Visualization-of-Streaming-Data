from socket import *
import random
from collections import deque
import numpy as np
import time
import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Get IP address
from urllib.request import urlopen
import re
def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    # data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'

    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

# String to float converter
s2f = lambda s: float("".join(i for i in s if 46 <= ord(i) < 58 and ord(i)!=47))
       
    
# Initialization of Parameters for graphing
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

myFmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(myFmt)

# Add labels
plt.title('EEG Over Time')
plt.xlabel('Time - HH:MM:SS')
plt.ylabel('EEG')
plt.ion()

# next create a socket object
s = socket()
print("Socket successfully created")
port = 5601

# WindowSize in seconds
windowSize = 15
viswinSize = 10

#bind to the port
s.bind((getPublicIp(), port))
print("socket binded to %s and port %s" %(getPublicIp(),port))

# put the socket into listening mode
i = 1 # counter
eeg = deque([0])
eegx = deque([datetime.now()])

# plotting function
def realtimePlot():
    ax.set_xlim([eegx[-1]-timedelta(seconds=viswinSize), eegx[-1]])
    ax.xaxis.set_major_formatter(myFmt)
    plt.plot(eegx,eeg,linestyle='-',color='r') # datetime.now(),eeg[-1],c='r'
    plt.gcf().autofmt_xdate()
    plt.pause(0.0001)


s.listen(1)
print("socket is listening")
while True:
    # Establish connection with client.
    conn, addr = s.accept()
    print('Got connection from', addr)
    timestart=datetime.now()
    timeWindow=datetime.now()+timedelta(seconds=windowSize) # Sliding Window of 2.5 minutes
    
    while True:
#         eeg=[]
#         eegx=[]
        data = conn.recv(8192)
        token=data.decode('utf-8')
        if not data: break
##################### put the socket into listening mode\n"

        if "stage" in token or "Hello" in token:
            print(token)
            pass
        else:
            eegBuffer=[]
            timeBuffer=[]
            hourBuffer=[]
            minBuffer=[]
            secBuffer=[]
            milBuffer=[]

            tokens=token.split('/*/')
            for lex in tokens:
                if lex != '':
                    lits=lex.split(',')
                    buffer=[s2f(j) for j in lits if j is not '' and 'NaN' not in j]
                    eegBuffer.extend(buffer[0::5])
                    hourBuffer.extend(buffer[1::5])
                    minBuffer.extend(buffer[2::5])
                    secBuffer.extend(buffer[3::5])
                    milBuffer.extend(buffer[4::5])
            
            for times in range(len(eegBuffer)):
                timeBuffer.extend([datetime.now().replace(hour=int(hourBuffer[times]),minute=int(minBuffer[times]),
                                                         second=int(secBuffer[times]),microsecond=int(milBuffer[times])*1000)])
            

    # Check if the window is exceeded
            if timeWindow > datetime.now():
                eeg.extend(eegBuffer)
                eegx.extend(timeBuffer)
#                 for dates in range(len(eeg)-lenPrev):
#                     eegx.extend([datetime.now()])
#                 print(eegx,eeg)
            else:
                eeg.extend(eegBuffer)
                eegx.extend(timeBuffer)

                # remove the same number that got extended
                for drop in range(len(eegBuffer)):
                    eeg.popleft()
                    eegx.popleft()
                    
            if len(eeg)>10:
#                 print(eegx,eeg)
                realtimePlot()
