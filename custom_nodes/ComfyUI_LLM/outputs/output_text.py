class OutputText:
    CATEGORY = "LLM/outputs"
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "", "forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    def execute(self, text, unique_id=None, extra_pnginfo=None):
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
