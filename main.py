import argparse
import os
from docstring_extractor import get_docstrings
import openaigpt as gpt
import json
from datetime import datetime
import re
import sys
import random


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_warning(msg):
    print(f"{bcolors.WARNING}{msg}{bcolors.ENDC}")


def print_info(msg):
    print(f"{bcolors.OKBLUE}{msg}{bcolors.ENDC}")


def print_success(msg):
    print(f"{bcolors.OKGREEN}{msg}{bcolors.ENDC}")


def print_fail(msg):
    print(f"{bcolors.FAIL}{msg}{bcolors.ENDC}")


parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "--data", help="training source code files directory", type=str
)
parser.add_argument(
    "-v",
    "--verbose",
    help="display detailed processing information",
    action="store_true",
)
parser.add_argument(
    "-p",
    "--prompt",
    help="a short sentence or phrase that is used to initiate a conversation",
    type=str,
)
parser.add_argument(
    "-m", "--model", help="gpt model to be used", default="gpt-3.5-turbo"
)
parser.add_argument(
    "-s",
    "--save",
    help="directory to save the prompt as a json file",
)
parser.add_argument(
    "-ca",
    "--callapi",
    help="calls openai api to generate response based on the input prompt",
    action="store_true",
)

parser.add_argument(
    "-l",
    "--limit",
    help="limit the number of input files for context learning",
    default=sys.maxsize,
    type=int,
)

parser.add_argument(
    "-sh",
    "--shuffle",
    help="shuffle the order of the list of files to traverse",
    action="store_true",
)

parser.add_argument(
    "-r",
    "--run",
    help="immediately run and verbose the generated code",
    action="store_true",
)

args = parser.parse_args()


verbose = args.verbose
LANGUAGE = "python"
DOMAIN = "simulation"
MAIN_FRAMEWORK = "simpy"
EXTENTION = ".py"
PROMPT_HEAD = [
    {
        "role": "system",
        "content": "You are a helpful assistant that generates python code per request",
    }
]

if args.data and args.prompt:
    if verbose:
        print_info(f"running with args: {args}")
        print_info(f"checking directory: {args.data}")
    prompt = PROMPT_HEAD.copy()
    counter = 0
    files = os.listdir(args.data)
    if args.shuffle:
        random.shuffle(files)
        if verbose:
            print_info("Shuffled")
    for file in files:
        if file.endswith(EXTENTION) and counter < args.limit:
            counter += 1
            if verbose:
                print_info(f"parsing {os.path.join(args.data, file)}")
            with open(os.path.join(args.data, file), "r") as py:
                docstrings = get_docstrings(py)
                user_content = f"Write a {DOMAIN} program in {LANGUAGE} using {MAIN_FRAMEWORK} with the following specifications:"
                user_content += (
                    f" a {docstrings['type']} as {docstrings['docstring_text']}"
                )
                for content in docstrings["content"]:
                    user_content += (
                        f" with a {content['type']} that {content['docstring_text']}"
                    )
                prompt.append({"role": "user", "content": user_content})
                py.seek(0, 0)
                source_code = py.read()
                source_code = re.sub(
                    r'(?s)(""".*?""")|#.*?$', "", source_code, flags=re.MULTILINE
                )
                prompt.append({"role": "assistant", "content": source_code})
                if verbose:
                    print(f"Docstrings: {docstrings}")
                    print(f"Source code: {source_code}")
    if prompt != PROMPT_HEAD:
        prompt.append({"role": "user", "content": args.prompt})
        if verbose:
            print(f"prompt: {prompt}")
        if args.save:
            with open(
                f"{args.save}prompt_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.json",
                "w",
            ) as f:
                f.write(json.dumps(prompt))
            if verbose:
                print_success("Prompt saved successfully")
        if args.callapi:
            if verbose:
                print_info(f"Calling OpenAI API with {args.model}")
            reason, response = gpt.chat(prompt, args.model)
            if verbose:
                print_warning(f"Finish reason: {reason}")
                print_info(response)
            if args.save:
                with open(
                    f"{args.save}response_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.txt",
                    "w",
                ) as f:
                    f.write(response)
                if verbose:
                    print_success("Response saved successfully")
            if args.run:
                if verbose:
                    print_info("Running the response")
                exec(response)

else:
    print_fail(
        "Not enough arguments are provided. Run with -h or --help for more information."
    )
