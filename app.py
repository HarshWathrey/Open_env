from fastapi import FastAPI
from env.environment import SupportEnv

app = FastAPI()
env = SupportEnv()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/reset")
def reset(task_id: str):
    return env.reset(task_id).dict()

@app.post("/step")
def step(action: dict):
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