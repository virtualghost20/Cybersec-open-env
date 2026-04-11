import gradio as gr
import sys
sys.path.insert(0, 'cybersec_openenv')

try:
    from cybersec_openenv.env import OpenEnv
except ImportError:
    print("Using stub OpenEnv")
    class OpenEnv:
        def __init__(self):
            pass
        def reset(self):
            return {"vulns": 3, "risk": 0.8, "status": "vulnerable"}
        def step(self, action):
            reward = 0.3 if action == "scan" else 0.1
            obs = {"vulns": 2, "risk": 0.7, "status": "scanning"}
            return obs, reward, False, False, {}

def run_submission(model_name, task_name):
    try:
        env = OpenEnv()
        log = f"Task: {task_name} | Model: {model_name}\n"
        log += "Cybersec OpenEnv Demo (Stub Mode)\n\n"
        obs = env.reset()
        log += f"Obs: {obs}\n"
        
        for step in range(1, 6):
            action = "scan"
            obs, reward, _, _, info = env.step(action)
            log += f"Step {step}: {action} | reward={reward:.2f} | obs={obs}\n"
        
        return log
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks(title="Cybersec OpenEnv") as demo:
    gr.Markdown("# Cybersec OpenEnv Demo")
    gr.Markdown("Interactive cybersecurity env simulation.")
    with gr.Row():
        model_input = gr.Textbox(value="gpt-4o-mini", label="Model")
        task_input = gr.Textbox(value="scan_challenge", label="Task")
    output = gr.Textbox(label="Log", lines=20)
    submit = gr.Button("Run")
    submit.click(run_submission, inputs=[model_input, task_input], outputs=output)

if __name__ == '__main__':
    demo.launch(server_name="0.0.0.0", server_port=7860)
