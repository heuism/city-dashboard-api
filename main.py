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

data: List[CityAndTemp] = [
    CityAndTemp(city="Melbourne", temp=10),
    CityAndTemp(city="Sydney", temp=20),
    CityAndTemp(city="Ho Chi Minh", temp=30),
    CityAndTemp(city="Adelaide", temp=10),
    CityAndTemp(city="Queensland", temp=25),
]

@app.get("/cities")
def get_cities(min: int = Query(0, description="Minimum value")):
    time.sleep(1.5)  # Simulate 1.5s delay
    
    
    return [city.dict() for city in data if city.temp >= min]

@app.post("/cities")
def add_cities(city: CityAndTemp):
    time.sleep(1.5)  # Simulate 1.5s delay
    data.append(city)
    return {"received": city}