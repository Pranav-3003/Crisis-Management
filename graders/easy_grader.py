import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env import CrisisEnv
from models import Action
from tasks.easy import get_easy_incidents

def simple_policy(state):
    if len(state.incidents) > 0:
        incident = state.incidents[0]
        if incident.type == "Fire":
            return Action(action_type="dispatch", resource="fire_truck", target=incident.location)
    return Action(action_type="ignore", resource="", target="None")

def grade(env=None):
    if env is None:
        env = CrisisEnv()
    
    total_reward = 0
    state = env.reset()
    env.incidents = get_easy_incidents()
    done = False
    
    while not done:
        action = simple_policy(state)
        state, reward, done, _ = env.step(action)
        total_reward += reward

    return max(0.0, min(1.0, total_reward / 20.0))

if __name__ == "__main__":
    print(f"Easy Grader Score: {grade()}")
