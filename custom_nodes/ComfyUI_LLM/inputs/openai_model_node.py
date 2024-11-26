class OpenAIModelNode:
    CATEGORY = "LLM/Inputs"
    RETURN_TYPES = ("LLM_MODEL",)
    FUNCTION = "execute"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": (
                    "STRING",
                    {"default": "gpt-4o-mini"},
                ),
                "api_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {"default": "https://api.openai.com/v1"},
                ),
                "temperature": (
                    "FLOAT",
                    {"default": 0.0, "min": 0.0, "max": 2.0, "step": 0.1},
                ),
            },
        }

    def execute(self, **kwargs):
        model_config = {
            "model": kwargs["model_name"],
            "api_key": kwargs["api_key"],
            "temperature": kwargs.get("temperature", 0.0),
            "base_url": kwargs.get("base_url", "https://api.openai.com/v1"),
        }
        print("model_config", model_config)
        return (model_config,)
