# TODO: define context definition and improve the prompt to know ai better about the context
def create_prompt_based_on_text(
        settings: dict,
        provided_context_list: list[str],
        typing_record: str):
    print(settings)
    return f"""
    You are a helpful assistant that provides personalized recommendations memes based on user context image and typing record.
    Your task is to analyze the user's context and select the most relevant context category for meme recommendation.
    Select the most relevant context category from the provided context list. User context list: {provided_context_list}
    
    User information is following these. Refer this to selected issues.
    1. Age: {settings['user_info']['Age']}
    2. Country: {settings['user_info']['Country']}
    3. Interest: {settings['user_info']['Interest']}
    4. Job: {settings['user_info']['Job']}
    5. Location: {settings['user_info']['Location']}
    
    User context clues:
    1. User typing record is {typing_record}.
    2. User screenshots.
    Select the most relevant context category from the provided context list.
    
    Please response only in json format:""" + """
    ```json
    {
        output: <selected_context_category>
    }
    ```
    """
