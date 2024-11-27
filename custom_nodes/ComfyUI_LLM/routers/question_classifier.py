import json

from openai import OpenAI

from custom_nodes.ComfyUI_LLM.helper.json_in_md_parser import (
    parse_and_check_json_markdown,
)
from custom_nodes.ComfyUI_LLM.helper.memory import get_history_prompt_text
from custom_nodes.ComfyUI_LLM.helper.utils import build_prompt
from custom_nodes.ComfyUI_LLM.route_data import RouteData, get_node_id, is_stopped


class QuestionClassifier:
    MAX_QUESTIONS = 3
    CATEGORY = "LLM/routers"
    RETURN_TYPES = ("ROUTE_DATA", "STRING") + tuple(
        "ROUTE_DATA" for _ in range(MAX_QUESTIONS)
    )
    RETURN_NAMES = ("_out", "class") + tuple(
        f"question_{i+1}" for i in range(MAX_QUESTIONS)
    )
    FUNCTION = "execute"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "_in": ("ROUTE_DATA", {"requireInput": True}),
                "node_id": ("STRING", {"default": ""}),
                "model": ("LLM_OPENAI_MODEL",),
                "query": (
                    "STRING",
                    {"default": "", "multiline": True, "defaultInput": True},
                ),
                "instructions": (
                    "STRING",
                    {"default": "", "multiline": True},
                ),
                "memory": ("BOOLEAN", {"default": True}),
                **{
                    f"question_{i+1}": ("STRING", {"default": "", "multiline": True})
                    for i in range(cls.MAX_QUESTIONS)
                },
            }
        }

    def execute(self, _in, node_id, query, model, instructions, memory, **questions):
        route_data = RouteData.from_json(_in)
        node_id = get_node_id(node_id)
        route_data.prev_node_type = self.__class__.__name__
        route_data.prev_node_id = node_id

        if is_stopped(route_data):
            return (route_data.to_json(),) + tuple(
                route_data.to_json() for _ in range(self.MAX_QUESTIONS)
            )

        classes = []
        for i in range(self.MAX_QUESTIONS):
            if questions[f"question_{i+1}"]:
                classes.append(
                    {
                        "category_id": f"class_{i+1}",
                        "category_name": questions[f"question_{i+1}"],
                    }
                )

        # Call OpenAI API
        client = OpenAI(api_key=model["api_key"], base_url=model["base_url"])
        response = client.chat.completions.create(
            model=model["model"],
            temperature=model["temperature"],
            messages=[
                {
                    "role": "system",
                    "content": build_prompt(
                        template=QUESTION_CLASSIFIER_SYSTEM_PROMPT,
                        variables={
                            "histories": (
                                get_history_prompt_text(route_data.messages)
                                if memory
                                else ""
                            ),
                        },
                    ),
                },
                {
                    "role": "user",
                    "content": QUESTION_CLASSIFIER_USER_PROMPT_1,
                },
                {
                    "role": "assistant",
                    "content": QUESTION_CLASSIFIER_ASSISTANT_PROMPT_1,
                },
                {
                    "role": "user",
                    "content": QUESTION_CLASSIFIER_USER_PROMPT_2,
                },
                {
                    "role": "assistant",
                    "content": QUESTION_CLASSIFIER_ASSISTANT_PROMPT_2,
                },
                {
                    "role": "user",
                    "content": build_prompt(
                        QUESTION_CLASSIFIER_USER_PROMPT_3,
                        variables={
                            "input_text": query,
                            "categories": json.dumps(classes, ensure_ascii=False),
                            "classification_instructions": instructions,
                        },
                    ),
                },
            ],
        )
        result_text = response.choices[0].message.content

        # print(f"result_text: {result_text}")

        category_name = classes[0]["category_name"]
        # category_id = classes[0]["category_id"]

        try:
            result_text_json = parse_and_check_json_markdown(result_text, [])
            if (
                "category_name" in result_text_json
                and "category_id" in result_text_json
            ):
                category_id_result = result_text_json["category_id"]
                classes_map = {
                    class_["category_id"]: class_["category_name"] for class_ in classes
                }
                category_ids = [_class["category_id"] for _class in classes]
                if category_id_result in category_ids:
                    category_name = classes_map[category_id_result]
                    # category_id = category_id_result
        except:
            pass
        finally:
            pass

        # print(f"assistant_message: {category_name} {category_id}")

        # Store questions and model in route_data variables
        route_data.variables[node_id] = {
            "model": model,
            "query": query,
            **{
                f"question_{i+1}": questions[f"question_{i+1}"]
                for i in range(self.MAX_QUESTIONS)
            },
            "class": category_name,
        }

        return (
            route_data.to_json(),
            category_name,
            *(
                (
                    route_data.to_json()
                    if questions[f"question_{i+1}"] == category_name
                    else RouteData(
                        stop=True,
                        conversation_id=route_data.conversation_id,
                        messages=route_data.messages,
                        query=route_data.query,
                        variables=route_data.variables,
                    ).to_json()
                )
                for i in range(self.MAX_QUESTIONS)
            ),
        )


QUESTION_CLASSIFIER_SYSTEM_PROMPT = """
    ### Job Description',
    You are a text classification engine that analyzes text data and assigns categories based on user input or automatically determined categories.
    ### Task
    Your task is to assign one categories ONLY to the input text and only one category may be assigned returned in the output. Additionally, you need to extract the key words from the text that are related to the classification.
    ### Format
    The input text is in the variable input_text. Categories are specified as a category list with two filed category_id and category_name in the variable categories. Classification instructions may be included to improve the classification accuracy.
    ### Constraint
    DO NOT include anything other than the JSON array in your response.
    ### Memory
    Here is the chat histories between human and assistant, inside <histories></histories> XML tags.
    <histories>
    {{histories}}
    </histories>
"""

QUESTION_CLASSIFIER_USER_PROMPT_1 = """
    { "input_text": ["I recently had a great experience with your company. The service was prompt and the staff was very friendly."],
    "categories": [{"category_id":"f5660049-284f-41a7-b301-fd24176a711c","category_name":"Customer Service"},{"category_id":"8d007d06-f2c9-4be5-8ff6-cd4381c13c60","category_name":"Satisfaction"},{"category_id":"5fbbbb18-9843-466d-9b8e-b9bfbb9482c8","category_name":"Sales"},{"category_id":"23623c75-7184-4a2e-8226-466c2e4631e4","category_name":"Product"}],
    "classification_instructions": ["classify the text based on the feedback provided by customer"]}
"""

QUESTION_CLASSIFIER_ASSISTANT_PROMPT_1 = """
```json
    {"keywords": ["recently", "great experience", "company", "service", "prompt", "staff", "friendly"],
    "category_id": "f5660049-284f-41a7-b301-fd24176a711c",
    "category_name": "Customer Service"}
```
"""

QUESTION_CLASSIFIER_USER_PROMPT_2 = """
    {"input_text": ["bad service, slow to bring the food"],
    "categories": [{"category_id":"80fb86a0-4454-4bf5-924c-f253fdd83c02","category_name":"Food Quality"},{"category_id":"f6ff5bc3-aca0-4e4a-8627-e760d0aca78f","category_name":"Experience"},{"category_id":"cc771f63-74e7-4c61-882e-3eda9d8ba5d7","category_name":"Price"}],
    "classification_instructions": []}
"""

QUESTION_CLASSIFIER_ASSISTANT_PROMPT_2 = """
```json
    {"keywords": ["bad service", "slow", "food", "tip", "terrible", "waitresses"],
    "category_id": "f6ff5bc3-aca0-4e4a-8627-e760d0aca78f",
    "category_name": "Experience"}
```
"""

QUESTION_CLASSIFIER_USER_PROMPT_3 = """
    '{"input_text": ["{{input_text}}"],',
    '"categories": {{categories}}, ',
    '"classification_instructions": ["{{classification_instructions}}"]}'
"""
