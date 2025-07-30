import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Or pass directly: OpenAI(api_key="your-api-key")


def analyze_context_with_gpt(image, model: str, prompt_text: dict):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text['user']},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300  # Adjust as needed
    )
    return response.choices[0].message.content
