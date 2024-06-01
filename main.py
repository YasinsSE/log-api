"""
@file main.py
@brief Program to log environmental measurements and provide data through a FastAPI service.
@author Yasin YILDIRIM
@date 05/2024

This program retrieves environmental data from a remote server, logs the data, and provides
two API endpoints to access temperature data at specific timestamps and to calculate
the percentage of time it rained between two timestamps. It includes functions to plot
the collected data for visualization purposes.
"""

from fastapi import FastAPI
import uvicorn
from data_logger import get_data, save_to_log, plot_data, read_log_file
from api import router

app = FastAPI()
app.include_router(router)

# Main function
def main():
    print("----------Program has started----------\n")

    open("measurement_log.txt", "w").close()

    timestampDetermination = get_data()
    timestamp = timestampDetermination.get('timestamp', None)
    date_time = datetime.fromtimestamp(timestamp)
    print("Current Date and Time of Location (when program runs):", date_time, "| Time stamp:", timestamp)

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
            rain_percent += 1  # To calculate how many percent of the time was raining 

        save_to_log({'name': name, 'timestamp': timestamp, 'temperature': temperature, 'rain_presence': rain})

        time.sleep(2)  # Collect data in 2-second intervals
        remain_time = end_time - time.time()
        if 298 <= remain_time <= 302 and not five_minutes_left_printed:
            print("Only 5 minutes left before the program ends!")
            five_minutes_left_printed = True  # To handle multiple printing

        if 58 <= remain_time <= 62 and not one_minute_left_printed:
            print("Only 1 minute left before the program ends!\n")    
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
    uvicorn.run(app, host="127.0.0.1", port=8000)

# uvicorn main:app --reload
# localhost/docs to try API out
# You can also monitor the process in the terminal.
# Upon closing the figure, the program will terminate.

# The server referenced by the .com domain is located in France.

# The timestamps in the measurement_log.txt are in the format "timestamp":1634000000 as specified.
