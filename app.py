from fastapi import FastAPI
from env.environment import SupportEnv

app = FastAPI()
env = SupportEnv()

@app.get("/")
def health():
    return {"status": "ok"}

from pydantic import BaseModel

class ResetRequest(BaseModel):
    task_id: str

@app.post("/reset")
def reset(req: ResetRequest):
    obs = env.reset(req.task_id)
    return obs.dict()

from env.models import Action

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action.dict())
    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    }
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()
