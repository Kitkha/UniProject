#!/usr/bin/env python3

# Generic modules
import getopt
import socket
import sys

# CLIENT SETUP
TCP_IP = '192.168.100.24'
TCP_PORT = 8080
BUFFER_SIZE = 64

# Function used to change the route of a specific vehicle
# add console arguments
def update_route(bus_id, route_number):
    if bus_id == None:
        print('Cannot send data: bus id is void')
    elif route_number == None:
        print('Cannot send data: route number is void')
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
        except OSError as msg:
            s.close()
            s = None
            print(msg)
            
        if s is None:
            print('Could not open socket')
        else:
            print('Connected to {} port {}'.format(TCP_IP, TCP_PORT))
            message = '3.{}.{}'.format(bus_id, route_number)
            
            s.send(message.encode('utf8'))
            data = s.recv(BUFFER_SIZE).decode('utf8')
            s.close()
            print('Server acknowledge message:', data)

bus_id = None
route_number = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hi:r:', ['help', 'id', 'route'])
except getopt.GetoptError:
    print('test.py -i <Vehicle ID> -r <New route number>')
    sys.exit()

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print('test.py -i <Vehicle ID> -r <New route number>')
        sys.exit()
    elif opt in ('-i', '--id'):
        bus_id = arg
    elif opt in ('-r', '--route'):
        route_number = arg

print ('Bus id is', bus_id)
print ('Route number is', route_number)
update_route(bus_id, route_number)

# TESTS
'''
update_route('1000', '1')
update_route('1000', '3')
update_route('1000', '5')
update_route('2000', '2')
'''
