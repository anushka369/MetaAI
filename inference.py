import os
from openai import OpenAI
from env import SimpleEnv, Action

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

MODEL = os.getenv("MODEL_NAME")

def run():
    env = SimpleEnv()
    obs = env.reset()

    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL,
            messages=
            [
                {
                    "role": "user",
                    "content": obs.text
                }
            ]
        )

        output = response.choices[0].message.content

        obs, reward, done, _ = env.step(
            Action(command=output)
        )

        print(reward.value)

        if done:
            break

if __name__ == "__main__":
    run()