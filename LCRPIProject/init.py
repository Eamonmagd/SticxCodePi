# created by Eamon Magdoubi
import os
import RPi.GPIO as GPIO
import sqlite3
import datetime
import csv

from CloudCommunication import CloudCommunication
import time
from SensorObject import SensorObject



#ACCELEROMETER IMPORT
import smbus
import math

#GPIO Pins for sensor pins

DHTPIN = 11



#pins associatd with humit and temperature sensors
MAX_UNCHANGE_COUNT = 100
STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5


sensorObj = SensorObject()

cc = CloudCommunication()
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
busTwo = smbus.SMBus(3) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)
busTwo.write_byte_data(address, power_mgmt_1, 0)


from hx711 import HX711
hx = HX711(29, 31)
hxtwo = HX711(38, 40)

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")
hxtwo.set_reading_format("MSB", "MSB")
# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(92)

hx.reset()

hx.tare()

hxtwo.set_reference_unit(92)
hxtwo.reset()
hxtwo.tare()




global timeFromLast
def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location

def systemLoop():
    timeFromLast = int(time.time())
    while True:
        currentTime = int(time.time())
        
        try:
                        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
            # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
            # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
            
            # np_arr8_string = hx.get_np_arr8_string()
            # binary_string = hx.get_binary_string()
            # print binary_string + " " + np_arr8_string
            
            # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
            val = max(0, int(hx.get_weight(5)))
            
            valTwo = max(0, int(hxtwo.get_weight(5)))
            
            print((val/1000)*9.807)
            print((valTwo/1000)*9.807)
            sensorObj.weightIncrement((val/1000)*9.807,(valTwo/1000)*9.807)
            # To get weight from both channels (if you have load cells hooked up 
            # to both channel A and B), do something like this
            #val_A = hx.get_weight_A(5)
            #val_B = hx.get_weight_B(5)
            #print "A: %s  B: %s" % ( val_A, val_B )

            hx.power_down()
            hx.power_up()
            
            hxtwo.power_down()
            hxtwo.power_up()
            #acceleration is all three vertices
            accel_xout = read_word_2c(0x3b)
            accel_yout = read_word_2c(0x3d)
            accel_zout = read_word_2c(0x3f)

            accel_xout_scaled = accel_xout / 16384.0
            accel_yout_scaled = accel_yout / 16384.0
            accel_zout_scaled = accel_zout / 16384.0
            sensorObj.accelerationAxis(round(accel_xout_scaled,4), round(accel_yout_scaled,4), round(accel_zout_scaled,4))
            
            print ("accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled)
            print ("accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled)
            print ("accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled)
            
            #acceleration is all three vertices for second accelerometer
            accel_xoutTwo = read_word_2ctwo(0x3b)
            accel_youtTwo = read_word_2ctwo(0x3d)
            accel_zoutTwo = read_word_2ctwo(0x3f)

            accel_xout_scaledTwo = accel_xoutTwo / 16384.0
            accel_yout_scaledTwo = accel_youtTwo / 16384.0
            accel_zout_scaledTwo = accel_zoutTwo / 16384.0
            
                        
            print ("accel_xout2: ", accel_xoutTwo, " scaled: ", accel_xout_scaledTwo)
            print ("accel_yout2: ", accel_youtTwo, " scaled: ", accel_yout_scaledTwo)
            print ("accel_zout2: ", accel_zoutTwo, " scaled: ", accel_zout_scaledTwo)
            sensorObj.accelerationAxisTwo(round(accel_xout_scaledTwo,4), round(accel_yout_scaledTwo,4), round(accel_zout_scaledTwo,4))
            
        except:
            print("error")
    
        result = read_dht11_dat()
        if result:
            humidity, temperature = result
            #    V                UNCOMMENT FOR COMMAND LINE READING
            #print("humidity: %s %%,  Temperature: %s C`" % (humidity, temperature))
            sensorObj.tempHumidIncrement(temperature, humidity)

        #time.sleep(1)
        
        #checking the current time is atleast an hour since last transmission
        
        #    V                UNCOMMENT FOR COMMAND LINE READING
        #print((float(currentTime)-float(timeFromLast))/(60*60))
        # 0.60 = 1 hour      
        if (((float(currentTime)-float(timeFromLast))/(60*60))>0.60):
            sensorObj.averageCalculator()
            cc.addValue(sensorObj.temperatureAverage, sensorObj.humidityAverage, sensorObj.xAverage, sensorObj.yAverage, sensorObj.zAverage, sensorObj.weightAverage, sensorObj.weightTwoAverage, sensorObj.xAverageTwo, sensorObj.yAverageTwo, sensorObj.zAverageTwo)
            timeFromLast = int(time.time())
            sensorObj.resetValues()
        time.sleep(1)
def destroy():
    GPIO.cleanup()
    pass

#ACCELEREMOTER code to get acceleration values in g force
def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


#ACCELEREMOTER TWOcode to get acceleration values in g force
def read_bytetwo(adr):
    return busTwo.read_byte_data(address, adr)

def read_wordtwo(adr):
    high = busTwo.read_byte_data(address, adr)
    low = busTwo.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2ctwo(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


#DTH11 data for tempreture and humidity
def read_dht11_dat():
    GPIO.setwarnings(False)
    GPIO.setup(DHTPIN, GPIO.OUT)
    GPIO.output(DHTPIN, GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(DHTPIN, GPIO.LOW)
    time.sleep(0.02)
    GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

    unchanged_count = 0
    last = -1
    data = []
    while True:
        current = GPIO.input(DHTPIN)
        data.append(current)
        if last != current:
            unchanged_count = 0
            last = current
        else:
            unchanged_count += 1
            if unchanged_count > MAX_UNCHANGE_COUNT:
                break

    state = STATE_INIT_PULL_DOWN

    lengths = []
    current_length = 0

    for current in data:
        current_length += 1

        if state == STATE_INIT_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_INIT_PULL_UP
            else:
                continue
        if state == STATE_INIT_PULL_UP:
            if current == GPIO.HIGH:
                state = STATE_DATA_FIRST_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_FIRST_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_DATA_PULL_UP
            else:
                continue
        if state == STATE_DATA_PULL_UP:
            if current == GPIO.HIGH:
                current_length = 0
                state = STATE_DATA_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_PULL_DOWN:
            if current == GPIO.LOW:
                lengths.append(current_length)
                state = STATE_DATA_PULL_UP
            else:
                continue
    if len(lengths) != 40:
        #print("Data not good, skip")
        return False

    shortest_pull_up = min(lengths)
    longest_pull_up = max(lengths)
    halfway = (longest_pull_up + shortest_pull_up) / 2
    bits = []
    the_bytes = []
    byte = 0

    for length in lengths:
        bit = 0
        if length > halfway:
            bit = 1
        bits.append(bit)
    #print("bits: %s, length: %d" % (bits, len(bits)))
    for i in range(0, len(bits)):
        byte = byte << 1
        if (bits[i]):
            byte = byte | 1
        else:
            byte = byte | 0
        if ((i + 1) % 8 == 0):
            the_bytes.append(byte)
            byte = 0
    #print (the_bytes)
    checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
    if the_bytes[4] != checksum:
        #print("Data not good, skip")
        return False
    #return humidity and temp vals
    return the_bytes[0], the_bytes[2]
  
if __name__ == '__main__':
    try:
        setup()
        systemLoop()
    except KeyboardInterrupt:
        destroy() 