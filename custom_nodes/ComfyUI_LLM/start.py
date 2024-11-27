import uuid


class StartNode:
    CATEGORY = "LLM"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Conversation ID", "Message")
    FUNCTION = "execute"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conversation_id": ("STRING", {"default": "", "multiline": False}),
                "message": (
                    "STRING",
                    {"default": "", "multiline": True},
                ),
            },
        }

    def execute(self, conversation_id, message):
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        return (
            conversation_id,
            message,
        )
