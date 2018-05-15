import sys

##
##	CSE 545 - Spring 2018
##	Team 9: Black Shadow (blackshadow@asu.edu)
##

class Analyze:

    def __init__(self):
        self.highlight_c = ["printf", "sprintf", "strcpy", "gets", "fgets", "puts", "execlp", "system", "strcpy",
                             "strcmp", "argv", "execvp", "File", "sleep", "memcpy" ]

        self.highlight_php = ["grep", "system", "eval", "popen", "include", "require", "REQUEST", "$_GET", "$_POST",
                               "COOKIE", "ENV", "PHPSESSID", "mysql_query", "$_SESSION", "document.write", 
                               "<input", "<a hef", "<img", "<script"]
        self.path = sys.argv[1]

    def readfile(self):
        # path = input("input path of file: ")
        if len(sys.argv) < 2:
            print("input the path of file as cmd argument")
            exit(1)

        if ".c" or ".asm" in self.path:
            self.analyze_c()
        if ".html" or ".php" in self.path:
            self.analyze_php()

    def analyze_c(self):
        print("Analyzing the C file :\n")
        linenum = 1
        with open(self.path) as f:
            for line in f:
                for i in self.highlight_c:
                    if i in line:
                        print("Line num {}: {}".format(linenum, i))
                linenum += 1

    def analyze_php(self):
        print("Analyzing the php file :\n")
        linenum = 1
        with open(self.path) as f:
            for line in f:
                for i in self.highlight_php:
                    if i in line:
                        print("Line num {}: {}".format(linenum, i))
                linenum += 1


if __name__ == "__main__":
    obj = Analyze()
    obj.readfile()
