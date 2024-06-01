"""
@brief Program to log environmental measurements and provide data through a FastAPI service.
@author Yasin YILDIRIM
@date 05/2024

This program retrieves environmental data from a remote server, logs the data, and provides
two API endpoints to access temperature data at specific timestamps and to calculate
the percentage of time it rained between two timestamps. It includes functions to plot
the collected data for visualization purposes.
"""

import json
import time
import requests
from fastapi import FastAPI
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pytz import timezone

app = FastAPI()

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
    plt.plot(timestamps, temperatures, label='Temperature (C)',color='red')
    plt.plot(timestamps, rain_presence, label="Rain (It's raining = 1, it's not raining = 0)", linestyle='dashed',color='blue')
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

# API for retrieving the temperature for timestamps entered by the user.
@app.get('/temperature')
async def get_temperature(timestamp:int):
    data = read_log_file()
    for entry in data:
        if timestamp == entry['timestamp']:
            temperature = entry['temperature']
            return {"Temperature": f"{temperature} C"}
    return {"Temperature": "Not found"}

# API that calculates the percentage of time it rained between two user-provided timestamps.
@app.get('/percentage')
async def get_percentage(timestamp1:int,timestamp2:int):
    data = read_log_file()
    rain_counter = 0
    entry_counter = 0
    for entry in data:
        if timestamp1 <= entry['timestamp'] <= timestamp2:
            if entry['rain_presence']:
                rain_counter += 1  # Increment the rain counter if rain was present in the entry
            entry_counter += 1  # Increment the total entry counter for each entry within the time range
            
            rain_percentage = (rain_counter/entry_counter)*100
    return {"Rain percentage between given time": rain_percentage}

# Main function
def main():
    print("----------Program has started----------\n")
    
    open("measurement_log.txt", "w").close()
    
    timestampDetermination = get_data()
    timestamp = timestampDetermination.get('timestamp',None)
    date_time = datetime.fromtimestamp(timestamp)
    print("Current Date and Time of Location (when program runs):", date_time, "| Time stamp:" ,timestamp)
    
    start_time = time.time()
    end_time = start_time + 600  # 10 minutes

    timestamps = []
    temperatures = []
    rain_presence = []
    rain_percent = 0    
    
    print("\nData is being saved to the log file...\n")
    
    five_minutes_left_printed = False
    one_minute_left_printed = False

    while time.time() < end_time:
        data = get_data()

        name = data.get('name', None)
        timestamp = data.get('timestamp', None)
        temperature = data.get('temperature', None)
        rain = data.get('rain', None)


        timestamps.append(timestamp)
        temperatures.append(temperature)
        rain_presence.append(True if rain else False)
        if rain:
            rain_percent += 1 # To calculate how many percent of the time was raining 

        save_to_log({'name': name ,'timestamp': timestamp, 'temperature': temperature, 'rain_presence': rain})
        #time.isoformat()

        time.sleep(2) # collect data in 2-second intervals
        remain_time = end_time - time.time()
        if 298 <= remain_time <= 302 and not five_minutes_left_printed:
            print("Only 5 minutes left before the program ends!")
            five_minutes_left_printed = True # To handle multiple printing

        if 58 <= remain_time <= 62 and not one_minute_left_printed:
            print("Only 1 minutes left before the program ends!\n")    
            one_minute_left_printed = True

    date_time = datetime.fromtimestamp(timestamp)
    print("Current Date and Time of Location (when program ends):", date_time)

    percentage_raining = (rain_percent / len(rain_presence)) * 100
    print(f"Percentage of time it was raining: {percentage_raining:.2f}%")
    
    time.sleep(5)
    # Plot the collected data
    plot_data(timestamps, temperatures, rain_presence)
    print("\n-----------Program has ended-----------")


if __name__ == "__main__":
    main()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


# uvicorn Blebox:app --reload
# localhost/docs to try API out
# You can also monitor the process in the terminal.
# Upon closing the figure, the program will terminate.

# The server referenced by the .com domain is located in France.
