"""Environment module."""

class OpenEnv:
    """Cybersec OpenEnv Gym-like environment."""
    
    def __init__(self):
        self.vulns = 0
        self.risk = 0.0
        self.status = "vulnerable"
        self.done = False
        import random
        self.random = random.Random()
    
    def reset(self):
        """Reset environment."""
        self.vulns = self.random.randint(2, 5)
        self.risk = 0.8
        self.status = "vulnerable"
        self.done = False
        obs = {
            "vulns": self.vulns,
            "risk": self.risk,
            "status": self.status
        }
        return obs
    
    def step(self, action):
        """Improved step with penalties, termination."""
        reward = 0.0
        terminated = False
        truncated = False
        action = action.lower().strip()
        
        # Penalty for repeat action
        repeat_penalty = -0.1 if hasattr(self, 'last_action') and self.last_action == action else 0.0
        self.last_action = action
        
        if action == "scan":
            detect_prob = 0.4 + 0.2 * (1 - self.risk)
            if self.random.random() < detect_prob:
                self.vulns = max(0, self.vulns - 1)
            reward = 0.15 + 0.15 * detect_prob + self.random.uniform(-0.05, 0.05) + repeat_penalty
            self.status = "scanning"
        
        elif action == "exploit":
            if self.vulns > 0:
                exploit_reward = 0.7 + 0.2 * (self.vulns / 5.0)
                self.risk = min(1.0, self.risk + 0.12)
                reward = exploit_reward + self.random.uniform(-0.08, 0.08) + repeat_penalty
                self.vulns -= 0.1  # partial
            else:
                self.risk = min(1.0, self.risk + 0.08)
                reward = -0.25 + self.random.uniform(-0.1, 0.05) + repeat_penalty
            self.status = "exploiting"
        
        elif action == "defend":
            risk_reduction = 0.18 * (1 - self.risk / 2.0)  # less effective at low risk
            self.risk = max(0.0, self.risk - risk_reduction)
            reward = 0.45 + 0.25 * risk_reduction + self.random.uniform(-0.05, 0.05) + repeat_penalty
            self.status = "defending"
        
        else:
            reward = -0.15 + repeat_penalty
            self.risk = min(1.0, self.risk + 0.05)
        
        # Bounds
        reward = max(0.0, min(1.0, reward))
        self.risk = max(0.0, min(1.0, self.risk))
        self.vulns = max(0, self.vulns)
        
        # Termination
        if self.risk < 0.2 or self.vulns <= 0:
            terminated = True
            reward = min(1.0, reward + 0.25)  # bonus
        elif self.risk > 0.98:
            terminated = True
            reward = max(0.0, reward - 0.4)  # penalty
        
        obs = {
            "vulns": int(self.vulns),
            "risk": round(self.risk, 2),
            "status": self.status
        }
        info = {"action": action, "repeat_penalty": repeat_penalty, "vulns_left": int(self.vulns)}
        
        self.done = terminated
        
        return obs, reward, terminated, truncated, info
