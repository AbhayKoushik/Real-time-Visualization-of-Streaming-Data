######################### Created by Abhay for Visualizing Real-time Data ##########################
######################### Real-time Streaming through remote web sockets ###########################

from socket import *
import random
from collections import deque
import numpy as np
import time
import psutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

#########################################################

# UTF-8 String to float converter
s2f = lambda s: float("".join(i for i in s if 46 <= ord(i) < 58 and ord(i)!=47))

# Initialization of Parameters for graphing
x_len = 3000         # Number of points to display
y_range = [0, 1200]  # Range of possible Y values to display

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 3000))
ys = [0] * x_len
ax.set_ylim(y_range)


# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys,'r-')


myFmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(myFmt)

# Add labels
plt.title('EEG Over Time')
plt.xlabel('Time - HH:MM:SS')
plt.ylabel('EEG')
plt.ion()

############################################################
# next create a socket object
s = socket()
print("Socket successfully created")

# initialize the same port number
port = 5601 

#bind to the port
s.bind(('xx.xx.xxx.xxx', port)) # Enter IP 
print("socket binded to %s" %(port))

# put the socket into listening mode
i=1 # counter

eeg=[0]
eegx=[0]

s.listen(1)
print("socket is listening")
while True:
    
    # Establish connection with client.
    conn, addr = s.accept()
    print('Got connection from', addr)
    while True:
        data = conn.recv(8192)
        token=data.decode('utf-8')
,
        if "Any initial Messages" in token or "Data except parseable floats go here" in token:
            print(token)
            pass
        else:
            tokens=token.split(',')
            
            # Continuously parsing and plotting in an infinite while loop
            eeg.extend([s2f(j) for j in tokens if j is not ''])
            eegx=np.arange(len(eeg))
            
            print(eegx[-1],eeg[-1])
            
            ############Scatterplot###########
            
            # Maintaining a 30 second window on the plot
            ax.set_xlim([datetime.now()-timedelta(seconds=30), datetime.now()])
            ax.xaxis.set_major_formatter(myFmt)
            
            # plotting the last elements of the collected data in real-time
            plt.plot(datetime.now(),eeg[-1],'r.') 
            plt.pause(0.0001)
