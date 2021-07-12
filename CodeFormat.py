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
            i += 1
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

    return error_list


#tial
s = "<users>" \
    "\n\t<user>" \
    "\n\t\t<id>l" \
    "\n\t\t<name>mustafa</name>" \
    "\n\t\t<followers>" \
    "\n\t\t\t<follower>" \
    "\n\t\t\t\t<name>l</id>" \
    "\n\t\t\t</follower>" \
    "\n\t\t</followers>" \
    "\n\t</user>" \
    "\n</users>"
index = 0
tt = ""
while index < len(s):
    if not s[index].isspace():
        tt += s[index]
    index += 1


print(tt)

print(mark_error(s))
