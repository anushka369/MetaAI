# 📦 Simple Text Processing OpenEnv Environment

## 📌 Overview

This project implements a **real-world OpenEnv environment** simulating common text-processing workflows such as:

* Cleaning noisy email subjects
* Extracting domains from email addresses
* Summarizing short messages

The environment is designed to evaluate **LLM-based agents** using the standard OpenEnv API (`reset()`, `step()`, `state()`), with **progressive task difficulty** and **deterministic grading**.

---

## 🎯 Motivation

Text processing is a core task in real-world systems like:

* Email triage pipelines
* Customer support automation
* Data preprocessing systems

This environment provides a **controlled benchmark** for evaluating how well agents can:

* Interpret instructions
* Generate structured outputs
* Improve over multi-step interactions

---

## ⚙️ Environment Design

### API Interface

The environment follows the OpenEnv specification:

* `reset()` → Initializes a new task and returns initial observation
* `step(action)` → Executes agent action and returns:

  * observation
  * reward
  * done
  * info
* `state()` → Returns current internal state

---

## 🧠 Observation Space

```json
{
  "text": "Task description",
  "progress": "float (0.0 to 1.0)"
}
```

* `text`: Task instruction
* `progress`: Current completion score

---

## 🎮 Action Space

```json
{
  "command": "string"
}
```

* Free-form natural language output from the agent
* Represents the agent’s attempt to solve the task

---

## 🏆 Reward Function

The reward is **continuous (0.0 → 1.0)** and reflects partial correctness.

### Strategy:

* Exact match → `1.0`
* Partial overlap → proportional score
* Incorrect output → low score

This ensures:

* Dense feedback across steps
* No sparse/binary-only rewards
* Encourages incremental improvement

---

## 📋 Tasks

The environment includes **3 tasks with increasing difficulty**:

### 🟢 Easy — Text Cleaning

* **Goal:** Clean an email subject
* **Target:** `"meeting at 5pm"`
* **Grader:** Exact match

---

### 🟡 Medium — Domain Extraction

* **Goal:** Extract domain from email
* **Target:** `"gmail.com"`
* **Grader:** Substring match

---

### 🔴 Hard — Message Summarization

* **Goal:** Summarize message meaning
* **Target:** `"project delayed due to bug"`
* **Grader:** Keyword overlap scoring

---

## 🧪 Grading Logic

Each task has a **deterministic grader**:

* Returns scores in `[0.0, 1.0]`
* Reproducible across runs
* Differentiates partial vs full correctness

No random scoring or constant outputs.

---

## 🔁 Episode Termination

An episode ends when:

* Score ≥ `0.9` (task effectively solved), OR
* Max steps (`5`) reached

---

## 🤖 Baseline Inference

The project includes a baseline script:

```
inference.py
```

### Requirements:

Set environment variables:

```bash
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="your-model-name"
export HF_TOKEN="your-hf-token"
```

### Run:

```bash
python inference.py
```

The script:

* Interacts with the environment
* Uses OpenAI client
* Produces reproducible scores

---

## 📊 Baseline Performance

| Task   | Score Range |
| ------ | ----------- |
| Easy   | 0.8 – 1.0   |
| Medium | 0.6 – 1.0   |
| Hard   | 0.3 – 0.9   |

---

## ⚠️ Limitations

* Task complexity is relatively simple
* Reward function uses basic token overlap
* No multi-step reasoning dependency yet

---

## 🔮 Future Improvements

* Add multi-turn workflows
* Introduce noisy real-world datasets
* Improve semantic scoring (embedding-based)
* Add adversarial edge cases

---

## 📁 Project Structure

```
.
├── env.py
├── tasks.py
├── inference.py
├── openenv.yaml
├── Dockerfile
└── README.md
```
