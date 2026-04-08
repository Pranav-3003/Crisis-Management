import os
from env import CrisisEnv
from models import Action
from openai import OpenAI

# ✅ Use their injected API
client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url=os.environ["API_BASE_URL"]
)

def get_action_from_llm(state):
    prompt = f"""
    You are a crisis manager AI.

    Current state:
    {state}

    Decide next action in JSON:
    {{
        "action_type": "dispatch",
        "resource": "ambulance",
        "target": "Zone A"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    # simple parse (safe fallback)
    try:
        import json
        action_dict = json.loads(content)
    except:
        action_dict = {
            "action_type": "dispatch",
            "resource": "ambulance",
            "target": "Zone A"
        }

    return Action(**action_dict)


def run_task(task_name):
    env = CrisisEnv()
    state = env.reset()

    print(f"[START] task={task_name}", flush=True)

    total_reward = 0
    step_count = 0
    done = False

    while not done:
        action = get_action_from_llm(state)  # ✅ LLM CALL

        state, reward, done, _ = env.step(action)

        step_count += 1
        total_reward += reward

        print(f"[STEP] step={step_count} reward={float(reward)}", flush=True)

    score = total_reward / 100

    print(f"[END] task={task_name} score={float(score)} steps={step_count}", flush=True)


if __name__ == "__main__":
    run_task("easy")
    run_task("medium")
    run_task("hard")