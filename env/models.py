from pydantic import BaseModel
from typing import List, Optional, Literal, Dict

class Ticket(BaseModel):
    id: str
    message: str
    customer_tier: str
    history: List[str]

class Observation(BaseModel):
    instruction: str
    ticket: Ticket
    step_count: int

class Action(BaseModel):
    action_type: Literal["classify","respond","escalate","request_info","close"]
    priority: Optional[Literal["low","medium","high","urgent"]] = None
    message: Optional[str] = None

class Reward(BaseModel):
    score: float
    breakdown: Dict[str, float]