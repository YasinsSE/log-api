#Overview

#This program is designed to log environmental measurements, such as temperature and rain presence, from a remote server. It saves the collected data to a log file and provides two API endpoints to access the temperature data at specific timestamps and to calculate the percentage of time it rained between two timestamps. The program also includes a feature to plot the collected data for visualization purposes.

Features
- **Data Retrieval:** Fetches environmental data from a remote server.
- **Data Logging:** Saves the fetched data to a log file (`measurement_log.txt`).
- **Data Visualization:** Plots the collected data (temperature and rain presence) using `matplotlib`.
- **API Endpoints:** Provides two endpoints via FastAPI:
  - `/temperature`: Retrieve the temperature at a specific timestamp.
  - `/percentage`: Calculate the percentage of time it rained between two timestamps.

 
  ## Usage
1. **Run the program:**
    ```sh
    python main.py
    ```

2. **Access the API:**
    The FastAPI server will run locally at `127.0.0.1:8000`. You can interact with the API endpoints using a tool like Postman or directly via your web browser.

3. **API Endpoints:**
    - **Retrieve Temperature:**
        ```http
        GET /temperature?timestamp=<timestamp>
        ```
        Replace `<timestamp>` with the desired timestamp.

    - **Calculate Rain Percentage:**
        ```http
        GET /percentage?timestamp1=<timestamp1>&timestamp2=<timestamp2>
        ```
        Replace `<timestamp1>` and `<timestamp2>` with the desired timestamps.

4. **Visualize Data:**
    After the program has run for the specified duration (10 minutes), it will plot the collected temperature and rain data.

Notes
The program logs data for a duration of 10 minutes, collecting data every 2 seconds.
The timestamps are logged in Unix timestamp format.
The API documentation is available at http://127.0.0.1:8000/docs.
