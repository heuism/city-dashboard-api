from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can narrow this to your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/cities")
def get_cities(min: int = Query(0, description="Minimum value")):
    time.sleep(1.5)  # Simulate 1.5s delay
    
    data = [
      { "city": "Melbourne", "temp": 10 },
      { "city": "Sydney", "temp": 20 },
      { "city": "Ho Chi Minh", "temp": 30 },
      { "city": "Adelaide", "temp": 10 },
      { "city": "Queensland", "temp": 25 }
    ];
    return [city for city in data if city["temp"] >= min]
