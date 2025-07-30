from meme_convention.recommendar.text_recorder import TypingRecorder
from meme_convention.recommendar.image_analyzer import analyze_context_with_gpt
from meme_convention.recommendar.context_injection_prompt import context_injection_prompt
from meme_convention.recommendar.screenshot import take_screenshot


def classify_context_category(context_category_lst: list[str], typing_recorder: TypingRecorder, model: str="gpt-4o-mini",) -> str:
    """
    Classify the context category based on the provided context category list.

    Args:
        context_category_lst (list[str]): List of context categories to choose from.

    Returns:
        str: The selected context category.
    """
    if not context_category_lst:
        raise ValueError("Context category list is empty.")

    screenshot = take_screenshot()
    typing_record = typing_recorder.get_last()
    prompt = context_injection_prompt(context_category_lst, typing_record)
    selected_context = analyze_context_with_gpt(screenshot, prompt, model)

    return selected_context
