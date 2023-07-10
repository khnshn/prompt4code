import os
import random

for file in os.listdir("./"):
    if file.endswith(".txt"):
        with open(file, "r") as f:
            code = f.read()
            print(code)
            exec(
                code,
                {
                    "__builtins__": {
                        "__import__": __import__,
                        "print": print,
                        "random": random,
                        "__build_class__": __build_class__,
                        "object": object,
                        "__name__": __name__,
                        "range": range,
                    }
                },
                {},
            )
