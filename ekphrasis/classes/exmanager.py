import json
import os
import re


class ExManager:
    ext_path = os.path.join(os.path.dirname(__file__),
                            '../regexes/expressions.txt')

    with open(ext_path) as fh:
        expressions = json.load(fh)

    def get_compiled(self):
        regexes = {k.lower(): re.compile(self.expressions[k]) for k, v in
                   self.expressions.items()}
        return regexes

    def print_expressions(self):
        {print(k.lower(), ":", self.expressions[k])
         for k, v in sorted(self.expressions.items())}
