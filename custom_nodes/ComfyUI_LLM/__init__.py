from .converts.any_to_string import AnyToString
from .inputs.input_text import InputText
from .inputs.openai_model_node import OpenAIModelNode
from .open_ai import OpenAINode
from .outputs.output_text import OutputText
from .prompts.prompt_builder import PromptBuilder
from .routers.question_classifier import QuestionClassifier
from .start import StartNode
from .utils.merge_text_output import MergeTextOutput

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "OpenAI Model": OpenAIModelNode,
    "--dynamic --type=STRING --label=text OutputText": OutputText,
    "Input Text": InputText,
    "Any To Text": AnyToString,
    "Start": StartNode,
    "OpenAI": OpenAINode,
    "Prompt Builder": PromptBuilder,
    "--dynamic --type=STRING --label=text MergeTextOutput": MergeTextOutput,
    "--dynamic --type=STRING --label=question QuestionClassifier": QuestionClassifier,
    # "Dynamic IMAGE Node": DynamicNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # "Dynamic IMAGE Node": "Dynamic Node",
    "--dynamic --type=STRING --label=text OutputText": "Output Text",
    "--dynamic --type=STRING --label=text MergeTextOutput": "Merge Text",
    "--dynamic --type=STRING --label=question QuestionClassifier": "Question Classifier",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
