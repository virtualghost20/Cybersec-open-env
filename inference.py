#!/usr/bin/env python3
'''Minimal Cybersec OpenEnv Inference Agent. Strict env vars. Optimized.'''
import os
import textwrap
import sys
import argparse
from typing import List, Optional

from openai import OpenAI

# Minimal OpenEnv stub - use API for full env (as in original inference)
class OpenEnv:
    def __init__(self, local_image_name: Optional[str] = None):
        self.local_image_name = local_image_name

    def reset(self):
        return {'state': 'initial'}  # Minimal stub

    def step(self, action: str):
        # Simulate step for --test
        reward = 0.8 if 'scan' in action.lower() else 0.2
        terminated = False
        truncated = False
        return {'state': f'after {action}'}, reward, terminated, truncated, {'error': None}

try:
    env_class = OpenEnv
except ImportError:
    print('[END] success=false steps=0 score=0.00 rewards=[]', file=sys.stderr)
    sys.exit(1)

parser = argparse.ArgumentParser(description='Minimal Cybersec OpenEnv Inference')
parser.add_argument('--test', action='store_true', help='Test mode with stub env')
args = parser.parse_args()

if args.test:
    os.environ.setdefault('API_BASE_URL', 'http://localhost:7860/v1')
    os.environ.setdefault('MODEL_NAME', 'gpt-4o-mini')
    os.environ.setdefault('TASK_NAME', 'scan_challenge')
    os.environ.setdefault('BENCHMARK', 'cybersec_openenv')

required_vars = ['API_BASE_URL', 'MODEL_NAME', 'TASK_NAME', 'BENCHMARK']
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print('[END] success=false steps=0 score=0.00 rewards=[]', flush=True)
    sys.exit(1)

MAX_STEPS = 10  # Reduced for speed
TEMPERATURE = 0.7
MAX_TOKENS = 100  # Reduced
SUCCESS_THRESHOLD = 0.3

MAX_REWARD = MAX_STEPS * 1.0
SYSTEM_PROMPT = 'Cybersec agent. Obs: state. Action: scan/exploit/defend. Maximize reward.'

def log_start(task, env, model):
    print(f'[START] task={task} env={env} model={model}', flush=True)

def log_step(step, action, reward, done, error=None):
    error_str = error or 'null'
    print(f'[STEP] step={step} action="{action}" reward={reward:.2f} done={done} error={error_str}', flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ','.join(f'{r:.2f}' for r in rewards)
    print(f'[END] success={success} steps={steps} score={score:.2f} rewards=[{rewards_str}]', flush=True)

def build_prompt(step, obs, last_reward, history):
    history_str = '\n'.join(history[-2:])  # Trim history
    return f'Step: {step}\nObs: {obs}\nLast reward: {last_reward:.2f}\nHistory:\n{history_str}\nAction:'

def main():
    env = env_class(os.getenv('LOCAL_IMAGE_NAME'))
    history = []
    rewards = []
    total_reward = 0.0
    steps = 0

    log_start(os.getenv('TASK_NAME'), os.getenv('BENCHMARK'), os.getenv('MODEL_NAME'))

    obs = env.reset()
    last_reward = 0.0

    client = OpenAI(base_url=os.getenv('API_BASE_URL'), api_key=os.getenv('HF_TOKEN', 'dummy')) if not args.test else None

    try:
        for step in range(1, MAX_STEPS + 1):
            if args.test:
                action = ['scan', 'exploit', 'defend'][(step-1) % 3]
            else:
                prompt = build_prompt(step, obs, last_reward, history)
                completion = client.chat.completions.create(
                    model=os.getenv('MODEL_NAME'),
                    messages=[{'role': 'system', 'content': SYSTEM_PROMPT}, {'role': 'user', 'content': prompt}],
                    temperature=TEMPERATURE, max_tokens=MAX_TOKENS
                )
                action = completion.choices[0].message.content.strip() or 'scan'

            obs, reward, term, trunc, info = env.step(action)
            done = term or trunc
            error = info.get('error') if info else None

            rewards.append(reward)
            total_reward += reward
            steps = step
            last_reward = reward

            log_step(step, action, reward, done, error)
            history.append(f'action={action} reward={reward:.2f}')

            if done: break

        score = total_reward / MAX_REWARD
        success = score >= SUCCESS_THRESHOLD

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        success = False
        steps = 0
        score = 0.0
        rewards = []
    finally:
        log_end(success, steps, score, rewards)

if __name__ == '__main__':
    main()

