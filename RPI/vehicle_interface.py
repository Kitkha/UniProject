#!/usr/bin/python

# Generic modules
import os
import threading
import time

# Project modules
import RPI_server_comm

# Open source modules
import I2C_LCD_driver
LCD = I2C_LCD_driver.lcd()

def show_time():
    #LCD.lcd_clear()
    LCD.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 1)
    LCD.lcd_display_string("Date: %s" %time.strftime("%d/%m/%Y"), 2)

def display_current_station(station_name):
    LCD.lcd_clear()
    LCD.lcd_display_string('Statia', 1)
    LCD.lcd_display_string(station_name, 2)
    time.sleep(0.8)
    
    if len(station_name) > 16:
        for index in range(0, len(station_name)-15):
            LCD.lcd_display_string(station_name[index:], 2)
            time.sleep(0.5)
        time.sleep(1)
    else:
        time.sleep(2.2)
    LCD.lcd_clear()

def display_next_station(station_name):
    LCD.lcd_clear()
    LCD.lcd_display_string('Urmeaza statia:', 1)
    LCD.lcd_display_string(station_name, 2)
    time.sleep(1.5)
    
    if len(station_name) > 16:
        for index in range(0, len(station_name)-15):
            LCD.lcd_display_string(station_name[index:], 2)
            time.sleep(0.5)
        time.sleep(1)
    else:
        time.sleep(2)
    LCD.lcd_clear()

def speak_current_station(station_name):
    station_name = ''.join(station_name.split('.'))
    os.system( 'espeak -vro+m7 -s 120 "Statia: '+station_name+'" --stdout | aplay' )
    
def speak_next_station(station_name):
    station_name = ''.join(station_name.split('.'))
    os.system( 'espeak -vro+m7 -s 120 "Urmeaza statia: '+station_name+'" --stdout | aplay' )
    
def current_station(station_id, station_name):
    t1 = threading.Thread(target = display_current_station, args=(station_name,))
    t2 = threading.Thread(target = speak_current_station, args=(station_name,))
    t3 = threading.Thread(target = RPI_server_comm.print_data(station_id,))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

def next_station(station_id, station_name):
    t1 = threading.Thread(target = display_next_station, args=(station_name,))
    t2 = threading.Thread(target = speak_next_station, args=(station_name,))
    t3 = threading.Thread(target = RPI_server_comm.print_data(station_id,))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    
def check_for_update():
    RPI_server_comm.check_for_update()

'''
current_station('Piata Alexandru cel Bun')
current_station('C.U.G')
speak_next_station('C.U.G')
speak_current_station('Unirii')
speak_next_station('Piata Alexandru cel Bun')
speak_current_station('Moara 1 Mai')
speak_next_station('Piata Independentei')
speak_next_station('Minerva')'''
'''
while 1:
    show_time()
    time.sleep(0.1)
'''
'''
display_next_station('Piata Alexandru cel Bun')
display_current_station('Unirii')
display_next_station('Piata Independentei')
display_current_station('C.U.G')
display_next_station('Moara 1 Mai')
display_next_station('Canta')'''
