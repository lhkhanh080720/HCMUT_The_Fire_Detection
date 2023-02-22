import time
import datetime

count = time.time()
while True:
    if time.time() - count >= 20:
        count = time.time()
        current_time = datetime.datetime.now().time()
        print("===========================")
        print("TIME = " + str(current_time.strftime("%H:%M:%S")))
        with open("/sys/devices/virtual/thermal/thermal_zone1/temp", "r") as temp_file:
            print("CPU: " + str(int(temp_file.read().strip())/1000))
        with open("/sys/devices/virtual/thermal/thermal_zone2/temp", "r") as temp_file:
            print("GPU: " + str(int(temp_file.read().strip())/1000))
        with open("/sys/devices/virtual/thermal/thermal_zone5/temp", "r") as temp_file:
            print("Thermal Fan: " + str(int(temp_file.read().strip())/1000))