import gradio as gr
from inference import decide_action

def test_agent(vulns, risk):
    state = {"vulns": vulns, "risk": risk}
    action = decide_action(state)
    return action

demo = gr.Interface(
    fn=test_agent,
    inputs=[gr.Slider(0, 10, label="Vulns"), gr.Slider(0, 1, label="Risk")],
    outputs="text",
    title="Cybersec Agent"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
