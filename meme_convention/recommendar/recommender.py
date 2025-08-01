from meme_convention.recommendar.text_recorder import TypingRecorder
from meme_convention.recommendar.multimodal_analyzer import analyze_context_with_gpt
from meme_convention.recommendar.context_prompt import create_prompt_based_on_text
from meme_convention.recommendar.screenshot import take_screenshot
from meme_convention.frontend.context_dialog import ContextCategoryDialog


def classify_context_category(context_category_lst: list[str],
                              allow_screenshot: bool,
                              typing_recorder: TypingRecorder = None,
                              model: str = "gpt-4o-mini") -> str:
    """
    Classify the context category based on the provided context category list.
    """
    if not context_category_lst:
        raise ValueError("Context category list is empty.")

    # Collect data
    typing_record = typing_recorder.get_last() if typing_recorder else ""
    screenshot = take_screenshot() if allow_screenshot else None

    # Decide classification method
    has_data_for_ai = typing_record or screenshot

    if has_data_for_ai:
        prompt = create_prompt_based_on_text(context_category_lst, typing_record)
        return analyze_context_with_gpt(screenshot, prompt, model)
    else:
        return ContextCategoryDialog.ask(context_category_lst)
