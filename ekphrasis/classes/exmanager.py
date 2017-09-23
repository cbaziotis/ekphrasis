import json
import re


class ExManager:

    with open('../regexes/expressions.txt') as fh:
        expressions = json.load(fh)

    def get_compiled(self):
        regexes = {k.lower(): re.compile(self.expressions[k]) for k, v in self.expressions.items()}
        return regexes

    def print_expressions(self):
        {print(k.lower(), ":", self.expressions[k]) for k, v in sorted(self.expressions.items())}
