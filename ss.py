###############################################
# Group Name  : Broncos

# Member1 Name: Kaden Mahoney
# Member1 SIS ID: 832306406
# Member1 Login ID: kjm43

# Member2 Name: Cade Fujitani
# Member2 SIS ID: 832956909
# Member2 Login ID: cadefuj
###############################################

###############################################
# MUST KEEP: sets printing butter to 1, so it will always flush. allows the autograder to work. 
import sys
sys.stdout = open(sys.stdout.fileno(), 'w', buffering=1)
###############################################
import socket
import threading
import random
import os
import ast
    
def findFileName(url):
    filename = ''
    if url is None:
        return None
    if '/' in url:
        filename = url.split('/').pop()
    else:
        filename = "index.html"
    return filename
    
def ThreadProcess(conn, url, chainlist):
    try : 
        reuturnFile = findFileName(url)
        if len(chainlist) == 0:
            print("chainlist is empty")
            print("issuing wget for file <", reuturnFile, ">")
            
            os.system('wget -q --output-document ' + reuturnFile + ' ' + url)
            
            print("File received")
            print("Relaying file...")
            
            with open(reuturnFile, 'rb') as f:
                while True:
                    data = f.read(1500)
                    if not data:
                        break
                    conn.send(data)
            os.remove(reuturnFile) 
        else:
            print("chainlist is\n")
            
            for chain in chainlist:
                size = len(chain)
                print('<', chain[:size-4], ",", chain[size-4:], '>')
            nextSS = random.choice(chainlist)
            chainlist.remove(nextSS)
            addrPort = nextSS.split(' ')
            
            print("next SS is <", addrPort[0], ",", addrPort[1], ">")
            
            socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
            socket2.connect((addrPort[0], int(addrPort[1])))
            temp = url + ' ' + str(chainlist)
            encodeStr = temp.encode('utf-8')
            socket2.send(encodeStr)
            
            print("waiting for file...\n...\n")
            while True:
                
                data = socket2.recv(1500)
                if not data:
                    break
                conn.send(data)
                
            print("Relaying file...")
            
            socket2.close()
        conn.close()
        
        print("Goodbye!")
    except Exception as e : 
        print(f"ERROR: {str(e)}")
        

if "-p" in sys.argv:
    try:
        port = int(sys.argv[sys.argv.index("-p") + 1])
    except:
        print("Input a port number after the '-p' flag!")
        exit(1)
else:
    port = 2345

hostname = socket.gethostname()
IP_ADDR = socket.gethostbyname(hostname)

print("ss <", IP_ADDR, ",", port, ">:")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
sock.bind((IP_ADDR, port))

try:
    while True:
        sock.listen()
        conn, addr = sock.accept()
        
        recv_data = conn.recv(1048)
        datasplit = recv_data.decode('utf-8').index(' ')
        url = recv_data.decode('utf-8')[:datasplit]
        chainlist = ast.literal_eval(recv_data.decode('utf-8')[datasplit+1:])
        
        print("Request: ", url)
        
        nextSSProcess = threading.Thread(target=ThreadProcess, args=(conn, url, chainlist))
        nextSSProcess.start()
        nextSSProcess.join()
except KeyboardInterrupt:
    exit(0)