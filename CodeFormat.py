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
            if code[i] == '!' or code[i] == '?':
                while code[i] != '>':
                    i += 1
                i += 1
            elif code[i] == '/':
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
                closed = False
                while code[i] != '>' and code[i] != ' ':
                    if code[i] == '/' and code[i + 1] == '>':
                        closed = True
                    temp += code[i]
                    i += 1
                if code[i] == ' ':
                    while code[i] != '>':
                        if code[i] == '/' and code[i + 1] == '>':
                            closed = True
                        i += 1
                i += 1
                if not closed:
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
            if code[i] == '!' or code[i] == '?':
                while code[i] != '>':
                    new_code += code[i]
                    i += 1
                i += 1
            elif code[i] == '/':
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
                    if new_code[-1].isspace():
                        while new_code[-1].isspace():
                            new_code = new_code[:-1]
                    new_code += f"</{tag.top()}>"
                    tag.pop()
                closed = False
                while code[i] != '>' and code[i] != ' ':
                    if code[i] == '/' and code[i + 1] == '>':
                        closed = True
                    temp += code[i]
                    i += 1
                after_temp = ""
                if code[i] == ' ':
                    while code[i] != '>':
                        if code[i] == '/' and code[i + 1] == '>':
                            closed = True
                        after_temp += code[i]
                        i += 1
                i += 1
                new_code += f"<{temp + after_temp}>"
                if not closed:
                    tag.push(temp)
        else:
            str_in_tag += code[i]
            new_code += code[i]
            i += 1
    while not tag.is_empty():
        new_code += f"</{tag.top()}>"
        tag.pop()
    return prettify_code(new_code)


def no_spaces_str(text: str) -> str:
    return '>'.join([subtext.strip('\n' '\t') for subtext in text.split('>')])


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
#     "\n\t<user id has_id>" \
#     "\n\t\t<id>l" \
#     "\n\t\t<name>mustafa</name>" \
#     "\n\t\t<followers>" \
#     "\n\t\t\t<follower>" \
#     "\n\t\t\t\t<name>l</id>" \
#     "\n\t\t\t</follower>" \
#     "\n\t\t" \
#     "\n\t</user>" \
#     "\n</users>"
#
# ss = "<?dnlndjNNv'vnvfd?>" \
#      "<!--dshdsivpisvn-->" \
#      "<note>" \
#      "<frame f_num=2 />" \
#      "<to>Tove</to>" \
#      "<from>Jani</from>" \
#      "<heading>Reminder</heading>" \
#      "<body>Don't forget me this weekend!</body>" \
#      "</note>"

# tt = no_spaces_str(ss)
#
# nn = fix_error(ss)

# print(fix_error(tt))
# print(ss)
# print(mark_error(ss))
#print(fix_error(ss))
# print(prettify_code(ss))
# prettify_code(ss)
