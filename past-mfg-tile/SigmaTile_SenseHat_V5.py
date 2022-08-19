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

import Queue as queue
from collections import deque
import numpy

from sense_hat import SenseHat

#---------------------------------------------------------------------------#
# Global Variables
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
# Worker Functions
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
# Worker Function - updates the modbus server based on the sensors
#---------------------------------------------------------------------------#
def update_sensor_datastore(sense, context, vibrationQueue): # Updates the sensors

    sleep(3)
    logging.debug('Polling Sensors')
    register = 3
    slave_id = 0x00
    address  = 0x00

    while (True):
       	newValues = []

        newValues.extend(float_to_uint16((32+1.8*sense.temperature)))
    	newValues.extend(float_to_uint16(sense.humidity))
    	newValues.extend(float_to_uint16(sense.pressure))

    	acceleration = sense.accel_raw
        vibrationQueue.put(acceleration)
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

#---------------------------------------------------------------------------#
# Worker Function - manages the content displayed on the sense hat screen
#---------------------------------------------------------------------------#
def display_manager(sense, context, IP_Address):
    joystickControl = 0
    errorCode = 100

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

    image_warning = [
        e,e,y,y,y,y,e,e,
        e,y,y,w,w,y,y,e,
        y,y,y,w,w,y,y,y,
        y,y,y,w,w,y,y,y,
        y,y,y,w,w,y,y,y,
        y,y,y,y,y,y,y,y,
        e,y,y,w,w,y,y,e,
        e,e,y,y,y,y,e,e,
        ]
    image_running = [
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
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
    image_notconfigured = [
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        e,e,e,e,e,e,e,e,
        ]

    previousValues = 100

    for i in range (0, 3):
        sense.show_message(IP_Address)

    while(True):
        values = context[0x00].getValues(3, 0x18, count=1)
        for event in sense.stick.get_events():
            if (event.action == 'pressed' and event.direction == 'right'):
                if joystickControl < 3:
                    joystickControl += 1
                else:
                    joystickControl = 0
            if (event.action == 'pressed' and event.direction == 'left'):
                if joystickControl > 0:
                    joystickControl -= 1
                else:
                    joystickControl = 3
            if (event.action == 'pressed' and event.direction == 'up'):
                if errorCode < 105:
                    errorCode += 1
                else:
                    errorCode = 100
            if (event.action == 'pressed' and event.direction == 'down'):
                if errorCode > 100:
                    errorCode -= 1
                else:
                    errorCode = 105
        logging.info(errorCode)
        context[0x00].setValues(3, 0x1B, [errorCode])
        if (values[0] != previousValues or joystickControl == 0):
            #logging.info('Screen State Changing')
            previousValues = values[0]
            joystickControl = 0
            if values[0] == 1:
                #sense.show_message("Alert Triggered!", scroll_speed = .05, text_colour = [255,255,255])
                sense.set_pixels(image_warning)
            elif values[0] == 2:
                sense.set_pixels(image_running)
            elif values[0] == 3:
                #sense.show_message("Planned Downtime", scroll_speed = .05, text_colour = [255,255,255])
                sense.set_pixels(image_plannedDowntime)
            elif values[0] == 4:
                #sense.show_message("Unplanned Downtime!", scroll_speed = .05, text_colour = [255,255,255])
                sense.set_pixels(image_unplannedDowntime)
            elif values[0] == 5:
                #sense.show_message("System Unavailable", scroll_speed = .05, text_colour = [255,255,255])
                sense.set_pixels(image_unavailable)
            else:
                sense.set_pixels(image_notconfigured)
        elif joystickControl == 1:
            sense.show_message('Temperature: {} C'.format(round(sense.temperature),2))
        elif joystickControl == 2:
            sense.show_message('Humidity: {} %'.format(round(sense.humidity),2))
        elif joystickControl == 3:
            sense.show_message('Pressure: {} mbar'.format(round(sense.pressure),2))
        else:
            sleep(1)

def part_creator(sense, context):
    goodCount = 0
    badCount = 0
    sleep(3)
    while(True):
        anomaly = context[0x00].getValues(3, 0x1C, count=1)
        if (anomaly[0] < 1):
            failureChance = sense.temperature * .0346 - .8154
        else:
            failureChance = 1-(sense.temperature * .0346 - .8154)
        if (random.random() < failureChance):
            badCount = badCount + 1
        else:
            goodCount = goodCount + 1
        context[0x00].setValues(3, 0x19, [goodCount, badCount])
        sleep(sense.pressure*.0059 - 4.12)

def alert_detection(vibrationQueue, context):
    xVibration = deque([],100)
    yVibration = deque([],100)
    zVibration = deque([],100)
    vibrationAlertDetector = 0
    vibrationAlert = 0

    while(True):
        latestSample = vibrationQueue.get()
        xVibration.append(abs(latestSample["x"]))
        yVibration.append(abs(latestSample["y"]))
        zVibration.append(abs(latestSample["z"]))
        xVibrationMean = numpy.mean(xVibration)
        yVibrationMean = numpy.mean(yVibration)
        zVibrationMean = numpy.mean(zVibration)
        if((xVibrationMean + yVibrationMean + zVibrationMean) > 1.4):
            vibrationAlertDetector = 1000 * 2 # Persistence of the anomaly - multiply by number of minutes for anomaly to last
        elif(vibrationAlertDetector > 0):
            vibrationAlertDetector = vibrationAlertDetector - 1
            vibrationAlert = 1
        else:
            vibrationAlert = 0

        context[0x00].setValues(3, 0x1C, [vibrationAlert])


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
vibrationQueue = queue.Queue()

Query = threading.Thread(name = 'Query', target = update_sensor_datastore, args = (sense, context, vibrationQueue))
Query.setDaemon(True)
Query.start()

Screen = threading.Thread(name = 'Screen', target = display_manager, args = (sense, context, IP_Address))
Screen.setDaemon(True)
Screen.start()

Parts = threading.Thread(name = 'Parts', target = part_creator, args = (sense, context))
Parts.setDaemon(True)
Parts.start()

Alert = threading.Thread(name = 'Anomaly', target = alert_detection, args = (vibrationQueue, context))
Alert.setDaemon(True)
Alert.start()

StartTcpServer(context, identity=identity, address=(IP_Address, 502))
