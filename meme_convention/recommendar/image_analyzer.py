import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Or pass directly: OpenAI(api_key="your-api-key")

def analyze_context_with_gpt(image, prompt_text: dict, model: str = "gpt-4o-mini") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300,  # Adjust as needed
        response_format={"type": "json_object"}
    )
    context = json.loads(response.choices[0].message.content)['output']

    print(prompt_text)

    return context
