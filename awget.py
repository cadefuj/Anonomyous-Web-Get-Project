###############################################
# Group Name  : Broncos

# Member1 Name: Cade Fujitani
# Member1 SIS ID: 832956909
# Member1 Login ID: cadefuj

# Member2 Name: Kaden Mahoney
# Member2 SIS ID: 832306406
# Member2 Login ID: kjm43
###############################################
###############################################
# MUST KEEP: sets printing butter to 1, so it will always flush. allows the autograder to work. 
import sys
import os.path
import random
from urllib.parse import urlparse
import socket
import io 
import pickle
sys.stdout = open(sys.stdout.fileno(), 'w', buffering=1)
###############################################

def readChainFile() :
    chainfile = ""
    if (len(sys.argv) < 2) : 
        print("Insufficent Input Parameters")
        exit(1)
    elif (len(sys.argv) == 3) :
        chainfile = "chaingang.txt"
        url = sys.argv[1]
        return chainfile, url
    else :
        url = sys.argv[1]
        chainfile = "chaingang.txt"
        if (len(sys.argv) == 4) :
            chainfile = sys.argv[3]
    return chainfile, url


def getRandomSS(chainfile): 
    try: 
        with open(chainfile, 'r') as file :
            data = file.read()
        chainlist = data[2:].split('\n')
        currentChain = random.choice(chainlist)
        return chainlist, currentChain
    except FileNotFoundError :
        print("Cannot find file or does not exist")

def getFile(sock,url) :
    buffer = b""
    if "/" in url :
        filename = url.split('/').pop()
    else : 
        filename = "index.html" 
    while True :
        data = sock.recv(3000)
        if not data :
            break
        buffer += (data)
    with open(filename, 'wb') as file :
        file.write(buffer)
    print("Received File: <" + filename + ">")
    
def startConnection():  
    chainfile, url = readChainFile()
    chain, current = getRandomSS(chainfile)
    addr, port = current.split(" ")
    print("awget:")
    print("Request: " + url)
    print("chainlist is")
    print(*chain, sep="\n")
    print("next SS is <" + current + ">")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, 
                     socket.SO_REUSEADDR, 1) 
    sock.connect((addr, int(port)))
    chain.remove(current)   
    strchain = url + ' ' + str(chain)
    encodeStr =  strchain.encode('utf-8')
    sock.sendall(encodeStr)
    print("waiting for file...")
    getFile(sock, url)
    print("Goodbye!")

startConnection()