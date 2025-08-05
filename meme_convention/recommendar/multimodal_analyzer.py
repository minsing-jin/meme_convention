import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# TODO: In the future, we will train multimodal RAG system with this function.
# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Or pass directly: OpenAI(api_key="your-api-key")

def analyze_context_with_gpt(image, prompt_text: dict, model: str = "gpt-4o-mini") -> str:
    contents = [{"type": "text", "text": prompt_text}]
    if image:
        contents.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{image}"
            }
        })

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": contents
            }
        ],
        max_tokens=300,  # Adjust as needed
        response_format={"type": "json_object"}
    )
    context = json.loads(response.choices[0].message.content)['output']

    print(prompt_text)

    return context
