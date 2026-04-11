#!/usr/bin/env python3
import numpy as np

def decide_action(state):
    vulns = state['vulns']
    risk = state['risk']
    step = state.get('step', 0)
    
    # Numpy for computation
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
    print("OpenEnv agent with numpy - ready")

