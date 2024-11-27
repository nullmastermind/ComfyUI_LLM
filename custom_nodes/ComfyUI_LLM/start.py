from custom_nodes.ComfyUI_LLM.route_data import RouteData, get_node_id


class StartNode:
    CATEGORY = "LLM"
    RETURN_TYPES = ("ROUTE_DATA", "STRING", "STRING")
    RETURN_NAMES = ("out_", "conversation_id", "query")
    FUNCTION = "execute"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "node_id": ("STRING", {"default": "start"}),
                "conversation_id": ("STRING", {"default": "", "multiline": False}),
                "query": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                    },
                ),
            },
        }

    def execute(self, node_id, conversation_id, query):
        route_data = RouteData(
            stop=False,
            query=query,
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
        )
        node_id = get_node_id(node_id)

        route_data.variables[node_id] = {
            "query": query,
        }
        route_data.prev_node_type = self.__class__.__name__
        route_data.prev_node_id = node_id

        return (
            route_data.to_json(),
            conversation_id,
            query,
        )
