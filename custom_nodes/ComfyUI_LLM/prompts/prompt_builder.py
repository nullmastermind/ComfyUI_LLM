from jinja2 import Template

from custom_nodes.ComfyUI_LLM.constant import IN_ICON
from custom_nodes.ComfyUI_LLM.route_data import RouteData, is_stopped, get_node_id


class PromptBuilder:
    CATEGORY = "LLM/prompts"
    RETURN_TYPES = ("ROUTE_DATA", "STRING")
    RETURN_NAMES = ("_out", "prompt")
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                IN_ICON: ("ROUTE_DATA", {"requireInput": True}),
                "node_id": ("STRING", {"default": ""}),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    def execute(self, **kwargs):
        _in = kwargs[IN_ICON]
        node_id = kwargs["node_id"]
        prompt = kwargs["prompt"]

        route_data = RouteData.from_json(_in)
        node_id = get_node_id(node_id)
        route_data.prev_node_type = self.__class__.__name__
        route_data.prev_node_id = node_id

        if is_stopped(route_data):
            return (
                route_data.to_json(),
                "",
            )

        prompt_template = Template(prompt)
        prompt = prompt_template.render(**route_data.variables)

        route_data.variables[node_id] = {"prompt": prompt}

        return (
            route_data.to_json(),
            prompt,
        )
