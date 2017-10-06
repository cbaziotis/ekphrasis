import json

##############################################################################
# EMOTICONS
##############################################################################
# [DPO023|}><=]?    # optional hat
# [xXB:#%=|;8\*]    # eyes
# ['\",]?           # optional tears
# [oc\-^]?          # optional nose
# [DpPO03cboÞþJSLxX*@$#&,.\|<>}{()\[\]\\/] # mouth
##############################################################################

__ltr_emoticon = [
    # optional hat
    r"(?:(?<![a-zA-Z])[DPO]|(?<!\d)[03]|[|}><=])?",

    # eyes
    r"(?:(?<![a-zA-Z\(])[xXB](?![a-ce-oq-zA-CE-OQ-Z,\.\/])|(?<![:])[:=|](?![\.])|(?<![%#\d])[%#](?![%#\d])|(?<![\d\$])[$](?![\d\.,\$])|[;](?!\()|(?<![\d\(\-\+])8(?![\da-ce-zA-CE-Z\\/])|\*(?![\*\d,.]))",

    # optional tears
    r"(?:['\",])?",

    # optional nose
    r"(?:(?<![\w*])[oc](?![a-zA-Z])|(?:[-‑^]))?",

    # mouth
    r"(?:[(){}\[\]<>|/\\]+|[Þ×þ]|(?<!\d)[30](?!\d)|(?<![\d\*])[*,.@#&](?![\*\d,.])|(?<![\d\$])[$](?![\d\.,\$])|[DOosSJLxXpPbc](?![a-zA-Z]))",
]

__rtl_emoticon = [
    r"(?<![\w])",
    r"(?:[(){}\[\]<>|/\\]+|(?<![\d\.\,])[0](?![\d\.])|(?![\d\*,.@#&])[*,.@#&]|[$]|(?<![a-zA-Z])[DOosSxX])",
    # mouth
    r"(?:[-‑^])?",  # optional nose
    r"(?:['\",])?",  # optional tears
    r"(?:[xX]|[:=|]|[%#]|[$8](?![\d\.])|[;]|\*)",  # eyes
    r"(?:[O]|[0]|[|{><=])?",  # optional hat
    r"(?![a-zA-Z])",
]

__LTR_FACE = "".join(__ltr_emoticon)
__RTL_FACE = "".join(__rtl_emoticon)

##############################################################################
# DATES/TIMES     todo: add days
# the regex captures most ways a date my be expressed in natural language.
##############################################################################
__short_date = r"(?:\b(?<!\d\.)(?:(?:(?:[0123]?[0-9][\.\-\/])?[0123]?[0-9][\.\-\/][12][0-9]{3})|(?:[0123]?[0-9][\.\-\/][0123]?[0-9][\.\-\/][12]?[0-9]{2,3}))(?!\.\d)\b)"
__full_date_parts = [
    # prefix
    r"(?:(?<!:)\b\'?\d{1,4},? ?)",

    # month names
    r"\b(?:[Jj]an(?:uary)?|[Ff]eb(?:ruary)?|[Mm]ar(?:ch)?|[Aa]pr(?:il)?|May|[Jj]un(?:e)?|[Jj]ul(?:y)?|[Aa]ug(?:ust)?|[Ss]ept?(?:ember)?|[Oo]ct(?:ober)?|[Nn]ov(?:ember)?|[Dd]ec(?:ember)?)\b",

    # suffix
    r"(?:(?:,? ?\'?)?\d{1,4}(?:st|nd|rd|n?th)?\b(?:[,\/]? ?\'?\d{2,4}[a-zA-Z]*)?(?: ?- ?\d{2,4}[a-zA-Z]*)?(?!:\d{1,4})\b)",
]
__fd1 = "(?:{})".format("".join(
    [__full_date_parts[0] + "?", __full_date_parts[1], __full_date_parts[2]]))
__fd2 = "(?:{})".format("".join(
    [__full_date_parts[0], __full_date_parts[1], __full_date_parts[2] + "?"]))
__date = "(?:" + "(?:" + __fd1 + "|" + __fd2 + ")" + "|" + __short_date + ")"

# print(__date)
# print(__date)

##############################################################################
# NUMBERS
##############################################################################
__number = r"\b\d+(?:[\.,']\d+)?\b"
__percentage = __number + "%"
__money = r"(?:[$€£¢]\d+(?:[\.,']\d+)?(?:[MmKkBb](?:n|(?:il(?:lion)?))?)?)|(?:\d+(?:[\.,']\d+)?[$€£¢])"

##############################################################################
# EXPRESSIONS
##############################################################################
EXPRESSIONS = {
    "HASHTAG": r"\#\b[\w\-\_]+\b",
    "CASHTAG": r"(?<![A-Z])\$[A-Z]+\b",
    "TAG": r"<[\/]?\w+[\/]?>",
    "USER": r"\@\w+",
    "EMPHASIS": r"(?:\*\b\w+\b\*)",
    "CENSORED": r"(?:\b\w+\*+\w+\b)",
    "ACRONYM": r"\b(?:[A-Z]\.)(?:[A-Z]\.)+(?:\.(?!\.))?(?:[A-Z]\b)?",
    "ELONGATED": r"\b[A-Za-z]*([a-zA-Z])\1\1[A-Za-z]*\b",
    "RTL_FACE": __RTL_FACE,
    "LTR_FACE": __LTR_FACE,
    "EASTERN_EMOTICONS": r"(?<![\w])(?:(?:[<>]?[\^;][\W_m][\;^][;<>]?)|(?:[^\s()]?m?[\(][\W_oTOJ]{1,3}[\s]?[\W_oTOJ]{1,3}[)]m?[^\s()]?)|(?:\*?[v>\-\/\\][o0O\_\.][v\-<\/\\]\*?)|(?:[oO0>][\-_\/oO\.\\]{1,2}[oO0>])|(?:\^\^))(?![\w])",
    "REST_EMOTICONS": r"(?<![A-Za-z0-9/()])(?:(?:\^5)|(?:\<3))(?![[A-Za-z0-9/()])",
    "EMOJI_UCS4": r"(?:[\U00002600-\U000027BF])|(?:[\U0001f300-\U0001f64F])|(?:[\U0001f680-\U0001f6FF])",
    "EMOJI_UCS2": r"(?:[\u2600-\u27BF])|(?:[\uD83C][\uDF00-\uDFFF])|(?:[\uD83D][\uDC00-\uDE4F])|(?:[\uD83D][\uDE80-\uDEFF])",
    "QUOTES": r"\"(\\.|[^\"]){2,}\"",
    "PERCENT": __percentage,
    "REPEAT_PUNCTS": r"([!?.]){2,}",
    "MONEY": __money,
    "EMAIL": r"(?:^|(?<=[^\w@.)]))(?:[\w+-](?:\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(?:\.(?:[a-z]{2,})){1,3}(?:$|(?=\b))",
    "PHONE": r'(?<![0-9])(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?![0-9])',
    "NUMBER": __number,
    "ALLCAPS": r"(?<![#@$])\b([A-Z][A-Z ]{1,}[A-Z])\b",
    # todo: fix - urls also capture trailing puncts, such as .
    "URL": r"(?:https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})",
    "DATE": __date,
    "TIME": r"(?:(?:\d+)?\.?\d+(?:AM|PM|am|pm|a\.m\.|p\.m\.))|(?:(?:[0-2]?[0-9]|[2][0-3]):(?:[0-5][0-9])(?::(?:[0-5][0-9]))?(?: ?(?:AM|PM|am|pm|a\.m\.|p\.m\.))?)",
    # "CAMEL_SPLIT": '((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))',
    # i think it can be simplified...
    # r'((?<=[a-z])[A-Z]|(?<=[A-Z][A-Z])[a-z]|(?<!^)(?<![A-Z])[A-Z](?=[a-z])|[0-9]+|(?<=[0-9\-\_])[A-Za-z]|[\-\_])',
    "CAMEL_SPLIT": r'((?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])|[0-9]+|(?<=[0-9\-\_])[A-Za-z]|[\-\_])',
    # REGEX_NORMALIZE_ELONG = '(.)\1+')
    "NORMALIZE_ELONG": r'(.)\1{2,}',
    "WORD": r"(?:[\w_]+)"
}

# # cant do all. win some, lose some ...
# testlist = [
#     "CamelCase",
#     "snake_case",
#     "MILvsPIT",
#     "WWENetwork",  # since this type of hashtag is more frequent i will optimize the regex for this case
#     "AlfaBetaGAMMA111deltaEpsilon123zeta-eta_theta",
# ]
#
# for t in testlist:
#     print(REGEXES["CAMEL_SPLIT"].sub(r' \1', t))

with open('expressions.txt', 'w') as file:
    file.write(json.dumps(EXPRESSIONS, sort_keys=True, indent=4, ))
