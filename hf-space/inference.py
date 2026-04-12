#!/usr/bin/env python3
import numpy as np

class CybersecEnv:
    def __init__(self):
        self.state = None
        self.step_count = 0

    def reset(self):
        self.state = {'vulns': 5.0, 'risk': 0.8, 'step': 0}
        self.step_count = 0
        observation = self.state
        info = {}
        return {"observation": observation, "info": info}

    def step(self, action):
        self.step_count += 1
        if self.state is None:
            observation = {"error": "reset first"}
            return {"observation": observation, "reward": 0.0, "terminated": True, "truncated": False, "info": {}}

        vulns = self.state['vulns']
        risk = self.state['risk']
        
        reward = 0.0
        terminated = self.step_count >= 10 or vulns <= 0 or risk >= 1.0
        
        if action == "scan":
            vulns -= 1.0
            reward += 0.2
        elif action == "exploit":
            if risk < 0.3:
                reward += 1.0
            else:
                risk += 0.2
                reward -= 0.5
        elif action == "defend":
            risk -= 0.2
            reward += 0.1
        
        self.state = {'vulns': max(0, vulns), 'risk': min(1.0, max(0, risk)), 'step': self.step_count}
        
        observation = self.state
        info = {"action": action}
        
        return {
            "observation": observation,
            "reward": reward,
            "terminated": terminated,
            "truncated": False,
            "info": info
        }

def decide_action(state):
    vulns = state['vulns']
    risk = state['risk']
    step = state.get('step', 0)
    
    vuln_score = np.array([vulns]) * 0.4
    risk_score = np.array([risk]) * 0.6
    
    if step < 3 or vuln_score > 0.8:
        return "scan"
    elif risk_score < 0.24 and vuln_score > 0:
        return "exploit"
    elif risk_score > 0.36:
        return "defend"
    else:
        return "defend"

if __name__ == '__main__':
    env = CybersecEnv()
    obs, info = env.reset()
    print("Reset OK:", obs['observation'])
    
    for i in range(5):
        action = decide_action(obs['observation'])
        obs, rew, term, trunc, info = env.step(action)
        print(f"Step {i+1}: action={action}, reward={rew}, obs={obs['observation']}")
        if obs['terminated']:
            break
    
    print("OpenEnv root agent ready")
