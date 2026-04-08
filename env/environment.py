from env.models import Observation, Reward, Ticket
from env.tasks import TASKS
from env.graders import grade_easy, grade_medium, grade_hard

class SupportEnv:

    def __init__(self):
        self.current_task = None
        self.step_count = 0
        self.trace = []

    def reset(self, task_id: str):
        self.current_task = TASKS[task_id]
        self.step_count = 0
        self.trace = []

        return Observation(
            instruction="You are a support agent. Choose best action.",
            ticket=Ticket(**self.current_task["ticket"]),
            step_count=self.step_count
        )

    def step(self, action_dict):
        self.step_count += 1
        self.trace.append(action_dict)

        reward_score = 0.0

        if self.current_task == TASKS["easy"]:
            reward_score = grade_easy(action_dict)

        elif self.current_task == TASKS["medium"]:
            reward_score = grade_medium(self.trace)

        elif self.current_task == TASKS["hard"]:
            reward_score = grade_hard(self.trace)

        reward = Reward(
            score=max(0.0, min(1.0, reward_score)),
            breakdown={"score": reward_score}
        )

        done = False
        if action_dict.get("action_type") == "close" or self.step_count >= 5:
            done = True

        obs = Observation(
            instruction="Continue resolving the ticket.",
            ticket=Ticket(**self.current_task["ticket"]),
            step_count=self.step_count
        )

        return obs, reward, done, {}

    def state(self):
        return {
            "task": self.current_task,
            "steps": self.step_count,
            "trace": self.trace
        }