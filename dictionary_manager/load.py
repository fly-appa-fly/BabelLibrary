from xml.dom import minidom


def load():
    doc = minidom.parse('eng-ukr.xdxf')
    words = doc.getElementsByTagName('ar')
    print(len(words))
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
                        print(child_node.firstChild.data.lower())
                    elif child_node.tagName == 'pos':
                        print('pos')
                        print(child_node.firstChild.firstChild.data)
                    else:
                        text_string += get_all_text(child_node.firstChild)
                else:
                    text_string += child_node.data


            return text_string

    print(get_all_text(word))

load()