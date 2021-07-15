import re


class Node:
    def __init__(self, name):
        self.tag = name
        self.is_printed = False

        self.children = []
        self.tagProperties = ""

    def add_child(self, node):
        self.children.append(node)

    def get_children(self):
        return self.children

    def add_property(self, str):
        self.tagProperties = str

    def get_properties(self):
        dict = {}
        if len(self.tagProperties) == 0:
            return dict
        properties = self.tagProperties.partition(' ')
        for i in range(len(properties)):
            if properties[i] != '' and properties[i] != ' ':
                single_property = properties[i].partition('=')
                dict[single_property[0]] = single_property[2]
        return dict

    def is_leaf(self):
        return len(self.children) == 0

    def height(self):
        max = -1
        sum = 0
        stack = [self]
        while len(stack) > 0:
            popped = stack.pop()
            if popped.is_leaf():
                if sum > max:
                    max = sum
                sum = 0
            sum += 1
            for child in popped.get_children():
                stack.append(child)
        return max


class XMLTree:
    def __init__(self, my_file):
        self.XML = my_file
        self.editedXML = []

        x = re.split('<', self.XML)
        for n in x:
            self.editedXML.append(n.strip())
        self.root = Node(re.sub("[>/]", '', self.editedXML.pop()))
        self.create_tree(self.root)

    def get_root(self):
        return self.root

    def create_tree(self, node):
        while len(self.editedXML) > 1:
            stack_top = self.editedXML.pop()
            if stack_top[0] != '/':

                # get the attributes out of the tag
                string_of_property = re.findall('(?<=\s).*?(?=>)', stack_top)
                if len(string_of_property) > 0:
                    node.add_property(string_of_property[0])

                # the open tag is next to the data without spacing, this cond. check if there's data or it just open tag
                if stack_top[-1] != '>':
                    # if there's data, extract it
                    split_tag_from_data = stack_top.partition('>')
                    node.add_child(Node(split_tag_from_data[2]))
                return

            # if it is closing tag create a node, as a child to the current node
            elif stack_top[0] == '/':
                new_node = Node(re.sub("[>/]", '', stack_top))
                node.add_child(new_node)
                self.create_tree(new_node)
        return


class RefStr:
    # wrap string in object, so it is passed by reference rather than by value

    def __init__(self, s=""):
        self.s = s

    def __add__(self, s):
        self.s += s
        return self

    def __str__(self):
        return self.s


def XML2json(tree):
    str = RefStr("{\n")
    square = False
    dfs(tree.get_root(), 1, str, square, False)
    str += "\n}"
    print(str)
    return str


def dfs(node, depth, str, square, is_last):
    open_bracket = False

    if not node.is_leaf():
        str += f'{"  " * depth}'

    if not node.is_printed:
        str += f'"{node.tag}"'
        if node.is_leaf():
            str += ",\n"

        elif not node.is_leaf():
            str += ":"

    if square:
        square = False
        str += "[\n"
        str += f'{"  " * depth}'

    if node.height() > 1 or len(node.get_properties()) > 0:
        open_bracket = True
        str += " {\n"
        key = list(node.get_properties().keys())
        val = list(node.get_properties().values())
        for i in range(len(node.get_properties())):
            str += f'{"  " * depth} "{key[i]}": {val[i]},\n'
        if len(node.get_properties()) > 0 and node.get_children()[0].is_leaf():
            str += f'{"  " * depth} "#text": '

    # for child in reversed(node.get_children()):
    for i in reversed(range(len(node.get_children()))):

        for j in range(len(node.get_children())):
            # err at index*
            if node.get_children()[i].tag == node.get_children()[j].tag and i != j:
                is_last = False
                if i == 0:
                    is_last = True
                square = False
                if not node.get_children()[i].is_printed:
                    square = True
                    node.get_children()[j].is_printed = True

        dfs(node.get_children()[i], depth + 1, str, square, is_last)

    if open_bracket:
        if depth > 1:
            str += f'{"  " * depth}}},\n'
        else:
            str += f'{"  " * depth}}}'

    if node.is_printed and is_last:
        str += f'{"  " * depth}],\n'


def main():
    txt = '''
    <users>
        <user myAtrr="mostafa">
            <id wow="mom">1</id>
            <name adena_bengarab="heeeelp">user1</name>
            <posts>
                <post>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaalllllllllllllllllllllllllllllllllllllllllllllllll
                    llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
                </post>
                <post>mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmssssssssssssssssssssssssssssssssssssssssssss
                    m,mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmlllllllllllllllllllllllllllllllllllllllllllllllllllll
                </post>
            </posts>
            <followers>
                <follower>
                    <id wa7ed="ana" etnen="mostafa">2</id>
                </follower>
                <follower>
                    <id>4</id>
                </follower>
                <follower>
                    <id>ahmed</id>
                </follower>
            </followers>
        </user>
    </users>
                
    '''
    tree = XMLTree(txt)
    # print(tree.root.children[0].children[0].height())
    XML2json(tree)
    # print(tree.root.children[0].children[0].children[1].children[0].get_properties())


if __name__ == "__main__":
    main()
