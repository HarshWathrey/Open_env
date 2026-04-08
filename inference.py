import os
import json
from openai import OpenAI
from env.environment import SupportEnv

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

env = SupportEnv()
TASKS = ["easy", "medium", "hard"]

def run_task(task_id):
    obs = env.reset(task_id)
    done = False
    total_reward = 0.0
    step_id = 0

    print(f"[START] task={task_id}")

    while not done:
        step_id += 1

        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            messages=[
                {"role": "system", "content": obs.instruction},
                {"role": "user", "content": json.dumps(obs.dict())}
            ]
        )

        try:
            action = json.loads(response.choices[0].message.content)
        except:
            action = {"action_type": "respond", "message": "fallback"}

        obs, reward, done, _ = env.step(action)
        total_reward += reward.score

        print(f"[STEP] task={task_id} step={step_id} reward={reward.score}")

    print(f"[END] task={task_id} total_reward={round(total_reward,3)}")


if __name__ == "__main__":
    for t in TASKS:
        run_task(t)