import re


class Node:
    def __init__(self, name):
        self.tag = name
        # self.tagType = None

        self.tagValue = None
        self.children = []
        self.tagProperties = []

    def add_child(self, node):
        self.children.append(node)

    def get_child(self, index):
        return self.children[index]

    def add_property(self, node):
        self.tagProperties.append(node)

    def get_property(self, index):
        return self.tagProperties[index]

    def is_leaf(self):
        return len(self.children) == 0


class XMLTree:
    def __init__(self, my_file):
        self.XML = my_file
        self.editedXML = []

        x = re.split('<', self.XML)
        for n in x:
            self.editedXML.append(n.strip())
        self.root = Node(re.sub("[>/]", '', self.editedXML.pop()))
        self.create_tree(self.root)

    def create_tree(self, node):
        while len(self.editedXML) > 1:
            stack_top = self.editedXML.pop()
            if stack_top[0] != '/':
                if stack_top[-1] != '>':
                    node.add_child(Node(stack_top))
                    # self.editedXML.pop()
                return

            elif stack_top[0] == '/':
                new_node = Node(re.sub("[>/]", '', stack_top))
                node.add_child(new_node)
                self.create_tree(new_node)
        return


def main():
    txt = '''
    <users>
        <user>
            <id>1</id>
            <name>user1</name>
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
                    <id>2</id>
                </follower>
                <follower>
                    <id>4</id>
                </follower>
            </followers>
        </user>
    </users>
                
    '''
    tree = XMLTree(txt)
    print(tree.root.children[0].children[1].children[0].tag)


if __name__ == "__main__":
    main()
