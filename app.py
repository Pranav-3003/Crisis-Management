from fastapi import FastAPI
from env import CrisisEnv
from models import Action

app = FastAPI()

env = CrisisEnv()

@app.post("/reset")
def reset():
    state = env.reset()
    return state

@app.post("/step")
def step(action: Action):
    state, reward, done, info = env.step(action)
    return {
        "observation": state,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()