import re

# todo:catch repeating parenthesis
emoticons = {
    ':*': '<kiss>',
    ':-*': '<kiss>',
    ':x': '<kiss>',
    ':-)': '<happy>',
    ':-))': '<happy>',
    ':-)))': '<happy>',
    ':-))))': '<happy>',
    ':-)))))': '<happy>',
    ':-))))))': '<happy>',
    ':)': '<happy>',
    ':))': '<happy>',
    ':)))': '<happy>',
    ':))))': '<happy>',
    ':)))))': '<happy>',
    ':))))))': '<happy>',
    ':)))))))': '<happy>',
    ':o)': '<happy>',
    ':]': '<happy>',
    ':3': '<happy>',
    ':c)': '<happy>',
    ':>': '<happy>',
    '=]': '<happy>',
    '8)': '<happy>',
    '=)': '<happy>',
    ':}': '<happy>',
    ':^)': '<happy>',
    '|;-)': '<happy>',
    ":'-)": '<happy>',
    ":')": '<happy>',
    '\o/': '<happy>',
    '*\\0/*': '<happy>',
    ':-D': '<laugh>',
    ':D': '<laugh>',
    # '(\':': '<laugh>',
    '8-D': '<laugh>',
    '8D': '<laugh>',
    'x-D': '<laugh>',
    'xD': '<laugh>',
    'X-D': '<laugh>',
    'XD': '<laugh>',
    '=-D': '<laugh>',
    '=D': '<laugh>',
    '=-3': '<laugh>',
    '=3': '<laugh>',
    'B^D': '<laugh>',
    '>:[': '<sad>',
    ':-(': '<sad>',
    ':-((': '<sad>',
    ':-(((': '<sad>',
    ':-((((': '<sad>',
    ':-(((((': '<sad>',
    ':-((((((': '<sad>',
    ':-(((((((': '<sad>',
    ':(': '<sad>',
    ':((': '<sad>',
    ':(((': '<sad>',
    ':((((': '<sad>',
    ':(((((': '<sad>',
    ':((((((': '<sad>',
    ':(((((((': '<sad>',
    ':((((((((': '<sad>',
    ':-c': '<sad>',
    ':c': '<sad>',
    ':-<': '<sad>',
    ':<': '<sad>',
    ':-[': '<sad>',
    ':[': '<sad>',
    ':{': '<sad>',
    ':-||': '<sad>',
    ':@': '<sad>',
    ":'-(": '<sad>',
    ":'(": '<sad>',
    'D:<': '<sad>',
    'D:': '<sad>',
    'D8': '<sad>',
    'D;': '<sad>',
    'D=': '<sad>',
    'DX': '<sad>',
    'v.v': '<sad>',
    "D-':": '<sad>',
    '(>_<)': '<sad>',
    ':|': '<sad>',
    '>:O': '<surprise>',
    ':-O': '<surprise>',
    ':-o': '<surprise>',
    ':O': '<surprise>',
    '°o°': '<surprise>',
    'o_O': '<surprise>',
    'o_0': '<surprise>',
    'o.O': '<surprise>',
    'o-o': '<surprise>',
    '8-0': '<surprise>',
    '|-O': '<surprise>',
    ';-)': '<wink>',
    ';)': '<wink>',
    '*-)': '<wink>',
    '*)': '<wink>',
    ';-]': '<wink>',
    ';]': '<wink>',
    ';D': '<wink>',
    ';^)': '<wink>',
    ':-,': '<wink>',
    '>:P': '<tong>',
    ':-P': '<tong>',
    ':P': '<tong>',
    'X-P': '<tong>',
    'x-p': '<tong>',
    'xp': '<tong>',
    'XP': '<tong>',
    ':-p': '<tong>',
    ':p': '<tong>',
    '=p': '<tong>',
    ':-Þ': '<tong>',
    ':Þ': '<tong>',
    ':-b': '<tong>',
    ':b': '<tong>',
    ':-&': '<tong>',
    '>:\\': '<annoyed>',
    '>:/': '<annoyed>',
    ':-/': '<annoyed>',
    ':-.': '<annoyed>',
    ':/': '<annoyed>',
    ':\\': '<annoyed>',
    '=/': '<annoyed>',
    '=\\': '<annoyed>',
    ':L': '<annoyed>',
    '=L': '<annoyed>',
    ':S': '<annoyed>',
    '>.<': '<annoyed>',
    ':-|': '<annoyed>',
    '<:-|': '<annoyed>',
    ':-X': '<seallips>',
    ':X': '<seallips>',
    ':-#': '<seallips>',
    ':#': '<seallips>',
    'O:-)': '<angel>',
    '0:-3': '<angel>',
    '0:3': '<angel>',
    '0:-)': '<angel>',
    '0:)': '<angel>',
    '0;^)': '<angel>',
    '>:)': '<devil>',
    '>:D': '<devil>',
    '>:-D': '<devil>',
    '>;)': '<devil>',
    '>:-)': '<devil>',
    '}:-)': '<devil>',
    '}:)': '<devil>',
    '3:-)': '<devil>',
    '3:)': '<devil>',
    'o/\o': '<highfive>',
    '^5': '<highfive>',
    '>_>^': '<highfive>',
    '^<_<': '<highfive>',  # todo:fix tokenizer - MISSES THIS
    '<3': '<heart>'
}

# todo: clear this mess
pattern = re.compile("^[:=\*\-\(\)\[\]x0oO\#\<\>8\\.\'|\{\}\@]+$")
mirror_emoticons = {}
for exp, tag in emoticons.items():
    if pattern.match(exp) \
            and any(ext in exp for ext in [";", ":", "="]) \
            and not any(ext in exp for ext in ["L", "D", "p", "P", "3"]):
        mirror = exp[::-1]

        if "{" in mirror:
            mirror = mirror.replace("{", "}")
        elif "}" in mirror:
            mirror = mirror.replace("}", "{")

        if "(" in mirror:
            mirror = mirror.replace("(", ")")
        elif ")" in mirror:
            mirror = mirror.replace(")", "(")

        if "<" in mirror:
            mirror = mirror.replace("<", ">")
        elif ">" in mirror:
            mirror = mirror.replace(">", "<")

        if "[" in mirror:
            mirror = mirror.replace("[", "]")
        elif "]" in mirror:
            mirror = mirror.replace("]", "[")

        if "\\" in mirror:
            mirror = mirror.replace("\\", "/")
        elif "/" in mirror:
            mirror = mirror.replace("/", "\\")

        # print(exp + "\t\t" + mirror)
        mirror_emoticons[mirror] = tag
emoticons.update(mirror_emoticons)

for exp, tag in list(emoticons.items()):
    if exp.lower() not in emoticons:
        emoticons[exp.lower()] = tag

emoticon_groups = {
    "positive": {'<highfive>', '<laugh>', '<heart>', '<happy>'},
    "negative": {'<annoyed>', '<sad>', }
}


def print_positive(sentiment):
    for e, tag in emoticons.items():
        if tag in emoticon_groups[sentiment]:
            print(e)

# print_positive("negative")
# print(" ".join(list(emoticons.keys())))
# [print(e) for e in list(emoticons.keys())]
