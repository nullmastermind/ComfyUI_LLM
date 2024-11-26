from .inputs.input_text import InputText
from .inputs.openai_model_node import OpenAIModelNode
from .outputs.output_text import OutputText

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "OpenAI Model": OpenAIModelNode,
    "Output Text": OutputText,
    "Input Text": InputText,
}

__all__ = ["NODE_CLASS_MAPPINGS"]
