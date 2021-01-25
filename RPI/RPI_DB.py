#!/usr/bin/env python3

# RPI DATABASE SETUP
BUS_ID = 1003
ROUTE_NUMBER = ''
ROUTE_ID = []
ROUTE_NAMES = []

# Update status flag:
# if route is up to date - 0
# if current route needs to be changed - length of the new route
UPDATE_STATE = '0'

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
STATION = sorted(STATION, key=lambda k: k['ID'])
STATION_ID = []
for station in STATION:
    STATION_ID.append(station['ID'])
    
# Binary search by station ID
# Return station dictionary if ID is found, None if ID is not found
def get_station_info(station_id):
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
            return STATION[mid]
    return None

# Search the current location in the route list
# Return the index of the current station ID
def get_route_index(last_station, current_station):
    n = len(ROUTE_ID)
    for i in range(n):
        if ROUTE_ID[i] == last_station:
            if ROUTE_ID[(i + 1) % n] == current_station:
                return (i + 1) % n
    return None

'''
for station in STATION:
    print(get_station_info(station['ID']))
print(get_station_info(123456))

ROUTE_ID = ['6', '4', '2', '3', '5', '4', '7']
print(get_route_index('6', '4')) #1
print(get_route_index('2', '3')) #3
print(get_route_index('4', '7')) #6
print(get_route_index('7', '6')) #0
print(get_route_index('4', '4')) #None
'''
