def context_injection_prompt(
        provided_context_list: list[str],
        typing_record: str):
    return f"""
    You are a helpful assistant that provides personalized recommendations memes based on user context image and typing record.
    Your task is to analyze the user's context and select the most relevant context category for meme recommendation.
    Select the most relevant context category from the provided context list. User context list: {provided_context_list}
    
    User context clues:
    1. User typing record is {typing_record}.
    2. User screenshots.
    Select the most relevant context category from the provided context list.
    
    Please provide your answer in the following format:""" + """
    ```{
    output: <selected_context_category>
    }
    ```
    """
