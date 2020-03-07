#!/usr/bin/env python
import sys
import termios
import contextlib
import urllib2
import time


v1 = ""
url = "http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/update/v1?value="


def sendRequest():

    global url
    urlFinal = url + v1
    urllib2.urlopen(urlFinal).read()



def parse(val):
    global v1

    print ("received" ,val)

    if (val == 65):
        print "pressed forward"
        v1 = "11"
    if (val == 66):
        print "pressed back"
        v1 = "22" 
    if (val == 67):
        print "pressed right"
        v1 = "33" 
    if (val == 68):
        print "pressed left"
        v1 = "44" 
    if (val == 120):
        print "pressed stop"
        v1 = "99" 

    sendRequest()


@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)


def main():
    print 'exit with ^C or ^D'
    with raw_mode(sys.stdin):
        try:
            while True:
                ch = sys.stdin.read(1)
                if not ch or ch == chr(4):
                    break
                print "here"
                print '%02x\n' % ord(ch),
                parse(ord(ch))
        except (KeyboardInterrupt, EOFError):
            pass


if __name__ == '__main__':
    v1 = "99" 
    sendRequest()
    main()
