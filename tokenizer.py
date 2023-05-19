import tiktoken
import argparse


def count_tokens(input_text):
    encoding = tiktoken.encoding_for_model('gpt-4')

    return len(encoding.encode(input_text))


def count_tokens_in_file(file_path):
    with open(file_path, 'r') as file:
        return count_tokens(file.read())


def count_words(input_text):
    return len(input_text.split())


def count_words_in_file(file_path):
    with open(file_path, 'r') as file:
        return count_words(file.read())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Count the words and tokens in a file:')
    parser.add_argument('input_files', nargs='+',
                        help='Input files to operate on')

    args = parser.parse_args()

    # Loop over the input files
    for file_path in args.input_files:
        print("Processing file:", file_path)

        tokens = count_tokens_in_file(file_path)
        words = count_words_in_file(file_path)
        print(f"Number of tokens: {tokens}")
        print(f"Number of words: {words}")
        print(f"Ratio of tokens to words: {tokens / words}")