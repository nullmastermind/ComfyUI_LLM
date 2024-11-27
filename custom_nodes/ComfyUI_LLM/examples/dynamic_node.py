from typing import Any, Dict, Tuple


class DynamicNode:
    """
    A class to represent a dynamic node in ComfyUI.
    """

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "_EXAMPLES"

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, dict]:
        return {"required": {}, "optional": {}}

    def run(self, **kw) -> Tuple[Any | None]:
        # the dynamically created input data will be in the dictionary kwargs
        # for k, v in kw.items():
        #    print(f'{k} => {v}')

        # return the first value found or `None` if no inputs are defined
        value = None
        if len(values := kw.values()) > 0:
            value = next(iter(values))
        return (value,)
