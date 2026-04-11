def decide_action(state):
    if state['vulns'] > 2:
        return "patch"
    elif state['risk'] > 0.7:
        return "defend"
    else:
        return "scan"
