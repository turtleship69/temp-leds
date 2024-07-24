from Arduino import Arduino
import wmi
import time

from config import BAUD, PORT

# Set up Arduino board

board = Arduino(BAUD, port=PORT)
pins = [3, 4, 5, 6, 7, 8]

for pin in pins:
    board.pinMode(pin, "OUTPUT")

# Define temperature thresholds
green2_temp = 40 # Celsius
green3_temp = 45
yellow1_temp = 50
yellow2_temp = 65
critical_temp = 70


def get_cpu_temp():
    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
    temperature_info = w.Sensor()
    if not temperature_info:
        import os
        os.popen("start ./OpenHardwareMonitor.exe")
        # input("press enter to continue")

    # Loop through sensor data to find the CPU temperature
    for sensor in temperature_info:
        if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
            return sensor.Value

    return None


while True:
    cpu_temp = get_cpu_temp()

    # Set all LEDs to LOW initially
    lights = ["HIGH", "LOW", "LOW", 
              "LOW", "LOW", "LOW", ]
    

    if cpu_temp >= green2_temp:
        lights[1] = "HIGH"
    if cpu_temp >= green3_temp:
        lights[2] = "HIGH"
    if cpu_temp >= yellow1_temp:
        lights[3] = "HIGH"
    if cpu_temp >= yellow2_temp:
        lights[4] = "HIGH"
    if cpu_temp > critical_temp:
        lights[5] = "HIGH"

    #print(lights, flush=True)
    
    for pin, state in zip(pins, lights):
        board.digitalWrite(pin, state)

    # Adjust delay as needed (e.g., 1 second)
    time.sleep(1)
