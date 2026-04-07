import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env import CrisisEnv
from models import Action
from tasks.hard import get_hard_incidents

def simple_policy(state):
    # Rule based priority -> if severity is high, respond. If low confidence (simulated via strict threshold), ignore
    if len(state.incidents) > 0:
        sorted_incidents = sorted(state.incidents, key=lambda x: x.severity, reverse=True)
        incident = sorted_incidents[0]
        
        if incident.severity > 0.7:
            resource_map = {"Fire": "fire_truck", "Medical": "ambulance", "Police": "police"}
            res = resource_map.get(incident.type, "ambulance")
            return Action(action_type="dispatch", resource=res, target=incident.location)
        else:
            return Action(action_type="ignore", resource="", target=incident.location)
            
    return Action(action_type="ignore", resource="", target="None")

def grade(env=None):
    if env is None:
        env = CrisisEnv()
        
    total_reward = 0
    state = env.reset()
    env.incidents = get_hard_incidents()
    done = False
    
    while not done:
        action = simple_policy(state)
        state, reward, done, _ = env.step(action)
        total_reward += reward

    return max(0.0, min(1.0, total_reward / 60.0))

if __name__ == "__main__":
    print(f"Hard Grader Score: {grade()}")
