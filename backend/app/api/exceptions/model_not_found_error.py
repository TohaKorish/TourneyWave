class ModelNotFoundError(Exception):
    def __init__(self, model_name: str):
        super().__init__(f"Model {model_name} not found")
