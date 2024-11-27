from jinja2 import Template


def build_prompt(template: str, variables: dict) -> str:
    prompt_template = Template(template)
    return prompt_template.render(variables)
