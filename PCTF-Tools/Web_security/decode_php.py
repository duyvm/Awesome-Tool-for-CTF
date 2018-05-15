import codecs
import base64
import re
import sys
from HTMLParser import HTMLParser

##
##	CSE 545 - Spring 2018
##	Team 9: Black Shadow (blackshadow@asu.edu)
##

def main():
    
    if len(sys.argv) < 2:
        print "a filename or a path is required"
        exit(1)
    else:
        filename = sys.argv[1]

    done = False
    decoded_str = ''
    
    with open(filename, 'r') as myfile:
          data = myfile.read()
    
    ori_body = data
    body = data

    while not done:        
        temp = re.search('\(\"(.+?)\"\)', body)
        encoded_str = temp.group(1)

        splited_str = ori_body.split("(")
        decode_progress = []
        
        for content in splited_str:
            
            if ('html_entity_decode' in content) or ('base64_decode' in content) or ('str_rot13' in content):
                decode_progress.append(content)        

        while decode_progress:
            cmd = decode_progress.pop()
            
            if cmd == 'str_rot13':
                decoded_str = codecs.getencoder("rot-13")(encoded_str)[0]
            
            if cmd == 'base64_decode':
                decoded_str = base64.b64decode(encoded_str)

            if cmd == 'html_entity_decode':
                hp = HTMLParser()
                decoded_str = hp.unescape(encoded_str)

            encoded_str = decoded_str            

        if ('html_entity_decode' in decoded_str) or ('str_rot13' in decoded_str):
            body = decoded_str
        else:
            done = True

    print decoded_str
    

if __name__ == '__main__':
    main()