# CodeArena: RL Benchmark for Autonomous Code Repair

CodeArena is an OpenEnv-compatible reinforcement learning benchmark for testing the capability of autonomous agents to debug, fix, and optimize broken code.

## Environment Description

The environment tests the agent on 3 difficulties of tasks:
1. **Easy**: Correcting syntax errors.
2. **Medium**: Fixing logical bugs.
3. **Hard**: Algorithm and efficiency optimization.

The agent interacts with the environment by receiving observations of the buggy code and submitting proposed fixes. Execution runs in a sandboxed subprocess.

### Observation Format
`buggy_code` (string): The current state of the source code.
`error_log` (string): Standard error output or runtime exceptions from previous attempts.
`test_results` (string): Count of passed vs total unit tests.
`previous_attempts` (list of strings): Complete history of fixes proposed during the episode.

### Action Format
`proposed_fix` (string): The complete raw Python code to overwrite the buggy file.

### Reward Function
The reward dynamically evaluates partial success bounded universally between 0.0 and 1.0:
- `0.3 * compile_score`: Full points if code compiles successfully.
- `0.4 * test_pass_ratio`: Proportional points based on the number of passed unit tests.
- `0.3 * efficiency_score`: Proportional points based on the execution speed relative to an established optimal algorithmic runtime. (Efficiency is only considered if all tests pass).

## Setup Instructions

### Local Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn server.env:app --reload --port 7860
```

### Docker / Hugging Face Spaces Deployment
The included `Dockerfile` is optimized for a 2 CPU, 8GB RAM footprint.
```bash
docker build -t codearena .
docker run -p 7860:7860 codearena
```

## Example Run

To test the environment natively with OpenAI's API:
```bash
export OPENAI_API_KEY="sk-..."
python inference.py
```

The script will produce structured logging:
```
[START] Initializing CodeArena inference logging
[STEP] Beginning Step 1
[STEP] Action taken. Reward received: 0.700. Task ID: easy-1
[STEP] Beginning Step 2
[STEP] Action taken. Reward received: 1.000. Task ID: easy-1
[END] Inference Complete. Executed 2 step(s).
```
