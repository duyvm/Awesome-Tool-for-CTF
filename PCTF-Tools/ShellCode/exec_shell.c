#include <unistd.h>

/*
	CSE 545 - Spring 2018
	Team 9: Black Shadow (blackshadow@asu.edu)
	The Art of Exploitation - page 296
*/


int main() {
	char filename[] = "/bin/sh\x00";
	char **argv, **envp;
	argv[0] = filename;
	argv[1] = 0;
	envp[0] = 0;
	execve(filename, argv, envp);
}