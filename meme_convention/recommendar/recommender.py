from meme_convention.recommendar.text_recorder import TypingRecorder
from meme_convention.recommendar.multimodal_analyzer import analyze_context_with_gpt
from meme_convention.recommendar.context_prompt import create_prompt_based_on_text
from meme_convention.recommendar.screenshot import take_screenshot
from meme_convention.frontend.context_dialog import ContextCategoryDialog


#TODO: Add privacy rule because it will occur core privacy issue(screenshot, typing recording).
# TODO: Add local model, locally screenshot
def classify_context_category(context_category_lst: list[str],
                              system_settings: dict,
                              typing_recorder: TypingRecorder = None,
                              model: str = "gpt-4o-mini") -> str:
    """
    Classify the context category based on the provided context category list.
    """
    if not context_category_lst:
        raise ValueError("Context category list is empty.")

    # Collect data
    typing_record = typing_recorder.get_last() if typing_recorder else ""
    screenshot = take_screenshot() if system_settings['allow_screenshot'] else None

    print(f"screen shot 여부: {system_settings['allow_screenshot']}, typing_recorder: {typing_recorder}")
    # Decide classification method
    has_data_for_ai = typing_record or screenshot

    if has_data_for_ai:
        prompt = create_prompt_based_on_text(context_category_lst, typing_record)
        return analyze_context_with_gpt(screenshot, prompt, model)
    else:
        return ContextCategoryDialog.ask(context_category_lst)
