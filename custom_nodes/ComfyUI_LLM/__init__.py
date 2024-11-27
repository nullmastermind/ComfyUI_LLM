from .converts.any_to_string import AnyToString
from .inputs.input_text import InputText
from .inputs.openai_model_node import OpenAIModelNode
from .open_ai import OpenAINode
from .outputs.output_text import OutputText
from .prompts.prompt_builder import PromptBuilder
from .start import StartNode

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "OpenAI Model": OpenAIModelNode,
    "Output Text": OutputText,
    "Input Text": InputText,
    "Any To Text": AnyToString,
    "Start": StartNode,
    "OpenAI": OpenAINode,
    "Prompt Builder": PromptBuilder,
}

__all__ = ["NODE_CLASS_MAPPINGS"]
