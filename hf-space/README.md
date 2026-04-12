# Cybersec OpenEnv HF Space

Interactive cybersecurity environment demo for agent benchmarking.

[![Space](https://img.shields.io/badge/%F0%9F%A4%97%20HF%20Space-ghostspy/Cybersec--openenv-blue)](https://huggingface.co/spaces/ghostspy/Cybersec-openenv)

**Features:**
- Gradio UI for reset/step/policy demo
- Stochastic OpenEnv with vulns/risk/status
- Docker-ready for HF Spaces

**Local Run:**
```
docker build -t cybersec-openenv .
docker run -p 7860:7860 cybersec-openenv
```

Open http://localhost:7860

Phase 1 OpenEnv compatible.

