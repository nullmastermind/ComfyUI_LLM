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
                "prompt": ("STRING", {"multiline": True}),
            },
        }

    def execute(self, model_config, prompt):
        # Initialize OpenAI client with provided configuration
        client = OpenAI(
            api_key=model_config["api_key"], base_url=model_config["base_url"]
        )

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model=model_config["model"],
                temperature=model_config["temperature"],
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract assistant's message
            assistant_message = response.choices[0].message.content
            return (assistant_message,)

        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return ("Error: " + str(e),)
