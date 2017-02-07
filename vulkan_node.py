class Node(object):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __repr__(self):
        return str(self.__class__) + self.name

    def __str__(self):
        return self.name + " -- " + self.desc

    def color(self):
        raise NotImplementedError


class HandleNode(Node):
    def __init__(self, name, desc):
        super(HandleNode, self).__init__(name, desc)

    def color(self):
        return "crimson"


class StructNode(Node):
    def __init__(self, name, desc):
        super(StructNode, self).__init__(name, desc)

    def color(self):
        return "forestgreen"


class ElementNode(Node):
    def __init__(self, name, desc):
        super(ElementNode, self).__init__(name, desc)

    def color(self):
        return "navy"


class CommandNode(Node):
    def __init__(self, name, desc):
        super(CommandNode, self).__init__(name, desc)

    def color(self):
        return "black"
