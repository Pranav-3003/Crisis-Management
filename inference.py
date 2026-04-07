from env import CrisisEnv
from models import Action

def run():
    env = CrisisEnv()
    state = env.reset()

    total_reward = 0
    done = False

    while not done:
        action = Action(
            action_type="dispatch",
            resource="ambulance",
            target="Zone A"
        )

        state, reward, done, _ = env.step(action)
        total_reward += reward

    return {
        "status": "completed",
        "total_reward": float(total_reward)
    }

if __name__ == "__main__":
    result = run()
    print(result)