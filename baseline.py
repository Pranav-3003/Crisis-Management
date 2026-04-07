from env import CrisisEnv
from models import Action

env = CrisisEnv()
state = env.reset()

print("Starting Baseline Evaluation...\n")

steps = 0
total_reward = 0

while True:
    if len(state.incidents) > 0:
        incident = state.incidents[0]
        resource_map = {"Fire": "fire_truck", "Medical": "ambulance", "Police": "police"}
        res = resource_map.get(incident.type, "ambulance")
        action = Action(action_type="dispatch", resource=res, target=incident.location)
        print(f"Step {steps} | Action: Dispatching {res} to {incident.location}")
    else:
        action = Action(action_type="ignore", resource="", target="None")
        print(f"Step {steps} | Action: Ignore (No incidents)")

    state, reward, done, _ = env.step(action)
    total_reward += reward
    print(f"Reward this step: {reward} | Cumulative: {total_reward}\n")
    
    steps += 1
    if done:
        break

print(f"Baseline Phase Complete. Final Score/Reward: {total_reward}")
