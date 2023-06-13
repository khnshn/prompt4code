<p center="left">
  <img alt="Prompt4Code logo" height="100" src="./dialog.png">
</p>

# Prompt4Code: Automated In-Context Learning to Generate Code Provided Code Examples with Docstrings

[![Prompt4Code version](https://img.shields.io/badge/version-Prompt4Code-red)](#)
[![license](https://img.shields.io/badge/license-MIT-green)](#)

**Prompt4Code** is a command line tool that facilitates in-context learning, automatically by reading local source code examples and extracting doctrings and turning them into a conversation with openai's GPT models.

## Before you begin

Run `pip install -r requirements.txt`

## Usage

Run `python main.py -h` or `python main.py --help`

## Usage example

`python main.py --prompt "write a simulation in python using simpy of a teacher's behavior in school. the teacher start with teaching, then go on a break, and then teach again, indefinitely. a teacher might get interrupted by their phone (such as receiving a notification). depending on task at hand and their availability they either respond to their interruption (caused by their phone) or they ignore it." --data ./examples --verbose --save ./responses/ --limit 3 --shuffle --callapi --run`
