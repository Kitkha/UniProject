#!/usr/bin/env python3

# Generic modules
import time
import signal
import sys

# Project modules
import RPI_DB
import vehicle_interface

# Open source modules
from rpi_rf import RFDevice

def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT, exithandler)
    
# Setup RF device for listening
RFpin = 17
rfdevice = None
rfdevice = RFDevice(RFpin)
rfdevice.enable_rx()
timestamp = None

# Variable used to verify if an update is needed
need_update = None

# The ID of the last visited station
last_id = None

# Dictionary of the current station
current_station = None

# Index of the current station in route list
index = None

print("Main programm started working...")

while 1:
    print('#################################################')
    vehicle_interface.check_for_update()
    if int(RPI_DB.UPDATE_STATE) > 0:
        need_update = True

    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        
        if str(rfdevice.rx_code) in RPI_DB.ROUTE_ID:
            print(str(rfdevice.rx_code) + ' [pulselength ' +
                  str(rfdevice.rx_pulselength) + ', protocol ' +
                  str(rfdevice.rx_proto) + ']')
            
            station_id = str(rfdevice.rx_code)
            station_name = RPI_DB.ROUTE_NAMES[RPI_DB.ROUTE_ID.index(station_id)]
            
            if need_update:
                if last_id == None:
                    last_id = station_id
                    vehicle_interface.current_station(station_id, station_name)
                else:
                    index = RPI_DB.get_route_index(last_id, station_id)
                    if index != None:
                        need_update = False
                        last_id = current_station
                        vehicle_interface.current_station(station_id, station_name)
            else:
                print('Following route: {}'.format(RPI_DB.ROUTE_ID))
                next_index = (index + 1) % len(RPI_DB.ROUTE_ID)
                if station_id == RPI_DB.ROUTE_ID[next_index]:
                    last_id = current_station
                    vehicle_interface.current_station(station_id, station_name)
                    index = next_index
                    next_index = (index + 1) % len(RPI_DB.ROUTE_ID)
                    vehicle_interface.next_station(RPI_DB.ROUTE_ID[next_index], RPI_DB.ROUTE_NAMES[next_index])
    vehicle_interface.show_time()
    time.sleep(1)
rfdevice.cleanup()
