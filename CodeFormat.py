from Stack import *


def mark_error(code: str):
    line_number = 1
    error_list = []
    tag = Stack()
    tag_line = Stack()
    i = 0
    str_in_tag = "\t"
    while i < len(code):
        if code[i] == '\n':
            line_number += 1
        if code[i] == '<':
            i += 1
            temp = str()
            if code[i] == '/':
                i += 1
                while code[i] != '>':
                    temp += code[i]
                    i += 1
                i += 1
                if not tag.is_empty() and temp == tag.top():
                    str_in_tag = "\t"
                    tag.pop()
                    tag_line.pop()
                else:
                    if not str_in_tag.isspace():
                        error_list.append(line_number)
                        tag_line.pop()
                        tag.pop()
                        str_in_tag = "\t"
                    else:
                        if line_number != 1:
                            error_list.append(line_number - 1)
                        else:
                            error_list.append(line_number)
                        while not tag.is_empty() and temp != tag.top():
                            tag.pop()
                            tag_line.pop()
                        if not tag.is_empty() and temp == tag.top():
                            tag.pop()
                            tag_line.pop()
            else:
                if not str_in_tag.isspace():
                    error_list.append(tag_line.top())
                    tag_line.pop()
                    tag.pop()
                while code[i] != '>':
                    temp += code[i]
                    i += 1
                i += 1
                tag.push(temp)
                tag_line.push(line_number)

        else:
            str_in_tag += code[i]
            i += 1
    while not tag.is_empty():
        error_list.append(line_number)
        tag_line.pop()
        tag.pop()

    return error_list


def fix_error(code: str):
    if len(mark_error(code)) == 0:
        return code
    new_code = str()
    tag = Stack()
    i = 0
    str_in_tag = "\t"
    while i < len(code):
        if code[i] == '<':
            i += 1
            temp = str()
            if code[i] == '/':
                i += 1
                while code[i] != '>':
                    temp += code[i]
                    i += 1
                i += 1
                if not tag.is_empty() and temp == tag.top():
                    str_in_tag = "\t"
                    new_code += f"</{temp}>"
                    tag.pop()
                else:
                    if not str_in_tag.isspace():
                        new_code += f"</{tag.top()}>"
                        tag.pop()
                        str_in_tag = "\t"
                    else:
                        while not tag.is_empty() and temp != tag.top():
                            new_code += f"</{tag.top()}>"
                            tag.pop()
                        if not tag.is_empty() and temp == tag.top():
                            new_code += f"</{tag.top()}>"
                            tag.pop()
            else:
                if not str_in_tag.isspace():
                    new_code += f"</{tag.top()}>"
                    tag.pop()
                while code[i] != '>':
                    temp += code[i]
                    i += 1
                i += 1
                new_code += f"<{temp}>"
                tag.push(temp)
        else:
            str_in_tag += code[i]
            new_code += code[i]
            i += 1
    while not tag.is_empty():
        new_code += f"</{tag.top()}>"
        tag.pop()
    return new_code


def no_spaces_str(string: str):
    final = str()
    for ch in string:
        if not ch.isspace():
            final += ch
    return final


def add_spaces(tap):
    i = 0
    final = str()
    while i < tap:
        final += "\t"
        i += 1
    return final


def prettify_code(s: str):
    code = no_spaces_str(s)
    final = str()
    taps = 0
    i = 0
    while i < len(code):
        if i + 1 < len(code) and code[i+1] == "<":
            if i + 2 < len(code) and code[i+2] != "/":
                taps += 1
                final += code[i]
                i += 1
                if code[i - 1] == ">":
                    final += "\n"
                    final += add_spaces(taps)
            else:
                final += code[i]
                i += 1
                if code[i - 1] == ">":
                    final += "\n"
                    final += add_spaces(taps)
                taps -= 1
        final += code[i]
        i += 1

    return final


#tial
# ss = "<users>" \
#     "\n\t<user>" \
#     "\n\t\t<id>l" \
#     "\n\t\t<name>mustafa</name>" \
#     "\n\t\t<followers>" \
#     "\n\t\t\t<follower>" \
#     "\n\t\t\t\t<name>l</id>" \
#     "\n\t\t\t</follower>" \
#     "\n\t\t" \
#     "\n\t" \
#     "\n"
# index = 0
# tt = ""
# while index < len(ss):
#     if not ss[index].isspace():
#         tt += ss[index]
#     index += 1
#
#
# nn = fix_error(ss)
# print(prettify_code(nn))

# print(fix_error(tt))
# print(mark_error(fix_error(tt)))

