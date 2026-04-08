from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import SupportEnv
from env.models import Action

app = FastAPI()
env = SupportEnv()

# -------- Health --------
@app.get("/")
def health():
    return {"status": "ok"}


# -------- Reset --------
class ResetRequest(BaseModel):
    task_id: str = "easy"   # default (important fallback)

@app.post("/reset")
def reset(req: ResetRequest = ResetRequest()):
    obs = env.reset(req.task_id)
    return obs.dict()


# -------- Step --------
@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action.dict())
    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    }


# -------- State --------
@app.get("/state")
def state():
    return env.state()
    
