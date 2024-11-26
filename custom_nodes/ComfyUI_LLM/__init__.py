from .OpenAI import OpenAINode
from .converts.any_to_string import AnyToString
from .inputs.input_text import InputText
from .inputs.openai_model_node import OpenAIModelNode
from .outputs.output_text import OutputText

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "OpenAI Model": OpenAIModelNode,
    "Output Text": OutputText,
    "Input Text": InputText,
    "Any To Text": AnyToString,
    "OpenAI": OpenAINode,
}

__all__ = ["NODE_CLASS_MAPPINGS"]
