import json
import time
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Function to get data of current measurement values
def get_data():
    measurements = requests.get("http://innov8dev.com/sampleapi/getdata.php")
    data = measurements.json()
    return data

# Function to save data to log file
def save_to_log(data):
    with open("measurement_log.txt", "a") as file:
        file.write(json.dumps(data) + "\n")

# Function to plot data
def plot_data(timestamps, temperatures, rain_presence):
    plt.figure(figsize=(8, 6))
    plt.title('Temperature and Rain Data')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.plot(timestamps, temperatures, label='Temperature (C)', color='red')
    plt.plot(timestamps, rain_presence, label="Rain (1 = raining, 0 = not raining)", linestyle='dashed', color='blue')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

# Function to read data from log file
def read_log_file():
    with open("measurement_log.txt", "r") as file:
        lines = file.readlines()
        data = [json.loads(line.strip()) for line in lines]
    return data
