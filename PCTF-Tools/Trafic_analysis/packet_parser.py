#!/usr/bin/env python

##
##	CSE 545 - Spring 2018
##	Team 9: Black Shadow (blackshadow@asu.edu)
##

import re
import subprocess
import os
import sys
#import db_handler

HEADER = 53

## Input arguments handler
# Check if no more than 1 argument (.pcap file) is passed into the program
if (len(sys.argv) > 2):
    print("Program accepts only one input file!")
    exit()
# If no arguments specified - display help message
elif (len(sys.argv) == 1):
    print("USAGE:\nUse the following format to analyze .pcap file: ./tcpdump_process filename.pcap")
    exit()
# If only one argument specified - assign it to filename variable
else:
   filename = sys.argv[1]

## Arguments for running tcpdump in "read .pcap file" configuration
command     = 'tcpdump'
param       = '-Aqr'    # -A     Print each packet (minus its link level header) in ASCII.
                        # -q     Print less protocol information so output lines are shorter.
                        # -r     Read  packets from file 

## Execute tcpdump command with specified parameter to read packets from .pcap file
# Launch system subprocess and store its output
pcap_raw = subprocess.check_output([command, param, filename])
# Decode obtained 
pcap = pcap_raw.decode('utf-8')
print ('\n')

## Use regular expression to divide collected data into separate packets for further analysis
# Each new packet starts with a newline character followed by time stamp of the form HH:MM
packets = re.split('\n(?=\d\d:\d\d)', pcap)

## Process each packet separately, one by one
for packet in packets:
    print packet
    ## Strip packet into lines and store length of the first line as an offset value
    lines       = packet.splitlines()
    headline    = lines[0]  # First line
    offset      = len(headline)

    ## Obtain necessary data using regular expressions
    # Retrive timestamp
    time_stamp  = packet[:15]
    # Retrive src. port number
    src_port    = re.search('(?<=\.)(?:(?!\.).)*?(?=\ >)', headline).group(0)
    # Retrive src. IP address
    src_ip      = re.search('(?<=IP )(?:(?!IP ).)*?(?=\.%s)' % (src_port), headline).group(0)
    # Retrive dest. port number
    recv_port   = re.search('(?<=\.)(?:(?!\.).)*?(?=\:)', headline).group(0)
    # Retrive dest. IP address
    recv_ip     = re.search('(?<=\> )(?:(?!\> ).)*?(?=.%s)' % (recv_port), headline).group(0)
    # Retrive packet payload (data being transmitted)
    payload     = packet[(offset + HEADER):]
    # Add tab in front of each line in payload for better readability
    data        = '\n||\t\t\t\t'.join(payload.splitlines())

    #db_handler.update(time_stamp, src_ip, src_port, recv_ip, recv_port, data, flg_flag)

    ## Write all useful information regarding the packet into a file
    with open("ALL_TRAFFIC.txt", "a") as myfile:
        myfile.write('|| Src. IP: \t%s' % (src_ip))
        myfile.write('|| Src. port: \t%s\n' % (src_port))
        myfile.write('|| Recv. IP: \t%s' % (recv_ip))
        myfile.write('|| Recv. port: \t%s\n' % (recv_port))
        myfile.write('|| Time: \t\t%s\n' % (time_stamp))
        myfile.write('|| Data: \t\t%s\n' % (data))
        myfile.write('========================== = = = = =  =  =  =  =   =   =   ~    ~    -    -\n')


    ## Or print it out in Terminal

"""     print ('|| Src. IP: \t%s' % (src_ip))
    print ('|| Src. port: \t%s\n' % (src_port))
    print ('|| Recv. IP: \t%s' % (recv_ip))
    print ('|| Recv. port: \t%s\n' % (recv_port))
    print ('|| Time: \t%s\n' % (time_stamp))
    print ('|| Data: \t%s\n' % (data))
    print ('=================================================== = = = = =  =  =  =  =   =   =   ~    ~    -    -\n') """
