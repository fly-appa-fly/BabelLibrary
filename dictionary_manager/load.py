from xml.dom import minidom


def load():
    doc = minidom.parse('oxford.xdxf')
    words = doc.getElementsByTagName('ar')
    print(len(words))
    c = False
    word = words[0]

    def get_all_text(node):
        if node.nodeType == node.TEXT_NODE:
            return node.data
        else:
            text_string = ""
            for child_node in node.childNodes:
                if child_node.nodeType != child_node.TEXT_NODE:
                    if child_node.tagName == 'k':
                        print('k')
                        c = False
                    elif child_node.tagName == 'c':
                        print('c')
                        print(child_node.firstChild.firstChild.data)
                        c = True
                    elif child_node.tagName == 'b':
                        print('b')
                        c = False
                else:
                    if get_all_text(child_node) != '\n':

                        print('enter')

                        text = get_all_text(child_node).split('\n')
                        for t in text[1:]:
                            if t != '':
                                if c == True:
                                    print('c')
                                print('a ' +t+'\n')

            return text_string

    print(get_all_text(word))

load()