#!/usr/bin/env python3

# Generic modules
import socket
import sys
import time

# Project modules
import RPI_DB

# SERVER COMMUNICATION SETUP
TCP_IP = '192.168.100.24'
TCP_PORT = 8080
BUFFER_SIZE = 64

TIME = time.strftime("%H:%M:%S")
DATE = time.strftime("%d/%m/%Y")

# SERVER COMMUNICATION FUNCTIONS

# Function that receives a list of stations from server and updates the route
def receive_route(s):
    print('Receiving route...')
    data = s.recv(int(RPI_DB.UPDATE_STATE) * 10 + 8).decode('utf8')
    s.close()
    print(data)
    route_list = eval(data)
    RPI_DB.ROUTE_NUMBER = route_list[0]
    RPI_DB.ROUTE_ID = route_list[1:]

    RPI_DB.ROUTE_NAMES = []
    for station_id in RPI_DB.ROUTE_ID:
        RPI_DB.ROUTE_NAMES.append(RPI_DB.get_station_info(station_id)['NAME'])
    
    print('Update complete')

# Function used by RPI to publish data on server
def print_data(station_id):
    if station_id == None:
        print('Cannot send data: station id is void')
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
            message = '1.{}.{}.{}.{}'.format(DATE, TIME,
                                             str(RPI_DB.ROUTE_NUMBER),
                                             station_id)
            s.send(message.encode('utf8'))
            
            data = s.recv(BUFFER_SIZE).decode('utf8')
            s.close()
            print('Server acknowledge message:', data)

# Function used by RPI to check if a route update is needed
def check_for_update():
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
        message = '2.{}.{}'.format(str(RPI_DB.BUS_ID),
                                   str(RPI_DB.ROUTE_NUMBER))
        s.send(message.encode('utf8'))

        data = s.recv(BUFFER_SIZE).decode('utf8')
        print('Server acknowledge message:', data)
        RPI_DB.UPDATE_STATE = data
        if int(RPI_DB.UPDATE_STATE) < 0:
            print('Check failed')
        elif int(RPI_DB.UPDATE_STATE) > 0:
            receive_route(s)
        else:
            print('Route up to date')

# TESTS
'''
print_data('100032')
print_data('123456')
print_data(None)

check_for_update()
'''
