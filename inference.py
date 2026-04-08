import os
import json
from env import CrisisEnv
from models import Action
from openai import OpenAI

# ✅ Use provided API (DO NOT CHANGE)
client = OpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url=os.environ.get("API_BASE_URL")
)


def get_action_from_llm(state):
    try:
        prompt = f"""
        You are a crisis manager AI.

        Current state:
        {state}

        Respond ONLY with valid JSON (no explanation):
        {{
            "action_type": "dispatch",
            "resource": "ambulance",
            "target": "Zone A"
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        # ✅ Validate response
        if not response or not response.choices:
            raise ValueError("Empty response")

        content = response.choices[0].message.content

        if not content:
            raise ValueError("No content returned")

        content = content.strip()

        if not content.startswith("{"):
            start = content.find("{")
            end = content.rfind("}")
            if start == -1 or end == -1:
                raise ValueError("No JSON found")
            content = content[start:end + 1]

        action_dict = json.loads(content)

        if not all(k in action_dict for k in ["action_type", "resource", "target"]):
            raise ValueError("Invalid keys")

        return Action(**action_dict)

    except Exception:
        return Action(
            action_type="dispatch",
            resource="ambulance",
            target="Zone A"
        )


def run_task(task_name):
    env = CrisisEnv()
    state = env.reset()

    print(f"[START] task={task_name}", flush=True)

    total_reward = 0.0
    step_count = 0
    done = False

    while not done:
        try:
            action = get_action_from_llm(state)
        except Exception:
            action = Action(
                action_type="dispatch",
                resource="ambulance",
                target="Zone A"
            )

        state, reward, done, _ = env.step(action)

        step_count += 1
        total_reward += float(reward)

        print(f"[STEP] step={step_count} reward={float(reward)}", flush=True)

    # Normalize score
    score = total_reward / 100.0

    print(f"[END] task={task_name} score={float(score)} steps={step_count}", flush=True)


if __name__ == "__main__":
    try:
        run_task("easy")
        run_task("medium")
        run_task("hard")
    except Exception:
        print("[START] task=error", flush=True)
        print("[STEP] step=1 reward=0.0", flush=True)
        print("[END] task=error score=0.0 steps=1", flush=True)