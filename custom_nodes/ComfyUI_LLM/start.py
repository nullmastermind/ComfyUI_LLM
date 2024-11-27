from custom_nodes.ComfyUI_LLM.data import RouteData


class StartNode:
    CATEGORY = "LLM"
    RETURN_TYPES = ("ROUTE_DATA", "STRING", "STRING")
    RETURN_NAMES = (">", "Conversation ID", "Message")
    FUNCTION = "execute"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conversation_id": ("STRING", {"default": "", "multiline": False}),
                "message": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                    },
                ),
            },
        }

    def execute(self, conversation_id, message):
        route_data = RouteData(
            stop=False,
            query=message,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )

        return (
            route_data.to_json(),
            conversation_id,
            message,
        )
