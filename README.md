# Cybersec OpenEnv 🔒

## Overview
Cybersecurity Open Environment for AI agents. Flat structure per spec.

## Structure
```
.
├── Dockerfile           # Docker build for deployment (port 7860)
├── inference.py         # LLM agent (OpenAI/HF, --test stub)
├── requirements.txt     # Minimal deps
├── openenv/config.yaml  # OpenEnv config (benchmarks/tasks)
├── cybersec_openenv/    # Core package (env, graders, server)
├── hf-space/            # HF Spaces deploy
└── (legacy dirs)
```

## Quick Start
```bash
pip install -r requirements.txt
python inference.py --test   # Stub test: success=true
docker build -t openenv .    # Build
docker run -p 7860:7860 openenv python inference.py  # Run
```

## Features
- OpenEnv Gym env for cybersec tasks
- Flask/Gradio API (/reset, /step)
- Optimized inference (10 steps, low tokens)
- HF Spaces ready

## Test Output Example
```
[START] task=scan_challenge env=cybersec_openenv model=gpt-4o-mini
[STEP] step=1 action="scan" reward=0.80 ...
[END] success=true steps=10 score=0.44 rewards=[0.80,0.20,...]
```

## Deploy
- GitHub: https://github.com/virtualghost20/Cybersec-open-env (branch blackboxai/restructure)
- HF: https://huggingface.co/spaces/ghostspy/Cybersec-openenv

## License
MIT
