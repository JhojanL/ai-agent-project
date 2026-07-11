import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ],
        max_tokens=50,
    )

    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    # User prompt
    print("User prompt:", args.user_prompt)
    print("Prompt tokens:", response.usage.prompt_tokens)
    print("Response tokens:", response.usage.completion_tokens)
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
