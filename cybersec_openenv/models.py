"""Models module."""
# Model definitions
class TaskModel:
    pass

def get_model(model_name: str):
    """
    Get model client based on name.
    Stub for OpenAI/HF.
    """
    class DummyModel:
        def __call__(self, *args, **kwargs):
            return {"generated_text": "stub response"}
    # Always return dummy to avoid API key
    return DummyModel()




