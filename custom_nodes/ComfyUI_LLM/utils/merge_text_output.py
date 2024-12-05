from typing import Any, Dict, Tuple


class MergeTextOutput:
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "LLM/utils"

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, dict]:
        return {
            "required": {
                "text": (
                    "STRING",
                    {
                        "defaultInput": True,
                        "requireInput": True,
                        "dynamic": True,
                    },
                ),
                "delimiter": ("STRING", {"default": "\\n", "multiline": False}),
            },
            "optional": {},
        }

    def run(self, delimiter: str, **kw) -> Tuple[Any | None]:
        delimiter = delimiter.replace("\\n", "\n")
        value = delimiter.join(v for v in kw.values() if v)
        return (value,)
