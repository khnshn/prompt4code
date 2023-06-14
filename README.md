<p center="left">
  <img alt="Prompt4Code logo" height="100" src="./dialog.png">
</p>

# Prompt4Code: Automated In-Context Learning to Generate Code Provided Code Examples with Docstrings

[![Prompt4Code version](https://img.shields.io/badge/Prompt4Code-v0.1.0-blue)](#)
[![license](https://img.shields.io/badge/license-MIT-green)](#)

**Prompt4Code** is a command line tool that facilitates in-context learning, automatically by reading local source code examples and extracting doctrings and turning them into a conversation with openai's GPT models.

## Before you begin

Run `pip install -r requirements.txt`

## Usage

_Run `python main.py -h` or `python main.py --help`:_

**usage**: `main.py [-h] [-d DATA] [-v] [-p PROMPT] [-m MODEL] [-s SAVE] [-ca] [-l LIMIT] [-sh] [-r]`

**options:**

```
-h, --help show this help message and exit
-d DATA, --data DATA training source code files directory
-v, --verbose display detailed processing information
-p PROMPT, --prompt PROMPT
a short sentence or phrase that is used to initiate a conversation
-m MODEL, --model MODEL
gpt model to be used
-s SAVE, --save SAVE directory to save the prompt as a json file
-ca, --callapi calls openai api to generate response based on the input prompt
-l LIMIT, --limit LIMIT
limit the number of input files for context learning
-sh, --shuffle shuffle the order of the list of files to traverse
-r, --run immediately run and verbose the generated code
```

## Example

```
python main.py
--prompt "this is my example prompt"
--data ./examples /
--verbose
--shuffle
--run
--save ./responses/
```
