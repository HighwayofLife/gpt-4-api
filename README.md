# GPT-4 API Utilities

This repo contains python scripts that allow you to interact with the ChatGPT API's, specifically tuned to interact with GPT-4 by default.

#### Contains the following scripts:

  - `chunk_file.py` - Split a file up into smaller chunks. Configurable to split by word count and/or token count.
  - `tokenizer.py` - Count The words and tokens of a file.
  - `gpt4.py` - Send in files as prompts to the Chat GPT-4 API, with configurable parameters for max token count, temperature, streaming capability, and more.

## `GPT4.py` - Send prompts to the GPT-4 API

This Python script allows you to use the GPT-4 API. It reads prompts from text files and sends them to the GPT-4 API, then prints the responses.

### Requirements

- Python 3.6 or higher
- OpenAI Python client v0.27.0 or higher

### Setup

1. Install the required Python package:

    ```bash
    pip install openai
    ```

2. Set your OpenAI API key as an environment variable:

    ```bash
    export OPENAI_API_KEY='your-api-key'
    ```

### Usage

You can run the script from the command line with the following syntax:

```bash
python gpt4.py input_file1 [input_file2 ...]
  [--model MODEL]
  [--max-tokens MAX_TOKENS]
  [--temperature TEMPERATURE]
  [--stream STREAM]
```

These parameters can also all be set from the Environment:
```bash
export OPENAI_MODEL="gpt-4"
export OPENAI_MAX_TOKENS=1000
export OPENAI_TEMPERATURE=1
export OPENAI_STREAM=true
```

| Parameter                       | Description                                                                                               | Default |
| ------------------------------- | --------------------------------------------------------------------------------------------------------- | ------- |
| `input_file1 [input_file2 ...]` | One or more text files containing the prompts to send to the GPT-4 API.                                   | N/A     |
| `--model MODEL`                 | The ID of the model to use.                                                                               | 'gpt-4' |
| `--max-tokens MAX_TOKENS`       | The maximum number of tokens for the API to generate.                                                     | 4500    |
| `--temperature TEMPERATURE`     | The temperature for the API to use when generating text.                                                  | 1       |
| `--stream STREAM`               | Whether to enable streaming. If set to `true`, the script will print the API's responses as they come in. | `false` |

For example, to send prompts from `prompt1.txt` and `prompt2.txt` to the GPT-4 API with streaming enabled, you would use:

```bash
python script.py prompt1.txt prompt2.txt --stream true
```

---

## File Chunking Tool

This tool reads a text file and splits it into smaller files by word or token count limits using a specified GPT model for tokenization. The tool provides a command-line interface for specifying these limits and supports processing multiple input files in one run.

### Prerequisites

You'll need Python 3.6 or later. Additionally, the following Python packages are required:

- argparse
- os
- tiktoken

You can install these with pip:

```bash
pip install argparse os tiktoken
```

### Usage

The script is run from the command line with the following arguments:

- `--word-limit`: The maximum number of words per chunk. If not provided, the script defaults to 3000 words.
- `--token-limit`: The maximum number of tokens per chunk, as defined by the GPT model. This takes precedence over the word limit if provided.
- `input_files`: One or more text files to be processed.


Example command:

```bash
python chunk_file.py input_file1.txt [input_file2 ...]
  [--word-limit WORD_LIMIT]
  [--token_limit MAX_TOKENS]
```

### Configuration

The following constants can be adjusted at the top of the script:

- `WORD_LIMIT`: Default word limit per chunk if not specified on command line.
- `TOKEN_LIMIT`: Default token limit per chunk if not specified on command line.
- `GPT_MODEL`: Name of the GPT model to use for tokenization. Adjust according to the latest model available.

### Output

The script creates one or more output files for each input file. The output files are named by appending a number to the name of the input file, e.g., `input1.1.txt`, `input1.2.txt`, etc.

The script prints to the console the name of each output file and the number of words and tokens written to that file. If a line would cause an output file to exceed the word or token limit, that line is moved to the next output file. 

Please note that the actual number of words or tokens written to the final output file for each input file may be less than the specified limit.

### Limitations

The script assumes that words are not split across lines and that lines fit in memory. If a word is split across two lines, the script will count it as two words. If you need to handle these cases, you'll need a more complex solution.

### License

This project is licensed under the terms of the [MIT license](./LICENSE)
