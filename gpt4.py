import openai
import os
import argparse

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = 'gpt-4'
MAX_TOKENS = 4500
TEMPERATURE = 1
STREAM = False


def handle_args(args):
    if os.environ.get('OPENAI_MODEL'):
        set_model_config_model(os.environ.get('OPENAI_MODEL'))

    if args.model:
        set_model_config_model(args.model)

    if os.environ.get('OPENAI_MAX_TOKENS'):
        set_model_config_max_tokens(os.environ.get('OPENAI_MAX_TOKENS'))

    if args.max_tokens:
        set_model_config_max_tokens(args.max_tokens)

    if os.environ.get('OPENAI_TEMPERATURE'):
        set_model_config_temperature(os.environ.get('OPENAI_TEMPERATURE'))

    if args.temperature:
        set_model_config_temperature(args.temperature)

    if os.environ.get('OPENAI_STREAM'):
        set_model_config_stream(os.environ.get('OPENAI_STREAM'))

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

    # Make the API call
    response = openai.ChatCompletion.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        messages=messages,
        stream=STREAM
    )
    return response


def print_response(input_text):
    response = call_gpt_4(input_text)

    if STREAM:
        for message in response:
            print(message)
    else:
        print(response)


def read_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Send a file prompt to GPT-4')
    parser.add_argument('input_files', nargs='+',
                        help='Input files to use for a prompt')
    parser.add_argument('--model', type=str, default=None,
                        help='OpenAI Chat Model to use')
    parser.add_argument('--max_tokens', type=int, default=None,
                        help='Max tokens to use')
    parser.add_argument('--temperature', type=float, default=None,
                        help='Temperature to use')
    parser.add_argument('--stream', type=bool, default=None,
                        help='Stream the output')

    args = parser.parse_args()

    handle_args(args)

    for file_path in args.input_files:
        print("Prompting with file:", file_path)

        input_text = read_from_file(file_path)
        print_response(input_text)
