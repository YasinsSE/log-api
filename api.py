from fastapi import APIRouter
from data_logger import read_log_file

router = APIRouter()

# API for retrieving the temperature for timestamps entered by the user.
@router.get('/temperature')
async def get_temperature(timestamp: int):
    data = read_log_file()
    for entry in data:
        if timestamp == entry['timestamp']:
            temperature = entry['temperature']
            return {"Temperature": f"{temperature} C"}
    return {"Temperature": "Not found"}

# API that calculates the percentage of time it rained between two user-provided timestamps.
@router.get('/percentage')
async def get_percentage(timestamp1: int, timestamp2: int):
    data = read_log_file()
    rain_counter = 0
    entry_counter = 0
    for entry in data:
        if timestamp1 <= entry['timestamp'] <= timestamp2:
            if entry['rain_presence']:
                rain_counter += 1  # Increment the rain counter if rain was present in the entry
            entry_counter += 1  # Increment the total entry counter for each entry within the time range
    rain_percentage = (rain_counter / entry_counter) * 100 if entry_counter > 0 else 0
    return {"Rain percentage between given time": rain_percentage}
