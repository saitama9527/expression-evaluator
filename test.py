import socket
def get_remote_machine_info():
    remote_host = 'www.google.com'
    local_host = socket.gethostname()
    try:
        print ("IP address(local): %s"%socket.gethostbyname(local_host))
    except socket.error as err_msg:
        print ("%s: %s" %(local_host, err_msg))
    try:
        print ("IP address(remote): %s"%socket.gethostbyname(remote_host))
    except socket.error as err_msg:
        print ("%s: %s" %(remote_host, err_msg))

if __name__ == '__main__':
    get_remote_machine_info()


import socket
def find_service_name():
    protocolname = 'tcp'
    for port in [80, 25]:
        print ("Port: %s => service name: %s" %(port, socket.getservbyport(port, protocolname)))
        print ("Port: %s => service name: %s" %(53, socket.getservbyport(53, 'udp'))) # DNS uses UDP
if __name__ == '__main__':
    find_service_name()