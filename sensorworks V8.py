import obd
import os
import smbus
from gpiozero import LED
from time import sleep
import time
from get_safe_distance import*
import serial
from get_lidar import*
import Queue
import threading

distance = Queue.LifoQueue()
speed = Queue.LifoQueue()

#connect to OBDII via built in bluetooth module
os.system("bluetoothctl")
os.system("trust 00:1D:A5:00:00:2E")
os.system("pair 00:1D:A5:00:00:2E")
os.system("exit")

#create a virtual serail com port for OBDII communication
os.system("sudo rfcomm bind 0 00:1D:A5:00:00:2E")

connection = obd.OBD("/dev/rfcomm0", baudrate = 115200) # auto-connects to RF port

#set LED to GPIO pin 11,13,15
red = LED(11)
yellow = LED(13)
green = LED(15)

#init system blink 3 time OBD connection established
for i in range(0,3):
    red.on()
    yellow.on()
    green.on()
    time.sleep(1)
    red.off()
    yellow.off()
    green.off()
    time.sleep(1)

#creates a serial instance to communicate with the lidar
ser = serial.Serial(
   port='/dev/ttyUSB0',
   baudrate = 115200,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=10
)

#lidar thread calls. Updates the distance lifoqueue with the distance measurements
def lidar_read(s, distance):
    while 1:
        try:
            dis = float(s.readline().split()[0])
            distance.put(dis)
        except:
            pass
        
#OBD thread calls. Updates the speed lifoqueue with the speed measurements        
def obd_read(connection, speed):
    while 1:
        cmd = obd.commands.SPEED # select an OBD command (sensor)
        response = connection.query(cmd) # send the command, and parse the response
        speed.put(response.value.to("mph").magnitude) # add the speed reading to the speed lifoqueue


#Alert thread indicates danger of collision based on current speed and distance
#to the front car
def alert():
    while 1:
        s = speed.get()
        current_distance = distance.get()*3.28084
        safe_distance = getSafeDistance(s)
        stopping_distance = getStoppingDistance(s)

        #print "curr: ", current_distance, "ft\n", "safe: ", safe_distance,"ft\n",\
              #"stopping: ",stopping_distance, "ft\n", "speed: ", s, "mph"

        #print "\n\n"
        
        if(current_distance >= safe_distance):
            red.off()
            yellow.off()
            green.on()
            #print "green"
            
        elif(current_distance < safe_distance and current_distance >= stopping_distance):
            red.off()
            yellow.on()
            green.off()
            #print "yellow"
            
        elif(current_distance < stopping_distance):
            red.blink(0.01, 0.01)
            yellow.off()
            green.off()
            #print "red"

#Create 3 threads to read OBD and the lidar and alert the user
thread1 = threading.Thread(target = lidar_read, args = (ser, distance,),)
thread2 = threading.Thread(target = obd_read, args = (connection, speed,),)
thread3 = threading.Thread(target = alert, args = (),)

#begin the 3 threads
thread1.start()
thread2.start()
thread3.start()



    
