class CybersecAgent:
    def __init__(self):
        self.last_action = None
        self.vuln_history = []
        self.risk_trend = 0.0
        self.scan_count = 0
        self.high_vuln_seen = False
        self.safe_exploit_count = 0

def decide_action(state):
    """
    High-performance adaptive policy for Cybersec OpenEnv.
    """
    vulns = state['vulns']
    risk = state['risk']
    status = state['status']
    step = state.get('step', 0)

    agent = CybersecAgent()  # Singleton-like, but stateless across calls (light memory via class if extended)

    # Early termination check - finish if secure
    if risk < 0.25 and vulns == 0:
        return "defend"  # Bonus reward

    # Dynamic thresholds
    safe_risk = 0.35 + 0.1 * step / 20  # Increase tolerance as steps progress
    low_vuln = vulns <= 1
    high_risk = risk > 0.75
    vuln_drop = len(agent.vuln_history) > 2 and vulns < agent.vuln_history[-2]

    # Repeat penalty avoidance
    repeat_penalty = agent.last_action == "scan" and agent.scan_count > 2

    # Multi-layered logic with expected value
    # EV scan: high if vulns high, risk low; low if scanned recently
    ev_scan = (vulns * 0.3) * (1 - risk) * 0.6 if not repeat_penalty else 0.1

    # EV exploit: high if vulns >0 and risk low; risk penalty
    ev_exploit = (vulns * 0.7) * max(0, 1 - risk * 1.5) if vulns > 0 else -0.3

    # EV defend: high if risk high; scales with risk
    ev_defend = risk * 0.8 + (0.2 if agent.high_vuln_seen else 0)

    # Update memory
    agent.vuln_history.append(vulns)
    if len(agent.vuln_history) > 5:
        agent.vuln_history.pop(0)
    agent.risk_trend = risk - agent.vuln_history[0] if len(agent.vuln_history) > 1 else 0
    agent.high_vuln_seen = agent.high_vuln_seen or vulns > 3
    if agent.last_action == "scan":
        agent.scan_count += 1
    else:
        agent.scan_count = 0

    # Decision tree
    if high_risk:
        return "defend"  # Priority 1: Risk mitigation
    elif low_vuln and risk < safe_risk:
        return "exploit"  # Safe exploit
    elif ev_scan > max(ev_exploit, ev_defend) and vulns > 1:
        return "scan"  # Discover vulns
    elif risk > 0.5 or agent.risk_trend > 0:
        return "defend"  # Maintain safety
    elif ev_exploit > ev_defend:
        return "exploit"  # Balanced exploit
    else:
        return "defend"  # Default: secure

    agent.last_action = action
    return action

