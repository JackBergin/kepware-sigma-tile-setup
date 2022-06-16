#!/usr/bin/env python

#---------------------------------------------------------------------------#
# Import Packages and Functions
#---------------------------------------------------------------------------#

from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
import random

from struct import pack, unpack

from time import sleep

import socket
import logging
import threading

from sense_hat import SenseHat

#---------------------------------------------------------------------------#
# Package Modifications
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
# Worker Functions
#---------------------------------------------------------------------------#
def update_sensor_datastore(sense, context): # Updates the sensors

    sleep(3)
    logging.debug('Polling Sensors')
    register = 3
    slave_id = 0x00
    address  = 0x00

    while (True):
       	newValues = []

        newValues.extend(float_to_uint16(sense.temperature))
    	newValues.extend(float_to_uint16(sense.humidity))
    	newValues.extend(float_to_uint16(sense.pressure))

    	acceleration = sense.accel_raw
    	newValues.extend(float_to_uint16(acceleration["x"]))
    	newValues.extend(float_to_uint16(acceleration["y"]))
    	newValues.extend(float_to_uint16(acceleration["z"]))

    	gyroscope = sense.gyro_raw
    	newValues.extend(float_to_uint16(gyroscope["x"]))
    	newValues.extend(float_to_uint16(gyroscope["y"]))
    	newValues.extend(float_to_uint16(gyroscope["z"]))

    	orientation = sense.orientation
    	newValues.extend(float_to_uint16(orientation["roll"]))
    	newValues.extend(float_to_uint16(orientation["pitch"]))
    	newValues.extend(float_to_uint16(orientation["yaw"]))


    	context[slave_id].setValues(register, address, newValues)

def display_manager(sense, context, IP_Address):
    r = [255,0,0]
    o = [255,127,0]
    y = [255,255,0]
    w = [255,255,255]
    g = [0,120,0]
    lg =[0,100,0]
    b = [0,0,255]
    i = [75,0,130]
    v = [159,0,255]
    e = [0,0,0]

    image_running = [
        e,e,g,g,g,g,e,e,
        e,g,g,g,g,g,g,e,
        g,g,g,g,g,w,g,g,
        g,g,g,g,w,g,g,g,
        g,w,g,g,w,g,g,g,
        g,g,w,w,g,g,g,g,
        e,g,g,w,g,g,g,e,
        e,e,g,g,g,g,e,e,
        ]
    connecting_images = []
    connecting_images.append([
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,b,b,e,e,e,
        e,e,b,e,e,b,e,e,
        e,e,e,e,e,e,e,e,
        ])
    connecting_images.append([
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,b,b,b,b,e,e,
        e,b,e,e,e,e,b,e,
        e,e,e,b,b,e,e,e,
        e,e,b,e,e,b,e,e,
        e,e,e,e,e,e,e,e,
        ])
    connecting_images.append([
        e,e,b,b,b,b,e,e,
        e,b,e,e,e,e,b,e,
        b,e,e,e,e,e,e,b,
        e,e,b,b,b,b,e,e,
        e,b,e,e,e,e,b,e,
        e,e,e,b,b,e,e,e,
        e,e,b,e,e,b,e,e,
        e,e,e,e,e,e,e,e,
        ])
    image_warning = [
        e,e,e,y,e,e,e,e,
        e,e,e,y,e,e,e,e,
        e,e,y,r,y,e,e,e,
        e,e,y,r,y,e,e,e,
        e,y,y,r,y,y,e,e,
        e,y,y,y,y,y,e,e,
        y,y,y,r,y,y,y,e,
        y,y,y,y,y,y,y,e,
        ]
    image_unplannedDowntime = [
        e,e,r,r,r,r,e,e,
        e,w,r,r,r,r,w,e,
        r,r,w,r,r,w,r,r,
        r,r,r,w,w,r,r,r,
        r,r,r,w,w,r,r,r,
        r,r,w,r,r,w,r,r,
        e,w,r,r,r,r,w,e,
        e,e,r,r,r,r,e,e,
        ]
    image_plannedDowntime = [
        e,e,b,b,b,b,e,e,
        e,b,b,b,b,b,b,e,
        b,b,b,b,b,w,b,b,
        b,b,b,b,w,b,b,b,
        b,w,b,b,w,b,b,b,
        b,b,w,w,b,b,b,b,
        e,b,b,w,b,b,b,e,
        e,e,b,b,b,b,e,e,
        ]
    image_unavailable = [
        e,e,w,w,w,w,e,e,
        e,w,e,e,e,w,w,e,
        w,e,e,e,w,w,e,w,
        w,e,e,w,w,e,e,w,
        w,e,w,w,e,e,e,w,
        w,w,w,e,e,e,e,w,
        e,w,e,e,e,e,w,e,
        e,e,w,w,w,w,e,e,
        ]
    image_errorInLast24 = [
        e,e,o,o,o,o,e,e,
        e,o,o,w,w,o,o,e,
        o,o,o,w,w,o,o,o,
        o,o,w,w,w,w,o,o,
        o,o,w,w,w,w,o,o,
        o,w,w,w,w,w,w,o,
        e,o,o,o,o,o,o,e,
        e,e,o,o,o,o,e,e,
        ]
    previousValues = 100

    for i in range (0, 3):
        sense.show_message(IP_Address)

    logging.info('Initialization Complete')
    while(True):
        values = context[0x00].getValues(3, 0x18, count=1)
        if values[0] != previousValues:
            logging.info('Screen State Changing')
            previousValues = values[0]
            if values[0] == 0:
                sense.set_pixels(image_running)
            elif values[0] == 1:
                sense.show_message("Alert Triggered!", scroll_speed = .05, text_colour = [255,255,255])
                sense.set_pixels(image_warning)
            elif values[0] == 2:
                sense.show_message("Planned Downtime", scroll_speed = .05, text_colour = [255,255,255])
                sense.set_pixels(image_plannedDowntime)
            elif values[0] == 3:
                sense.show_message("Unplanned Downtime!", scroll_speed = .05, text_colour = [255,255,255])
                sense.set_pixels(image_unplannedDowntime)
            elif values[0] == 4:
                sense.show_message("Error in last 24 Hours", scroll_speed = .05, text_colour = [255,255,255])
                sense.set_pixels(image_errorInLast24)
            elif values[0] == 5:
                sense.show_message("System Unavailable", scroll_speed = .05, text_colour = [255,255,255])
                sense.set_pixels(image_unavailable)
            else:
                sense.show_message('PTC Sigma Tile')
        else:
            sleep(1)

def part_creator(sense, context):
    goodCount = 0
    badCount = 0
    sleep(3)
    while(True):
        failureChance = sense.temperature * .0346 - .8154
        if (random.random() < failureChance):
            badCount = badCount + 1
        else:
            goodCount = goodCount + 1
        context[0x00].setValues(3, 0x19, [goodCount, badCount])
        sleep(sense.pressure*.1 + 115)


#---------------------------------------------------------------------------#
# Helper Functions
#---------------------------------------------------------------------------#
def float_to_uint16(number):
    i1, i2 = unpack('HH', pack('f', number))
    return i1, i2

def initialize(): # Function Initialization
    network_connected = False
    connecting_images = []
    sense = SenseHat()
    e = [0,0,0]
    b = [0,0,255]
    connecting_images.append([
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,b,b,e,e,e,
        e,e,b,e,e,b,e,e,
        e,e,e,e,e,e,e,e,
        ])
    connecting_images.append([
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,b,b,b,b,e,e,
        e,b,e,e,e,e,b,e,
        e,e,e,b,b,e,e,e,
        e,e,b,e,e,b,e,e,
        e,e,e,e,e,e,e,e,
        ])
    connecting_images.append([
        e,e,b,b,b,b,e,e,
        e,b,e,e,e,e,b,e,
        b,e,e,e,e,e,e,b,
        e,e,b,b,b,b,e,e,
        e,b,e,e,e,e,b,e,
        e,e,e,b,b,e,e,e,
        e,e,b,e,e,b,e,e,
        e,e,e,e,e,e,e,e,
        ])
    while (network_connected==False):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com",80))
            IP_Address = s.getsockname()[0]
            s.close()
        except:
            for image in range(3):
                sense.set_pixels(connecting_images[image])
                sleep(1)
        else:
            network_connected = True
    return IP_Address, sense

#---------------------------------------------------------------------------#
# Main Function
#---------------------------------------------------------------------------#

# Define global connections variable
#number_connections = 0

# Set logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

# Initialize your data store
store = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [1]*100),
    co = ModbusSequentialDataBlock(0, [2]*100),
    hr = ModbusSequentialDataBlock(0, [0]*100),
    ir = ModbusSequentialDataBlock(0, [4]*100))
context = ModbusServerContext(slaves=store, single=True)

# Initialize the server information
identity = ModbusDeviceIdentification()
identity.VendorName  = 'pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl   = 'http://github.com/bashwork/pymodbus/'
identity.ProductName = 'pymodbus Server'
identity.ModelName   = 'pymodbus Server'
identity.MajorMinorRevision = '1.0'


# Run the server you want
IP_Address, sense = initialize()
Query = threading.Thread(name = 'Query', target = update_sensor_datastore, args = (sense, context))
Query.setDaemon(True)
Query.start()

Screen = threading.Thread(name = 'Screen', target = display_manager, args = (sense, context, IP_Address))
Screen.setDaemon(True)
Screen.start()

Parts = threading.Thread(name = 'Parts', target = part_creator, args = (sense, context))
Parts.setDaemon(True)
Parts.start()

StartTcpServer(context, identity=identity, address=(IP_Address, 502))
