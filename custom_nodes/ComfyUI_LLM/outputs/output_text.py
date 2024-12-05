class OutputText:
    CATEGORY = "LLM/outputs"
    RETURN_TYPES = ("OUTPUT_TEXT",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (
                    "STRING",
                    {
                        "defaultInput": True,
                        "requireInput": True,
                        "default": "",
                        "multiline": True,
                    },
                ),
            },
            "optional": {},
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    def execute(self, unique_id=None, extra_pnginfo=None, **kwargs):
        text_array = kwargs.values()

        # Filter and join valid strings from the array
        text = "\n".join(str(t) for t in text_array if t is not None and str(t).strip())
        text = [text]

        # Early return if no workflow info provided
        if unique_id is None or extra_pnginfo is None:
            return {"ui": {"text": text}, "result": (text,)}

        # Validate extra_pnginfo structure
        if not isinstance(extra_pnginfo, list):
            print("Error: extra_pnginfo must be a list")
            return {"ui": {"text": text}, "result": (text,)}

        # Validate workflow data structure
        workflow_info = extra_pnginfo[0]
        if not isinstance(workflow_info, dict) or "workflow" not in workflow_info:
            print("Error: Invalid workflow data structure")
            return {"ui": {"text": text}, "result": (text,)}

        # Update node widget values if node exists
        workflow = workflow_info["workflow"]
        target_node = None
        for node in workflow["nodes"]:
            if str(node["id"]) == str(unique_id[0]):
                target_node = node
                break

        if target_node:
            target_node["widgets_values"] = [text]

        return {"ui": {"text": text}, "result": (text,)}
