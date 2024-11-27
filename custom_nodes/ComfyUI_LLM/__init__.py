from .converts.any_to_string import AnyToString
from .inputs.input_text import InputText
from .inputs.openai_model_node import OpenAIModelNode
from .open_ai import OpenAINode
from .outputs.output_text import OutputText
from .prompts.prompt_builder import PromptBuilder
from .routers.dynamic_node import DynamicNode
from .routers.question_classifier import QuestionClassifier
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
    "Question Classifier": QuestionClassifier,
    # "Dynamic IMAGE Node": DynamicNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # "Dynamic IMAGE Node": "Dynamic Node",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
