from env import CrisisEnv
from models import Action

env = CrisisEnv()
state = env.reset()

done = False

while not done:
    action = Action(
        action_type="dispatch",
        resource="ambulance",
        target="Zone A"
    )
    state, reward, done, _ = env.step(action)
    print("Reward:", reward)