from fastapi import FastAPI
from env import CrisisEnv
from models import Action
import uvicorn

app = FastAPI()
env = CrisisEnv()

@app.post("/reset")
def reset():
    return env.reset()

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

# ✅ REQUIRED MAIN FUNCTION
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

# ✅ REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()