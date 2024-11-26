import json


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


class AnyToString:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": (AnyType("*"), {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "execute"

    OUTPUT_NODE = True

    CATEGORY = "LLM/Converts"

    def execute(self, **kwargs):
        input_any = kwargs.get("any")

        if input_any is None:
            return ("None",)
        elif isinstance(input_any, dict):
            return (json.dumps(input_any, indent=2),)
        elif isinstance(input_any, list):
            return (json.dumps(input_any, indent=2),)
        elif isinstance(input_any, bool):
            if input_any:
                return ("True",)
            else:
                return ("False",)
        else:
            return (str(input_any),)
