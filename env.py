from typing import Dict, Any
from pydantic import BaseModel


class Observation(BaseModel):
    text: str
    progress: float


class Action(BaseModel):
    command: str


class Reward(BaseModel):
    value: float


class SimpleEnv:
    def __init__(self):
        self.tasks = [
            {
                "goal": "clean email subject",
                "target": "meeting at 5pm",
                "difficulty": "easy"
            },
            {
                "goal": "extract domain from email",
                "target": "gmail.com",
                "difficulty": "medium"
            },
            {
                "goal": "summarize message",
                "target": "project delayed due to bug",
                "difficulty": "hard"
            }
        ]
        self.current_task = None
        self.state_data = {}

    def reset(self) -> Observation:
        import random

        self.current_task = random.choice(self.tasks)

        self.state_data = {
            "done": False,
            "steps": 0,
            "progress": 0.0
        }

        return Observation(
            text=f"Task: {self.current_task['goal']}",
            progress=0.0
        )

    def step(self, action: Action):
        self.state_data["steps"] += 1

        pred = action.command.lower()
        target = self.current_task["target"]

        score = self._compute_score(pred, target)

        self.state_data["progress"] = score

        done = False

        if score > 0.9 or self.state_data["steps"] >= 5:
            done = True

        self.state_data["done"] = done

        return (
            Observation(
                text=f"Task: {self.current_task['goal']}",
                progress=score
            ),
            Reward(value=score),
            done,
            {}
        )

    def state(self) -> Dict[str, Any]:
        return self.state_data

    def _compute_score(self, pred: str, target: str) -> float:
        if pred == target:
            return 1.0

        overlap = len(set(pred.split()) & set(target.split()))
        total = len(set(target.split()))

        if total == 0:
            return 0.0

        return overlap / total