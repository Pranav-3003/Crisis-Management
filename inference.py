from env import CrisisEnv
from models import Action

def run_task(task_name):
    env = CrisisEnv()
    state = env.reset()

    print(f"[START] task={task_name}", flush=True)

    total_reward = 0
    step_count = 0
    done = False

    while not done:
        action = Action(
            action_type="dispatch",
            resource="ambulance",
            target="Zone A"
        )

        state, reward, done, _ = env.step(action)

        step_count += 1
        total_reward += reward

        print(f"[STEP] step={step_count} reward={float(reward)}", flush=True)

    score = total_reward / 100  # normalize

    print(f"[END] task={task_name} score={float(score)} steps={step_count}", flush=True)


if __name__ == "__main__":
    run_task("easy")
    run_task("medium")
    run_task("hard")