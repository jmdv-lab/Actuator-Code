# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:17:15 2023

@author: SDU
"""

import serial
import time
import csv

data = []
ser = serial.Serial("COM7", 115200, timeout=1)

def bend_control(ser, bend_val):    #angle on the range of 0 to +180
    ser_bytes = ser.readline()
    ser.flushInput()
    time.sleep(0.001)
    motor_bend=str(bend_val)
    cmd="a"+motor_bend+"\n"
    #print(cmd)
    ser.write(bytes(cmd, encoding="ascii"))

angle = -10
direction = 1
start_time = time.time()
line_count = 0
#total_time = 220

# Loop until total record time has elapsed
while time.time() - start_time < 1050 :
   # if angle % 10 == 0:  # Check if angle is a multiple of 10 (10, 20, 30, etc.)
    record_time = time.time()
    angle += direction * 10
    if angle > 100 or angle < 0:
        direction *= -1
    cmd = "a" + str(angle) + "\n"
    #ser.write(cmd.encode())
    bend_control(ser, angle)
   
    while time.time() - record_time <= 50:  # Record data for 150 seconds
    # Read data from serial port
        line = ser.readline().decode("utf-8").rstrip()
    
        # Ignore first 2 lines of serial communication
        # Increment line counter
        line_count += 1
    
        # Ignore first two lines of serial communication
        if line_count <= 1:
            print("Skipping line:", line)
            continue
    
        # Split data into list of values using comma as delimiter
        values = line.split(',')
        print(values)
    
        if len(values)<4:
            print("Skipping line:", line)
            continue
    
        # Convert values to float and append to data list
        try:
            data.append([time.time() - start_time, values[0], values[1], values[2], values[3]])
        except ValueError:
            continue
        time.sleep(0.01)

ser.close()

# Save data to CSV file
filename = "datagptcontroller70.csv"
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "Value 1", "Value 2", "Value 3", "Value 4"])
    writer.writerows(data)

print("Data saved to file:", filename)
