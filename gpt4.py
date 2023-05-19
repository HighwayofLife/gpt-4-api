import openai
import os
import argparse

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4"
MAX_TOKENS = 4500
TEMPERATURE = 1
STREAM = False


def handle_args(args):
    if os.environ.get("OPENAI_MODEL"):
        set_model_config_model(os.environ.get("OPENAI_MODEL"))

    if args.model:
        set_model_config_model(args.model)

    if os.environ.get("OPENAI_MAX_TOKENS"):
        set_model_config_max_tokens(os.environ.get("OPENAI_MAX_TOKENS"))

    if args.max_tokens:
        set_model_config_max_tokens(args.max_tokens)

    if os.environ.get("OPENAI_TEMPERATURE"):
        set_model_config_temperature(os.environ.get("OPENAI_TEMPERATURE"))

    if args.temperature:
        set_model_config_temperature(args.temperature)

    if os.environ.get("OPENAI_STREAM"):
        set_model_config_stream(os.environ.get("OPENAI_STREAM"))

    if args.stream:
        set_model_config_stream(args.stream)


def set_model_config_model(model):
    global MODEL
    MODEL = model


def set_model_config_max_tokens(max_tokens):
    global MAX_TOKENS
    MAX_TOKENS = max_tokens


def set_model_config_temperature(temperature):
    global TEMPERATURE
    TEMPERATURE = temperature


def set_model_config_stream(stream):
    global STREAM
    STREAM = stream


def call_gpt_4(input_text):
    messages = [
        {
            "role": "user",
            "content": input_text,
        }
    ]

    try:
        # Make the API call
        response = openai.ChatCompletion.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=messages,
            stream=STREAM,
        )
        return response
    except openai.error.InvalidRequestError as e:
        print(f"Invalid request: {e}")
    except openai.error.AuthenticationError as e:
        print(f"Authentication error: {e}")
    except openai.error.APIConnectionError as e:
        print(f"Network error: {e}")
    except openai.error.OpenAIError as e:
        print(f"Unknown error: {e}")
    except Exception as e:
        print(f"Unknown error: {e}")

def print_response(input_text):
    response = call_gpt_4(input_text)
    print("-----------------\n")

    if STREAM:
        # If streaming, the response is an iterable
        print(" ", end="")
        for message in response:
            if "content" in message["choices"][0]["delta"]:
                print(message["choices"][0]["delta"]["content"], end="", flush=True)
        print("\n\n-----------------")
    else:
        print(response)


def read_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a file prompt to GPT-4")
    parser.add_argument(
        "input_files", nargs="+", help="Input files to use for a prompt"
    )
    parser.add_argument(
        "--model", type=str, default=None, help="OpenAI Chat Model to use"
    )
    parser.add_argument(
        "--max_tokens", type=int, default=None, help="Max tokens to use"
    )
    parser.add_argument(
        "--temperature", type=float, default=None, help="Temperature to use"
    )
    parser.add_argument("--stream", type=bool, default=None, help="Stream the output")

    args = parser.parse_args()

    handle_args(args)

    print("Prompting with files:", args.input_files)

    input_text = ""
    for file_path in args.input_files:
        input_text += read_from_file(file_path)

    print_response(input_text)
