
# Project "Capture the Flag" (PCTF) - CSE545 Spring 2018

## Description 
This project is developed in a team of 6 students as a part of CSE545 coursework. The tools we developed include backdoor, proxy, reflector, traffic analyzer, vulnerability detector, PHP decoder, and aggressive shellcode. A detailed report is given in "CSE545-Team9-FinalReport.pdf". The "PCTF.pptx" explains how a Capture the Flag challenge works.

## Development Environment
- Python 2.7
- gcc 4.8+

## How to use

The PCTF-Tools/SWAPG were provided to us by the instructor.

### Backdoor
```
$./backdoorName PORT_NUM
```
This backdoor once launched did not need any further configurations. This would just listen to incoming connections on the port specified.

### Backdoor auto connect script
``` 
$ python backdoorConnect.py
```
This application required to be properly configured before launching. First the proper Game IP and Auth token must be supplied. Then the array containing the Hosts that are infected with the backdoor need to be specified. Lastly the directory where the flags were located needed to be specified since this is different for each service. Also the service ID for the service that allowed the backdoor needed to be specified in order to get the correct Flag IDs for the current tick using `api.py`.

### Proxy
Launch this application by naming it the same as the service such that Xinetd.d service will call this python script instead of the original service. Also be sure to make this application executable.

This tool will take a user input then apply the firewall rules set, send the input and check whether it contains flag information, or send the input to the reflector machine to be reflected to everyone else. Once this input was sanitized or dropped, it is then sent to the original service. This service sends back a reply and this application will then return that reply to Xinetd.d.

This application requires configuration such as which list of characters and strings are considered error level 1, 2, or 3. Requires whether to call the sub-services: Verify Flag or Reflector. Some basic information about the original service such that it can call it correctly.

### Reflector
This tool is a standalone service that needs to ran on a machine that is capable of submitting flags and executing api.py to get flag ID and host information. This application requires configuration to be made describing which teams to reflect traffic and login information to read flags. This tool can be disabled but make sure to disable reflector in prox.py.
```
$ python Reflector.py
```

### Flag verify
This tool is a standalone service that needs to be ran on the same machine as the machine that has the flags. This tool would need to be written separately for each service. As it is required that this application be able to parse out Flag_ID, FLag_Password and Flag from the flag files located on the machine. This tool can be disable but make sure to disable flag verify in proxy.py.
```
$ python FlagVerify.py
```

### Auto exploit tool
This application is a skeleton application taking a working exploit for the practice PCTF. Please fill out the configuration section that most importantly contains the flag path. This path is the location of the flags for that current service.
``` 
$ python autoExploit.py
```

### Port Scanner
This tool will just try and bin a raw socket with every port to see if there is a response. To launch this tool just make sure the configuration is set. The only thing required is the port range, separated to 2 variables: PORT_RANGE_LOW and PORT_RANGE_HIGH, then fill out the array TEAMS_TO_SCAN which is a list of the teams that will be scanned.
```
$ python portScanner.py
```

### Traffic Analyzer
The `lunch-monitoring.bash` executes the `tcpdump` command every 3 min (180 sec), saves a `.pcap` file, and repeats the action until manually stopped with a keyboard interrupt
```
$ ./lunch-monitoring.bash
```
The `packet_parser.py` accepts the `.pcap` filename (+`/path`, if not in the same folder) as an input argument, and outputs

`ALL_TRAFIC.txt` file with all packets presented in readable form. If `ALL_TRAFIC.txt` already exists in the folder, `packet_parser.py` will append newly processed packets to existing file.
```
$ python packet_parser.py <filename>
```
### Vulnerability Detector
This detector scan a `.c`, `.asm`, `.php`, or `.html` file and then displays the line number which contains potential vulnerable keywords.
```
$ python FileAnalyzer.py <file_name>
```
### PHP Decoder
In CTF 3, the PHP files are encoded with `base64_decode` and `str_rot13` for several iterations. Therefore we prepare a script to decode repeatedly until it's readable for human.
```
$ python decode_php.py <file_name>
```

### Shellcode
Shellcode has a few samples from project 3 to help pop a shell and also a sample from the book to run /bin/sh without needing to pop a shell.
```
$ gcc -m32 -o exec_shell exec_shell.c
$ ./exec_shell
```
```
$ gcc -m32 -o shell1 shell1.c
$ ./shell1
```
```
$ gcc -m32 -o shell2 shells.c
$ ./shell2 <path to vulnerable binary>
```
