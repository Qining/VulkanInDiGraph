import pygraphviz as pgv


class Node(object):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __repr__(self):
        return str(self.__class__) + self.name

    def __str__(self):
        return self.name + "\n" + self.desc

    def color(self):
        raise NotImplementedError

    def shape(self):
        raise NotImplementedError


class HandleNode(Node):
    def __init__(self, name, desc):
        super(HandleNode, self).__init__(name, desc)

    def color(self):
        return "crimson"

    def shape(self):
        return "box"


class StructNode(Node):
    def __init__(self, name, desc):
        super(StructNode, self).__init__(name, desc)

    def color(self):
        return "forestgreen"

    def shape(self):
        return "ellipse"


class ElementNode(Node):
    def __init__(self, name, desc):
        super(ElementNode, self).__init__(name, desc)

    def color(self):
        return "navy"

    def shape(self):
        return "underline"


class CommandNode(Node):
    def __init__(self, name, desc):
        super(CommandNode, self).__init__(name, desc)

    def color(self):
        return "black"

    def shape(self):
        return "diamond"


def NodeFactory(name, BaseClass):
    assert isinstance(name, str)

    def __init__(self, desc):
        super(self.__class__, self).__init__(name, desc)

    return type(name, (BaseClass,), {"__init__": __init__})

_struct_nodes = [
    "VkImageCreateInfo",
    "VkImageViewCreateInfo",
    "VkBufferCreateInfo",
    "VkBufferViewCreateInfo",
    "VkDescriptorSetLayoutBinding",
    "VkDescriptorSetLayoutCreateInfo",
    "VkPipelineLayoutCreateInfo",
    "VkAttachmentReference",
    "VkAttachmentDescription",
    "VkSubpassDescription",
    "VkRenderPassCreateInfo",
    "VkFramebufferCreateInfo",
    "VkVertexBindingDescription",
    "VkVertexAttributeDescription",
    "VkPipelineVertexInputStateCreateInfo",
    "VkDescriptorPoolCreateInfo",
    "VkDescriptorSetAllocateInfo",
    "VkDescriptorBufferInfo",
    "VkWriteDescriptorSet",
    "VkRenderPassBeginInfo",
    "VkGraphicsPipelineCreateInfo",
]

_handle_nodes = [
    "VkDescriptorSetLayout",
    "VkPipelineLayout",
    "VkRenderPass",
    "VkImage",
    "VkImageView",
    "VkBuffer",
    "VkBufferView",
    "VkFramebuffer",
    "VkGraphicsPipeline",
    "VkDescriptorPool",
    "VkDescriptorSet",
]

_element_nodes = [
    "VkDescriptorType",
    "VkShaderStageFlags",
    "VkSampleCountFlagBits",
    "VkFormat",
]


_command_nodes = [
    "vkCmdBeginRenderPass",
    "vkCmdEndRenderPass",
    "vkCmdBindDescriptorSet",
    "vkCmdBindPipeline",
    "vkCmdDrawIndexed",
    "vkUpdateDescriptor",
]

for n in _struct_nodes:
    globals()[n] = NodeFactory(n, StructNode)
for n in _handle_nodes:
    globals()[n] = NodeFactory(n, HandleNode)
for n in _element_nodes:
    globals()[n] = NodeFactory(n, ElementNode)
for n in _command_nodes:
    globals()[n] = NodeFactory(n, CommandNode)


def build_graph(edge_list):
    assert isinstance(edge_list, list)
    G = pgv.AGraph(directed=True, strict=True)
    for e in edge_list:
        for item in e:
            if isinstance(item, Node):
                G.add_node(item, color=item.color(), shape=item.shape())
        if len(e) == 3:
            G.add_edge(e[0], e[1], **e[2])
        else:
            G.add_edge(e[0], e[1])
    return G


def write_graph(graph, output):
    assert isinstance(graph, pgv.AGraph)
    assert isinstance(output, str)
    graph.layout('dot')
    graph.draw(output)


class Styles:
    implicit_dep = {"style": "dashed"}
    implicit_match = {"style": "dashed", "arrowhead": "none"}
