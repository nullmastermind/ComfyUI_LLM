from typing import Any, Dict, Tuple


class MergeTextOutput:
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = "LLM/utils"

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, dict]:
        return {"required": {}, "optional": {}}

    def run(self, **kw) -> Tuple[Any | None]:
        value = "\n".join(v for v in kw.values() if v)

        return (value,)
