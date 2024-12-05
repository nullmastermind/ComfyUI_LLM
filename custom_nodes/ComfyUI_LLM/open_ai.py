from jinja2 import Template
from openai import OpenAI

from custom_nodes.ComfyUI_LLM.constant import OUT_ICON, IN_ICON
from custom_nodes.ComfyUI_LLM.route_data import RouteData, get_node_id, is_stopped


class OpenAINode:
    CATEGORY = "LLM"
    RETURN_TYPES = (
        "ROUTE_DATA",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (OUT_ICON, "answer", "system_prompt")
    FUNCTION = "execute"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                IN_ICON: ("ROUTE_DATA", {"requireInput": True}),
                "node_id": ("STRING", {"default": "open_ai"}),
                "model": ("LLM_OPENAI_MODEL",),
                "system_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "You are a helpful assistant.",
                        "defaultInput": True,
                    },
                ),
                "query": (
                    "STRING",
                    {"multiline": True, "defaultInput": True},
                ),
                "stream": ("BOOLEAN", {"default": False}),
                "jinja": ("BOOLEAN", {"default": False}),
                "memory": ("BOOLEAN", {"default": True}),
            },
        }

    def execute(self, **kwargs):
        # Extract required parameters from kwargs
        _in = kwargs[IN_ICON]
        node_id = kwargs["node_id"]
        model = kwargs["model"]
        query = kwargs["query"]
        system_prompt = kwargs["system_prompt"]
        jinja = kwargs["jinja"]
        memory = kwargs["memory"]

        route_data = RouteData.from_json(_in)
        node_id = get_node_id(node_id)
        route_data.prev_node_type = self.__class__.__name__
        route_data.prev_node_id = node_id

        if is_stopped(route_data):
            return (
                route_data.to_json(),
                "",
            )

        if jinja:
            system_prompt_template = Template(system_prompt)
            system_prompt = system_prompt_template.render(**route_data.variables)
            query_template = Template(query)
            query = query_template.render(**route_data.variables)

        # Initialize OpenAI client with provided configuration
        client = OpenAI(api_key=model["api_key"], base_url=model["base_url"])

        # update history
        route_data.messages.append({"role": "user", "content": query})

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model=model["model"],
                temperature=model["temperature"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    *(
                        route_data.messages
                        if memory
                        else [{"role": "user", "content": query}]
                    ),
                ],
                # stream=stream,
            )

            assistant_message = response.choices[0].message.content

            route_data.variables[node_id] = {
                "answer": assistant_message,
                "system_prompt": system_prompt,
            }
            route_data.messages.append(
                {"role": "assistant", "content": assistant_message}
            )

            return (
                route_data.to_json(),
                assistant_message,
                system_prompt,
            )

        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")

            route_data.stop = True
            route_data.variables[node_id] = {
                "answer": "Error: " + str(e),
                "system_prompt": system_prompt,
            }

            return (
                route_data.to_json(),
                "Error: " + str(e),
                system_prompt,
            )
