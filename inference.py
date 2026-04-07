from env import CrisisEnv
from models import Action

def run():
    env = CrisisEnv()
    state = env.reset()

    done = False

    while not done:
        # simple baseline logic
        if len(state.incidents) > 0:
            action = Action(
                action_type="dispatch",
                resource="ambulance",
                target="Zone A"
            )
        else:
            action = Action(
                action_type="ignore",
                resource="",
                target=""
            )

        state, reward, done, _ = env.step(action)

    return {"status": "success"}

if __name__ == "__main__":
    print(run())