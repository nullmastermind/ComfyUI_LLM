class ModelNode:
    CATEGORY = "llm/model"
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "execute"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "number": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
                "choice": (["option1", "option2"], {"default": "option1"}),
                "model": ("MODEL",),
            },
            "optional": {"optional_param": ("FLOAT", {"default": 1.0})},
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    def execute(self, **kwargs):
        print(kwargs)
        return ("",)
