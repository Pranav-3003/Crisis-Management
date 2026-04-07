from pydantic import BaseModel
from typing import List

class Incident(BaseModel):
    type: str
    severity: float
    location: str
    is_real: bool

class Resource(BaseModel):
    ambulance: int
    fire_truck: int
    police: int

class Observation(BaseModel):
    time: int
    incidents: List[Incident]
    resources: Resource

class Action(BaseModel):
    action_type: str  # dispatch / ignore / verify
    resource: str
    target: str

class Reward(BaseModel):
    score: float
