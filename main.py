import json
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import time

from sqlmodel import SQLModel, Field, Session, create_engine, select
from pydantic import BaseModel

app = FastAPI()

class CityAndTemp(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    city: str
    temp: int

sqlite_file = "cities.db"
engine = create_engine(f"sqlite:///{sqlite_file}", echo=True)

# Create the table if it doesn't exist
SQLModel.metadata.create_all(engine)

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

def seed_cities_to_db():
    if not file_path.exists():
        print("cities.json not found.")
        return

    with open(file_path) as f:
        raw_data = json.load(f)
        cities = [CityAndTemp(**city) for city in raw_data]

        with Session(engine) as session:
            session.add_all(cities)
            session.commit()
            print(f"✅ Seeded {len(cities)} cities into the database.")

@app.get("/cities")
def get_cities(min: int = Query(0, description="Minimum value")):
    with Session(engine) as session:
        print(min)
        statement = select(CityAndTemp).where(CityAndTemp.temp >= min)
        results = session.exec(statement).all()
        return results

@app.post("/cities")
def add_cities(city: CityAndTemp):
    with Session(engine) as session:
        session.add(city)
        session.commit()
        session.refresh(city)
        
        cities = session.exec(select(CityAndTemp)).all()
        return cities
      
if __name__ == "__main__":
    seed_cities_to_db()