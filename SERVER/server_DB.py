#!/usr/bin/env python3
import time
# SERVER DATABASE

# List of IP's allowed to change the route of a vehicle
ADMIN_IP = [ '192.168.100.24' ]

# Request types
PRINT_DATA = '1'
ASK_FOR_UPDATE = '2'
UPDATE_ROUTE = '3'

# System check - False if check failed
check = True

# A local copy of data about all stations
STATION = [
    { 'ID' : '100001', 'NAME' : 'Baza 3' },
    { 'ID' : '100002', 'NAME' : 'Bicaz' },
    { 'ID' : '100003', 'NAME' : 'Bucium' },
    { 'ID' : '100004', 'NAME' : 'C.U.G.' },
    { 'ID' : '100005', 'NAME' : 'Canta' },
    { 'ID' : '100006', 'NAME' : 'Ciric' },
    { 'ID' : '100007', 'NAME' : 'Continental' },
    { 'ID' : '100008', 'NAME' : 'Copou' },
    { 'ID' : '100009', 'NAME' : 'Dacia' },
    { 'ID' : '100010', 'NAME' : 'Dancu' },
    { 'ID' : '100011', 'NAME' : 'Elena Doamna' },
    { 'ID' : '100012', 'NAME' : 'Familial' },
    { 'ID' : '100013', 'NAME' : 'Filarmonica' },
    { 'ID' : '100014', 'NAME' : 'Gara' },
    { 'ID' : '100015', 'NAME' : 'Gara Internationala' },
    { 'ID' : '100016', 'NAME' : 'George Cosbuc' },
    { 'ID' : '100017', 'NAME' : 'Minerva' },
    { 'ID' : '100018', 'NAME' : 'Mircea cel Batran' },
    { 'ID' : '100019', 'NAME' : 'Moara 1 Mai' },
    { 'ID' : '100020', 'NAME' : 'Pacurari' },
    { 'ID' : '100021', 'NAME' : 'Palatul Culturii' },
    { 'ID' : '100022', 'NAME' : 'Pasaj Nicolina' },
    { 'ID' : '100023', 'NAME' : 'Piata Alexandru cel Bun' },
    { 'ID' : '100024', 'NAME' : 'Piata Independentei' },
    { 'ID' : '100025', 'NAME' : 'Piata Mihai Eminescu' },
    { 'ID' : '100026', 'NAME' : 'Piata Unirii' },
    { 'ID' : '100027', 'NAME' : 'Podu Ros' },
    { 'ID' : '100028', 'NAME' : 'Podu de Fier' },
    { 'ID' : '100029', 'NAME' : 'Stadion' },
    { 'ID' : '100030', 'NAME' : 'Targu Cucu' },
    { 'ID' : '100031', 'NAME' : 'Tatarasi Nord' },
    { 'ID' : '100032', 'NAME' : 'Tesatura' },
    { 'ID' : '100033', 'NAME' : 'Triumf' },
    { 'ID' : '100034', 'NAME' : 'Tudor Vladimirescu' },
    { 'ID' : '100035', 'NAME' : 'Universitate' }
    ]
# Sort the stations by their ID to make search easier
STATION = sorted(STATION, key=lambda k: k['ID'])

# List of all existing routes
ROUTES = [
    { 'NUMBER' : '1', 'STATIONS' : ['100001', '100025'] },
    { 'NUMBER' : '2', 'STATIONS' : ['100034', '100019', '100021', '100006'] },
    { 'NUMBER' : '3', 'STATIONS' : ['100011', '100016', '100023'] },
    { 'NUMBER' : '1b', 'STATIONS' : ['100030', '100022', '100013', '100033', '100015', '100029'] },
    { 'NUMBER' : '30b', 'STATIONS' : ['100035', '100003', '100004', '100027', '100018'] },
    { 'NUMBER' : '999', 'STATIONS' : ['100010'] }
    ]

# Make a list of all existing route numbers
ROUTE_NUMBERS = []
print('-> Checking all route numbers...')
for route in ROUTES:
    if route['NUMBER'] in ROUTE_NUMBERS:
        print('Route number {} already assigned'.format(route['NUMBER']))
        check = False
    ROUTE_NUMBERS.append(route['NUMBER'])

# List of all vehicles that have been assigned a route
# Can be temporarily updated at the request of an admin client
BUS_ROUTES = [
    { 'BUS_ID' : '1000', 'ROUTE_NUMBER' : '1' },
    { 'BUS_ID' : '1001', 'ROUTE_NUMBER' : '2' },
    { 'BUS_ID' : '1002', 'ROUTE_NUMBER' : '3' },
    { 'BUS_ID' : '1003', 'ROUTE_NUMBER' : '1b' },
    { 'BUS_ID' : '3000', 'ROUTE_NUMBER' : '30b' },
    { 'BUS_ID' : '9999', 'ROUTE_NUMBER' : '999' }
    ]
# Sort the vehicles by their ID to make search easier
BUS_ROUTES = sorted(BUS_ROUTES, key=lambda k: k['BUS_ID'])

# Make a list of all existing bus id's
BUS_IDS = []
print("-> Checking all bus id's...")
for bus_route in BUS_ROUTES:
    if bus_route['BUS_ID'] in BUS_IDS:
        print('Bus id {} already assigned'.format(bus_route['BUS_ID']))
        check = False
    BUS_IDS.append(bus_route['BUS_ID'])

# DATABASE FUNCTIONS

# Binary search stations by ID
# Return station index if ID is found, None if ID is not found
def get_station_index(station_id):
    left = 0
    right = len(STATION) - 1
    mid = 0
    while left <= right:
        mid = (right + left) // 2
        if STATION[mid]['ID'] < str(station_id):
            left = mid + 1
        elif STATION[mid]['ID'] > str(station_id):
            right = mid - 1
        else:
            return mid
    return None

# Return station dictionary if ID is found, None if ID is not found
def get_station_dict(station_id):
    station_index = get_station_index(station_id)
    if station_index == None:
        return None
    return STATION[station_index]

# Search routes by route number
# Return route dictionary if number is found, None if number is not found
def get_route_dict(route_number):
    for route in ROUTES:
        if route_number == route['NUMBER']:
            return route
            break
    return None

# Binary search by bus ID
# Return Route dictionary if ID is found, None if ID is not found
def get_bus_route_index(bus_id):
    left = 0
    right = len(BUS_ROUTES) - 1
    mid = 0
    while left <= right:
        mid = (right + left) // 2
        if BUS_ROUTES[mid]['BUS_ID'] < str(bus_id):
            left = mid + 1
        elif BUS_ROUTES[mid]['BUS_ID'] > str(bus_id):
            right = mid - 1
        else:
            return mid
    return None

# Return bus route dictionary if ID is found, None if ID is not found
def get_bus_route_dict(bus_id):
    bus_route_index = get_bus_route_index(bus_id)
    if bus_route_index == None:
        return None
    return BUS_ROUTES[bus_route_index]

# Assign a new route for the bus with the given ID
def update_db(bus_id, route_number):
    bus_route_index = get_bus_route_index(bus_id)
    BUS_ROUTES[bus_route_index]['ROUTE_NUMBER'] = route_number

# Check if the given route number and route number corresponding with
# the given bus id are the same
# Return True if route is up to date, False if an update is needed
def route_check(bus_id, route_number):
    bus_route = get_bus_route_dict(bus_id)
    if bus_route['ROUTE_NUMBER'] == route_number:
        return True
    return False

# DATABASE CHECK FUNCTIONS

def check_station_ids():
    print("-> Checking all stations...")
    err_msg = 'Station id {} already assigned to {}'

    ret_code = True
    n = len(STATION)
    i = 0
    while i < n:
        name_list = []
        j = i + 1
        found_duplicate = False
        while j < n and STATION[i]['ID'] == STATION[j]['ID']:
            name_list = name_list + [STATION[j]['NAME']]
            j = j + 1
            found_duplicate = True
            ret_code = False
        if found_duplicate:
            print(err_msg.format(STATION[i]['ID'], name_list))
            i = j
        i = i + 1
    return ret_code
    
def check_route_stations():
    print("-> Checking the station ID's in routes database...")
    err_msg = 'In route {} the station ID {} is not registered'

    ret_code = True
    for route in ROUTES:
        for station in route['STATIONS']:
            station_dict = get_station_dict(station)
            if station_dict == None:
                print(err_msg.format(route['NUMBER'], station))
                ret_code = False
    return ret_code
    
def check_bus_routes():
    print("-> Checking the route numbers in bus database...")
    err_msg = 'For bus {} the route number {} is not registered'

    ret_code = True
    for bus in BUS_ROUTES:
        if bus['ROUTE_NUMBER'] not in ROUTE_NUMBERS:
            print(err_msg.format(bus['BUS_ID'], bus['ROUTE_NUMBER']))
            ret_code = False
    return ret_code

def run_DB_check():
    chk1 = check_station_ids()
    chk2 = check_route_stations()
    chk3 = check_bus_routes()
    return chk1 and chk2 and chk3 and check

# TESTS
'''
for station in STATION:
    print(get_station_dict(station['ID']))
print(get_station_dict(123456))

for bus_route in BUS_ROUTES:
    print(get_bus_route_dict(bus_route['BUS_ID']))
print(get_bus_route_dict(123456))

for route in ROUTES:
    print(get_route_dict(route['NUMBER']))
print(get_route_dict('5'))

update_db('1000', '1')
update_db('1000', '3')
update_db('1000', '5')
update_db('2000', '2')

print(route_check('1000', '1'))
print(route_check('1000', '2'))

print(run_DB_check())

start_time = time.time()
for i in range(20000):
    for j in range(20000):
        if i == j:
            break
print("--- %s seconds ---" % (time.time() - start_time))
'''
