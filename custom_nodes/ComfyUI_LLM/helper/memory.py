from typing import List


def get_history_prompt_text(
    prompt_messages: List[dict],
    human_prefix: str = "Human",
    ai_prefix: str = "Assistant",
) -> str:
    string_messages = []
    for m in prompt_messages:
        if m["role"] == "user":
            role = human_prefix
        elif m["role"] == "assistant":
            role = ai_prefix
        else:
            continue

        message = f"{role}: {m['content']}"
        string_messages.append(message)

    return "\n".join(string_messages)
