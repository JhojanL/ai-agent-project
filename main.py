import argparse
import os
import sys
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from call_function import available_functions, call_function
from config import MAX_ITERS
from prompts import system_prompt


def get_llm_client() -> OpenAI:
    """Initializes and returns the OpenAI client configured for OpenRouter."""
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def run_conversation(client: OpenAI, messages: List[Dict[str, Any]], verbose: bool) -> None:
    """
    Handles the core agent loop. Limits executions to MAX_ITERS iterations 
    to prevent runaway execution or infinite loops.
    """
    max_iterations = MAX_ITERS

    for iteration in range(max_iterations):
        if verbose:
            print(f"\n--- Iteration {iteration + 1}/{max_iterations} ---")

        try:
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                temperature=0,  # Ensure reliable, deterministic code/tool choices
                tools=available_functions,
            )
        except OpenAIError as e:
            print(f"API Error occurred: {e}", file=sys.stderr)
            sys.exit(1)

        if not response.usage:
            raise RuntimeError("API response appears to be malformed")

        if verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        assistant_message = response.choices[0].message
        
        # 1. Save the assistant's turn in the chat history
        messages.append(assistant_message)

        # 2. If no tool calls are requested, we have the final response
        if not assistant_message.tool_calls:
            print("\nFinal response:")
            print(assistant_message.content)
            return

        # 3. Process and execute tool calls sequentially
        for tool_call in assistant_message.tool_calls:
            if tool_call.type != "function":
                continue

            if verbose:
                print(f" - Calling function: {tool_call.function.name}")

            # Execute the local implementation
            result_message = call_function(tool_call, verbose=verbose)

            if not result_message.get("content"):
                raise RuntimeError(f"Empty function response returned for {tool_call.function.name}")

            # 4. Save the tool execution response in the chat history
            messages.append(result_message)

            if verbose:
                print(f"-> {result_message['content']}")

    # If the loop finishes without returning, the model exceeded the iteration limit
    print(
        f"\nError: Agent exceeded the maximum execution limit of {max_iterations} iterations without resolving.",
        file=sys.stderr
    )
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    client = get_llm_client()

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    run_conversation(client, messages, args.verbose)


if __name__ == "__main__":
    main()