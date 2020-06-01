import re
from janlz.constants import Token, KEYWORD_LOOKUP_MAP, ESCAPED_SYMBOL

KEYWORD_REX = re.compile(
    r'^(class|constructor|function|method|field|static|var|int\s|char\s|boolean|void|true|false|null|this|let|do\s|if|else|while|return)')
SYMBOL_REX = re.compile(r'^([{}()\[\]_.,;+\-*\/&|<>=~])')
IDENTIFIER_REX = re.compile(r'^([a-zA-Z_][a-zA-Z0-9_]*)')
INT_CONSTANT_REX = re.compile(r'^(\d{1,5})')
STRING_CONSTANT_REX = re.compile(r'^\"(.*)\"')


def _parse_4digit_number(s):
    i = int(s)
    if 0 <= i <= 32767:
        return i
    else:
        raise ValueError("{0} is out of range".format(i))


def _remove_comment(lines):
    '''
    skip comment expression in the lines.
    TODO: Optimize the performance (ex: Loop, Recursive).
    - Case1: // ~
    - Case2: /** ~ */
    - Case3: Multi Line Comment
    /**
      * ~
      */

    :return: void
    '''

    # Case 1
    lines = [l.split('//')[0] for l in lines]

    # Case 2
    ONE_LINE_COMMENT_REX = re.compile(r'(\/\*(.*)\*\/)')
    lines = [re.sub(ONE_LINE_COMMENT_REX, '', l) for l in lines]

    # Case 3
    MULTI_LINES_COMMENT_REX_START = re.compile(r'^(\s*\/\*\*\s*.*[\*\/]*)$')
    MULTI_LINES_COMMENT_REX_MID = re.compile(r'^(\s*\*.*)$')
    MULTI_LINES_COMMENT_REX_END = re.compile(r'^(\s*\*\/)$')
    for i, line in enumerate(lines):
        result = MULTI_LINES_COMMENT_REX_START.match(line)
        if result is not None and result.group(1) is not None:

            # Subtract "/** ~"
            lines[i] = re.sub(MULTI_LINES_COMMENT_REX_START, '', line).strip()

            # Subtract "* ~"
            i += 1
            mid_line = lines[i]
            match = MULTI_LINES_COMMENT_REX_MID.match(mid_line)
            while match is not None and match.group(1) is not None:
                lines[i] = re.sub(MULTI_LINES_COMMENT_REX_MID, '', mid_line).strip()
                if len(lines) == i+1: break
                i += 1
                mid_line = lines[i]
                match = MULTI_LINES_COMMENT_REX_MID.match(mid_line)

            # Subtract "*/"
            last_line = lines[i]
            match = MULTI_LINES_COMMENT_REX_END.match(last_line)
            if match is not None and match.group(1) is not None:
                lines[i] = re.sub(MULTI_LINES_COMMENT_REX_END, '', last_line).strip()

    return lines


class Tokenizer:

    def __init__(self, path):
        f = open(path, 'r')
        self.lines = f.readlines()
        f.close()

        # Remove newline char from the input
        self.lines = [com.rstrip() for com in self.lines]
        # Remove comment
        self.lines = _remove_comment(self.lines)

        self.index = 0
        self.last = len(self.lines)
        self.line = self.lines[self.index]
        self._clear()
        return

    def has_more_token(self):
        return self.line is not "" or self.index < self.last

    def advance(self):
        self._clear()

        result = self._read_line(SYMBOL_REX, self.line, Token.SYMBOL)
        if result != self.line:
            self.line = result
            return
        result = self._read_line(KEYWORD_REX, result, Token.KEYWORD)
        if result != self.line:
            self.line = result
            return
        result = self._read_line(IDENTIFIER_REX, result, Token.IDENTIFIER)
        if result != self.line:
            self.line = result
            return
        result = self._read_line(STRING_CONSTANT_REX, result, Token.STRING_CONST)
        if result != self.line:
            self.line = result
            return
        result = self._read_line(INT_CONSTANT_REX, result, Token.INT_CONST)

        if result == self.line:
            self.line = self.line[1:]
        else:
            self.line = result

        if self.line is "":
            self.index += 1
            if self.index != self.last:
                self.line = self.lines[self.index]
        return

    def token_type(self):
        return self._token_type

    def keyword(self):
        return self._keyword

    def symbol(self):
        return self._symbol

    def identifier(self):
        return self._identifier

    def int_val(self):
        return self._int_val

    def string_val(self):
        return self._string_val

    def _clear(self):
        self._token_type, self._keyword, self._symbol = None, None, None
        self._identifier, self._int_val, self._string_val = None, None, None

    def _read_line(self, rex, line, token_type):
        result = rex.match(line)
        if result is not None and result.group(1) is not None:
            if token_type is not None:
                self._token_type = token_type
            if token_type is Token.KEYWORD:
                self._keyword = KEYWORD_LOOKUP_MAP.get(result.group(1).replace(" ", ""))
            elif token_type is Token.SYMBOL:
                self._symbol = result.group(1)
            elif token_type is Token.IDENTIFIER:
                self._identifier = result.group(1)
            elif token_type is Token.INT_CONST:
                self._int_val = _parse_4digit_number(result.group(1))
            elif token_type is Token.STRING_CONST:
                replaced_str = result.group(1)
                for k, v in ESCAPED_SYMBOL.items(): replaced_str = replaced_str.replace(k, v)
                self._string_val = replaced_str

            return re.sub(rex, '', line)
        else:
            return line
