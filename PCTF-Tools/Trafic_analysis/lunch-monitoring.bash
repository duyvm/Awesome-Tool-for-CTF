#!/bin/bash

##
##	CSE 545 - Spring 2018
##	Team 9: Black Shadow (blackshadow@asu.edu)
##

OPTIND=1
port=""
i="1"

function show_help {
echo "Usage: bash ${0##*/} [-h] [&]"
echo -e "\t The script runs tcpdump command in loop,"
echo -e "\t saving output file every 3 minutes (every tick)."
echo -e "\t .pcap file name has incremental part, to ensure no"
echo -e "\t files get overwritten"
               exit 0
           }
while getopts "h?p:" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    esac
done

while true; do
echo "Launching tcpdump"
tcpdump -i eth0 -Aqn 'tcp[13]=24' and not port ssh and not port 443 and not arp and '(dst 172.31.129.9 and dst portrange 20001-20004)' or '(src 172.31.129.9 and src portrange 20001-20004)' -w tcpdump_temp$i.pcap &
pid=$!
sleep 180
kill $pid
echo "The tcpdump terminated"
i=$[$i+1]
done
