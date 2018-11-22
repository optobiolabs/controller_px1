#!/usr/local/bin/python3


#python controller.py 'profile.xlsx' '1;2000,250,0,0,0;2000,0,250,0,0;2000,0,0,250,0;2000,0,0,0,250'
import sys


i = 0
argument = []
for eachArg in sys.argv:
    i += 1
    if i == 2:
        argument = eachArg


if argument:

    if ".xlsx" in argument:
        #print("file")
        import read_xls as rx
        import pandas as pd
        profile_xlsx = pd.read_excel(argument)
        #print(profile_xlsx)
        profile_ms = profile_xlsx.copy()
        columns = ['timeA', 'durationA', 'timeB', 'durationB']
        pd.options.mode.chained_assignment = None
        for c in columns:
            for r in range(profile_ms.shape[0]):
                profile_ms[c][r] = rx.in_milliseconds(profile_xlsx[c][r])

        profileA = profile_ms[['timeA','intensityA', 'durationA']].rename(columns={'timeA':'time', 'intensityA':'intensityA', 'durationA':'duration'})
        profileB = profile_ms[['timeB','intensityB', 'durationB']].rename(columns={'timeB':'time', 'intensityB':'intensityB', 'durationB':'duration'})
        channelA = rx.channel_complete(profileA, 'intensityA').set_index('time')
        channelB = rx.channel_complete(profileB, 'intensityB').set_index('time')

        both_channels = pd.concat([channelB, channelA]).sort_index()
        complete_table = both_channels.fillna(method='ffill').fillna(0)

        profile = rx.serial_format(complete_table)

    else:
        #print("string")
        profile = argument

else:
    profile = input("enter value: ")

print(profile)

#import serial_connect
#import serial_write
#import serial_monitor
#import pandas as pd
import serial_connect as sc

print(sc.arduino.name)

if not sc.arduino.name == 'no device found':
    print (sc.arduino.readline())
    sc.arduino.write((str(profile) + '\r\n').encode())
    print (sc.arduino.readline())
