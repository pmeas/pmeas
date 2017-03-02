import json, socket, subprocess, sys

PORT = 8034

#TODO add ability for backend to send audio interfaces to frontend

def backend(timeout=None):
    def getIp():
        return subprocess.check_output(['ip', 'neighbor']).split()[0]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.setblocking(1)
    try:
        sock.connect((getIp(), PORT))
        jbytes = sock.recv(4096)
        return jbytes.decode('utf-8')
    finally:
        sock.close()

if __name__ == '__main__':
    #USAGE bridge <frontend|backend>
    #run the frontend THEN the backend
    if sys.argv[1] == 'frontend':
        frontend(sys.stdin.read())
    elif sys.argv[1] == 'backend':
        sys.stdout.write(backend())