import os
import argparse
import tiktoken


WORD_LIMIT = 3000
TOKEN_LIMIT = 0
GPT_MODEL = "gpt-4"
ENCODING = None


def config_set_word_limit(word_limit):
    global WORD_LIMIT
    WORD_LIMIT = word_limit


def config_set_token_limit(token_limit):
    global TOKEN_LIMIT
    TOKEN_LIMIT = token_limit


def config_set_gpt_model(gpt_model):
    global GPT_MODEL
    GPT_MODEL = gpt_model


def config_set_encoding_for_model():
    global ENCODING

    ENCODING = tiktoken.encoding_for_model(GPT_MODEL)


def count_tokens(input_text):
    if not ENCODING:
        config_set_encoding_for_model()

    return len(ENCODING.encode(input_text))


def split_file(file_path):
    # check if the file exists
    if not os.path.isfile(file_path):
        print(f"File: {file_path} does not exist.")
        return

    with open(file_path, 'r') as f:
        file_num = 1
        word_count = 0
        token_count = 0
        output_file = None
        current_line = ""

        for line in f:
            words = line.strip().split()
            new_token_count = token_count + count_tokens(line)
            new_word_count = word_count + len(words)

            if ((TOKEN_LIMIT > 0 and new_token_count > TOKEN_LIMIT) or new_word_count > WORD_LIMIT) and output_file:
                # Show the file being written and the number of words written to that file
                print(
                    f"Writing to file: {new_file_name}, with {word_count} words and {token_count} tokens.")
                output_file.close()
                output_file = None

            if not output_file:
                # open new output file
                # Strip the extension from the original file name and append a number
                new_file_name = os.path.splitext(
                    file_path)[0] + f".{file_num}.txt"
                output_file = open(new_file_name, 'w')
                file_num += 1
                word_count = 0
                token_count = 0

            # write line to current output file
            output_file.write(current_line)
            word_count += len(words)
            token_count += count_tokens(current_line)
            current_line = line

        if output_file:
            # Show the file being written and the number of words written to that file
            print(
                f"Writing to file: {new_file_name}, with {word_count} words and {token_count} tokens.")
            output_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Count the words and tokens in a file:')
    parser.add_argument('--word-limit', type=int, default=None,
                        help='Chunk word limit for the operation, token limit takes precedence over word limit')
    parser.add_argument('--token-limit', type=int, default=None,
                        help='Chunk token limit for the operation, token limit takes precedence over word limit')
    parser.add_argument('input_files', nargs='+',
                        help='Input files to operate on')

    args = parser.parse_args()

    word_limit = args.word_limit
    token_limit = args.token_limit

    # Loop over the input files
    for file_path in args.input_files:
        print("Processing file:", file_path)
        if word_limit is not None:
            print("Word limit:", word_limit)
            config_set_word_limit(word_limit)

        if token_limit is not None:
            print("Token limit:", token_limit)
            config_set_token_limit(token_limit)

        split_file(file_path)
