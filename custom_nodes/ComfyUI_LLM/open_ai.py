from openai import OpenAI

from custom_nodes.ComfyUI_LLM.data import RouteData, get_node_id


class OpenAINode:
    CATEGORY = "LLM"
    RETURN_TYPES = (
        "ROUTE_DATA",
        "STRING",
    )
    RETURN_NAMES = (
        ">",
        "answer",
    )
    FUNCTION = "execute"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "route_data_json": ("ROUTE_DATA", {"requireInput": True}),
                "node_id": ("STRING", {"default": ""}),
                "model_config": ("LLM_OPENAI_MODEL",),
                "system_prompt": (
                    "STRING",
                    {"multiline": True, "default": "You are a helpful assistant."},
                ),
                "query": (
                    "STRING",
                    {"multiline": True, "defaultInput": True},
                ),
                "stream": ("BOOLEAN", {"default": False}),
            },
        }

    def execute(
        self,
        route_data_json,
        node_id,
        model_config,
        query,
        system_prompt,
        stream,
    ):
        route_data = RouteData.from_json(route_data_json)
        node_id = get_node_id(node_id)

        if route_data.stop:
            return (
                route_data.to_json(),
                "",
            )

        # Initialize OpenAI client with provided configuration
        client = OpenAI(
            api_key=model_config["api_key"], base_url=model_config["base_url"]
        )

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model=model_config["model"],
                temperature=model_config["temperature"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
                # stream=stream,
            )

            assistant_message = response.choices[0].message.content

            route_data.variables[node_id] = {
                "answer": assistant_message,
            }

            return (
                route_data.to_json(),
                assistant_message,
            )

        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")

            route_data.stop = True
            route_data.variables[node_id] = {
                "answer": "Error: " + str(e),
            }

            return (
                route_data.to_json(),
                "Error: " + str(e),
            )
