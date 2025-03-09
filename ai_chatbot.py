import os
from api import client


def chat_with_claude(
    max_history=10,
    max_tokens=500,
    model="claude-3-haiku-20240307",
    system_prompt=None,
    stream=True,
):
    """
    Run an interactive chat with Claude.

    Args:
        max_history (int): Maximum number of messages to keep in history
        max_tokens (int): Maximum tokens in Claude's response
        model (str): Claude model to use
        system_prompt (str): Optional system prompt
        stream (bool): Whether to stream the response
    """
    conversation_history = []

    print(f"Chat with Claude (Type 'quit' to exit)")
    print("-" * 50)

    while True:
        user_input = input("User: ")

        if user_input.lower() == "quit":
            print("Conversation ended.")
            break

        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})

        # Trim conversation history if it gets too long
        if len(conversation_history) > max_history:
            # Keep only the most recent messages
            conversation_history = conversation_history[-max_history:]

        try:
            # Build request parameters
            request_params = {
                "model": model,
                "messages": conversation_history,
                "max_tokens": max_tokens,
            }

            # Add system prompt if provided
            if system_prompt:
                request_params["system"] = system_prompt

            # Make the API call
            if stream:
                # Handle streaming response
                print("Assistant: ", end="", flush=True)
                full_response = ""

                # For streaming, we don't pass the stream parameter to the stream() method
                with client.messages.stream(**request_params) as stream_response:
                    for chunk in stream_response:
                        if chunk.type == "content_block_delta":
                            if chunk.delta.text:
                                print(chunk.delta.text, end="", flush=True)
                                full_response += chunk.delta.text

                print()  # Add newline after streaming completes
                assistant_response = full_response
            else:
                # For non-streaming, we need to set stream=False
                request_params["stream"] = False
                response = client.messages.create(**request_params)
                assistant_response = response.content[0].text
                print(f"Assistant: {assistant_response}")

            # Add assistant response to history
            conversation_history.append(
                {"role": "assistant", "content": assistant_response}
            )

        except Exception as e:
            print(f"Error: {e}")
            if "credit balance is too low" in str(e):
                print(
                    "You've run out of credits. Please add more credits to your account."
                )
                break


# Example usage
if __name__ == "__main__":
    # Basic usage with default parameters
    # chat_with_claude()

    # Advanced usage with customized parameters
    chat_with_claude(
        max_history=6,
        max_tokens=300,
        model="claude-3-haiku-20240307",
        # system_prompt="Please provide response as Kwame Nkrumah."
    )
