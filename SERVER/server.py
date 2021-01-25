#!/usr/bin/env python3

# Generic modules
import socket
import sys

# Project modules
import server_DB

# SERVER SETUP
if not server_DB.run_DB_check():
    print('Database check failed. Exiting...')
    sys.exit()
else:
    print('Database check successful')
    
TCP_IP = '192.168.100.24'
TCP_PORT = 8080
BUFFER_SIZE = 64

# SERVER FUNCTIONS

# Function that receives a list of stations from server and updates the route
def send_route(route_dict):
    print('Sending route...')
    route_list = [route_dict['NUMBER']] + route_dict['STATIONS']
    print(route_list)
    data = str(route_list).encode('utf8')
    conn.send(data)
    print('Data sent')
        
# REQUEST TYPE = PRINT_DATA
# Print the data received from RPI
# Send acknowledge message back to the RPI
def print_data():
    global message
    message = message.split('.')
    station = server_DB.get_station_dict(message[4])
    
    if station == None:
        conn.send('Station ID not found in DB'.encode('utf8'))
        print('Station ID not found in DB')
    else:
        print('[' + message[1] +
              ', ' + message[2] +
              ']: Vehicle ' + message[3] +
              ' arrived at station ' + station['NAME'])
        
    conn.send('Data sent successfuly'.encode('utf8'))
    conn.close()

# REQUEST TYPE = ASK_FOR_UPDATE
# Check if the RPI needs to update the route
# Send a message back to RPI about the update status
def check_for_update():
    global message
    route_dict = None
    message = message.split('.')
    if message[1] in server_DB.BUS_IDS:
        if server_DB.route_check(message[1], message[2]):
            log_message = 'no update needed'
            ack_message = '0'
        else:
            bus_dict = server_DB.get_bus_route_dict(message[1])
            route_dict = server_DB.get_route_dict(bus_dict['ROUTE_NUMBER'])

            ack_message = str(len(route_dict['STATIONS']))
            log_message = 'needs route update'
    else:
        log_message = 'unknown vehicle ID'
        ack_message = '-1'
    print('Client {} requested a route check'.format(addr[0]))
    print('Vehicle {} with route {}: {}'.format(message[1], message[2], log_message))
    conn.send(ack_message.encode('utf8'))
    if int(ack_message) > 0:
        send_route(route_dict)
    conn.close()

# REQUEST TYPE = UPDATE_ROUTE
# Check if the route needs to be changed
# If changes need to be done, update the route number
# Send acknowledge message back to the admin client
def change_route():
    global message
    message = message.split('.')
    if message[1] in server_DB.BUS_IDS:
        if message[2] in server_DB.ROUTE_NUMBERS:
            if server_DB.route_check(message[1], message[2]):
                log_message = 'no changes needed to be done'
            else:
                server_DB.update_db(message[1], message[2])
                log_message = 'changed route number'
            ack_message = 'Route update successful'
        else:
            log_message = 'unknown route number'
            ack_message = 'Route update failed'
    else:
        log_message = 'unknown bus id'
        ack_message = 'Route update failed'

    print('Admin {} requested a route update'.format(addr[0]))
    print('Vehicle {} with route {}: {}'.format(message[1], message[2], log_message))
    conn.send(ack_message.encode('utf8'))
    conn.close()

# RUN SERVER
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print ('Starting up on {} port {}'.format(TCP_IP, TCP_PORT))

while True:
    try:
        conn, addr = s.accept()
        print ('Connection address:', addr)
        data = conn.recv(BUFFER_SIZE)
        message = data.decode('utf8')
        
        if message[0] == server_DB.PRINT_DATA:
            print_data()
        elif message[0] == server_DB.ASK_FOR_UPDATE:
            check_for_update()
        elif message[0] == server_DB.UPDATE_ROUTE:
            if addr[0] in server_DB.ADMIN_IP:
                change_route()
                
    except OSError as msg:
        print(msg)
        conn.close()
