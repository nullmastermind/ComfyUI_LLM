from openai import OpenAI


class OpenAINode:
    CATEGORY = "LLM"
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_config": ("LLM_OPENAI_MODEL",),
                "system_prompt": (
                    "STRING",
                    {"multiline": True, "default": "You are a helpful assistant."},
                ),
                "user_prompt": (
                    "STRING",
                    {"multiline": True, "defaultInput": True, "label_on": True},
                ),
                "stream": ("BOOLEAN", {"default": False}),
            },
        }

    def execute(self, model_config, user_prompt, system_prompt, stream):
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
                    {"role": "user", "content": user_prompt},
                ],
                # stream=stream,
            )

            # if stream:
            #     # Collect streamed responses
            #     full_response = ""
            #     for chunk in response:
            #         if chunk.choices[0].delta.content:
            #             full_response += chunk.choices[0].delta.content
            #     return (full_response,)
            # else:
            #     # Extract assistant's message (non-streaming)
            #     assistant_message = response.choices[0].message.content
            #     return (assistant_message,)

            assistant_message = response.choices[0].message.content
            return (assistant_message,)

        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return ("Error: " + str(e),)
