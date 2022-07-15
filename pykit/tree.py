import string
import json

"""
缩进树语法解析器，将缩进树结构解析成AST语法树对象
"""

"""
generate
  adt
    edit
    edit2
generate-2
  adt-2
  adt-3
    edit3
    edit5
"""

token = []
tokens = []
chars = string.ascii_letters + string.digits + "[]-"


class EOF:
    pass


def emmit_token(_type):
    global token
    tokens.append({"type": _type, "value": "".join(token)})
    token = []


def start(char):
    if char in chars:
        token.append(char)
        return is_chars

    if char in "\r\n":
        token.append(char)
        return is_wrap_line

    if char == " ":
        token.append(char)
        return is_space

    raise SyntaxError("无效字符")


def is_chars(char):
    if isinstance(char, EOF):
        emmit_token("Name")
        return start

    if char in chars:
        token.append(char)
        return is_chars

    if char in "\r\n":
        emmit_token("Name")
        token.append(char)
        return is_wrap_line

    if char == " ":
        emmit_token("Name")
        token.append(char)
        return is_space

    raise SyntaxError("无效字符")


def is_wrap_line(char):
    if isinstance(char, EOF):
        emmit_token("WrapLine")
        return start

    if char in chars:
        emmit_token("WrapLine")
        token.append(char)
        return is_chars

    if char in "\r\n":
        token.append(char)
        return is_wrap_line

    if char == " ":
        emmit_token("WrapLine")
        token.append(char)
        return is_space

    raise SyntaxError("无效字符")


def is_space(char):
    if isinstance(char, EOF):
        emmit_token("WhiteSpace")
        return start

    if char in chars:
        emmit_token("WhiteSpace")
        token.append(char)
        return is_chars

    if char in "\r\n":
        emmit_token("WhiteSpace")
        token.append(char)
        return is_wrap_line

    if char == " ":
        token.append(char)
        return is_space

    raise SyntaxError("无效字符")


with open("./views.tree", "r") as fp:
    content = fp.read()
    state = start
    for c in content:
        state = state(c)
    state(EOF())
obj = []


def expression():
    current = 0
    size = len(tokens)
    distance = 0

    def walk(parent_distance=-1):
        nonlocal current, size, distance

        node_list = []
        while True:
            if current >= size:
                return node_list

            _token = tokens[current]

            if _token["type"] == "WrapLine":
                distance = 0

            if _token["type"] == "WhiteSpace":
                distance = len(_token["value"])
                if distance <= parent_distance:
                    return node_list

            if _token["type"] == "Name":
                if distance == 0 and parent_distance != -1:
                    current -= 1
                    return node_list

                node = {
                    "type": "ItemLiteral",
                    "name": _token["value"],
                    "item": []
                }
                current += 1
                node["item"] = walk(distance)
                node_list.append(node)

                if distance <= parent_distance:
                    return node_list

            current += 1

    return walk()


if __name__ == '__main__':
    print(json.dumps(expression(), indent=4))
