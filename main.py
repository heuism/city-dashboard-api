import json
from pathlib import Path
from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import time

from pydantic import BaseModel

app = FastAPI()

class CityAndTemp(BaseModel):
    city: str
    temp: int

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can narrow this to your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_cities() -> List[CityAndTemp]:
  if not file_path:
    return []
  with open(file_path) as f:
    raw_data = json.load(f)
    return [CityAndTemp(**city) for city in raw_data]
  
def save_cities(cities: List[CityAndTemp]):
  with open(file_path, "w") as f:
    json.dump([city.dict() for city in cities], f, indent=2)

file_path = Path("cities.json")
data: List[CityAndTemp] = []

data = load_cities()

@app.get("/cities")
def get_cities(min: int = Query(0, description="Minimum value")):
    time.sleep(1.5)  # Simulate 1.5s delay
    
    data = load_cities()
    
    return [city.dict() for city in data if city.temp >= min]

@app.post("/cities")
def add_cities(city: CityAndTemp):
    time.sleep(1.5)  # Simulate 1.5s delay
    data = load_cities()
    data.append(city)
    save_cities(data)
    return {"received": city}