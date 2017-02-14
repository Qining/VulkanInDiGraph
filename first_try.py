import pygraphviz as pgv
import sys
from vulkan_node import Node, StructNode, HandleNode, ElementNode, CommandNode

output_name = "first_try.png"
edge_list = []

# cube rendering descriptor set layouts and pipeline layout
uniform_buffer_descriptor_type = ElementNode("VkDescriptorType",
                                             "Uniform Buffer")
vertex_shader_stage_flag = ElementNode("VkShaderStageFlags", "Vertex")
camera_binding = StructNode("VkDescriptorSetLayoutBinding", "Camera")
transform_binding = StructNode("VkDescriptorSetLayoutBinding", "Transform")
cube_descriptor_set_layout_create_info = StructNode(
    "VkDescriptorSetLayoutCreateInfo", "Cube Rendering")
cube_descriptor_set_layout = HandleNode("VkDescriptorSetLayout",
                                        "Cube Rendering")
cube_pipeline_layout_create_info = StructNode("VkPipelineLayoutCreateInfo",
                                              "Cube Rendering")
cube_pipeline_layout = HandleNode("VkPipelineLayout", "Cube Rendering")

edge_list.extend([
    (uniform_buffer_descriptor_type, camera_binding),
    (vertex_shader_stage_flag, camera_binding),
    (uniform_buffer_descriptor_type, transform_binding),
    (vertex_shader_stage_flag, transform_binding),
    (camera_binding, cube_descriptor_set_layout_create_info),
    (transform_binding, cube_descriptor_set_layout_create_info),
    (cube_descriptor_set_layout_create_info, cube_descriptor_set_layout),
    (cube_descriptor_set_layout, cube_pipeline_layout_create_info),
    (cube_pipeline_layout_create_info, cube_pipeline_layout),
])

# Create render pass for cube rendering
cube_depth_attachment_ref = StructNode("VkAttachmentReference", "Depth at 0")
cube_color_attachment_ref = StructNode("VkAttachmentReference", "Color at 1")
cube_subpass_desc = StructNode("VkSubpassDescription", "Cube Rendering")
cube_sample_bit = StructNode("VkSampleCountFlagBits", "4 bits")
cube_depth_format = ElementNode("VkFormat", "Depth format")
cube_depth_attachment_desc = StructNode("VkAttachmentDescription", "For Depth")
cube_color_attachment_desc = StructNode("VkAttachmentDescription", "For Color")
cube_color_format = ElementNode("VkFormat", "Color format")
cube_render_pass_create_info = StructNode("VkRenderPassCreateInfo",
                                          "Cube Rendering")
cube_render_pass = HandleNode("VkRenderPass", "Cube render pass")

edge_list.extend([
    # subpass description
    (cube_color_attachment_ref, cube_subpass_desc),
    (cube_depth_attachment_ref, cube_subpass_desc),
    # depth attachment description
    (cube_sample_bit, cube_depth_attachment_desc),
    (cube_depth_format, cube_depth_attachment_desc),
    # color attachment description
    (cube_sample_bit, cube_color_attachment_desc),
    (cube_color_format, cube_color_attachment_desc),
    # Renderpass create info
    (cube_depth_attachment_desc, cube_render_pass_create_info),
    (cube_color_attachment_desc, cube_render_pass_create_info),
    (cube_subpass_desc, cube_render_pass_create_info),
    (cube_render_pass_create_info, cube_render_pass),
])

# Create framebuffer for cube rendering
cube_depth_image_create_info = StructNode("VkImageCreateInfo",
                                          "Cube Depth Image")
cube_color_image_create_info = StructNode("VkImageCreateInfo",
                                          "Cube Color Image")
cube_depth_image = HandleNode("VkImage", "Cube Depth Image")
cube_color_image = HandleNode("VkImage", "Cube Color Image")
cube_depth_view_create_info = StructNode("VkImageViewCreateInfo",
                                         "Cube Depth view")
cube_color_view_create_info = StructNode("VkImageViewCreateInfo",
                                         "Cube Color view")
cube_depth_view = HandleNode("VkImageView", "Cube Depth view")
cube_color_view = HandleNode("VkImageView", "Cube Color view")
cube_framebuffer_create_info = StructNode("VkFramebufferCreateInfo",
                                          "Cube rendering framebuffer")
cube_framebuffer = HandleNode("VkFramebuffer", "Cube rendering framebuffer")

edge_list.extend([
    (cube_depth_format, cube_depth_image_create_info),
    (cube_sample_bit, cube_depth_image_create_info),
    (cube_color_format, cube_color_image_create_info),
    (cube_sample_bit, cube_color_image_create_info),
    (cube_depth_image_create_info, cube_depth_image),
    (cube_color_image_create_info, cube_color_image),
    (cube_depth_format, cube_depth_view_create_info),
    (cube_depth_image, cube_depth_view_create_info),
    (cube_color_format, cube_color_view_create_info),
    (cube_color_image, cube_color_view_create_info),
    (cube_depth_view_create_info, cube_depth_view),
    (cube_color_view_create_info, cube_color_view),
    (cube_render_pass, cube_framebuffer_create_info),
    (cube_depth_view, cube_framebuffer_create_info),
    (cube_color_view, cube_framebuffer_create_info),
    (cube_framebuffer_create_info, cube_framebuffer),
])

# build pipeline for cube rendering
cube_vertex_binding_desc = StructNode("VkVertexBindingDescription",
                                      "cube model vertex buffers")
cube_vertex_attribute_desc = StructNode(
    "VkVertexAttributeDescription",
    "cube model vertex info for each \'location\'")
cube_pipeline_vertex_input_state_create_info = StructNode(
    "VkPipelineVertexInputStateCreateInfo", "cube model vertex info")
cube_pipeline_create_info = StructNode("VkGraphicsPipelineCreateInfo",
                                       "cube pipeline create info")
cube_pipeline = HandleNode("VkGraphicsPipeline", "cube pipeline")
edge_list.extend([
    (cube_vertex_binding_desc, cube_pipeline_vertex_input_state_create_info),
    (cube_vertex_attribute_desc, cube_pipeline_layout_create_info),
    (cube_pipeline_vertex_input_state_create_info, cube_pipeline_create_info),
    (cube_pipeline_layout, cube_pipeline_create_info),
    (cube_pipeline_create_info, cube_pipeline),
])

# Allocate cube rendering descriptor sets and update the descriptor sets
cube_descriptor_pool_create_info = StructNode("VkDescriptorPoolCreateInfo",
                                              "Cube descriptor pool")
cube_descriptor_pool = HandleNode("VkDescriptorPool", "Cube descriptor pool")
cube_descriptor_set_allocate_info = StructNode("VkDescriptorSetAllocateInfo",
                                               "Cube descriptor set")
cube_descriptor_set = HandleNode("VkDescriptorSet", "Cube descriptor set")
camera_uniform_buffer = HandleNode("VkBuffer", "Cube Rendering Camera data")
transform_uniform_buffer = HandleNode("VkBuffer",
                                      "Cube Rendering Transform data")
camera_descriptor_buffer_info = StructNode(
    "VkDescriptorBufferInfo", "Cube descriptor buffer info: camera")
transform_descriptor_buffer_info = StructNode(
    "VkDescriptorBufferInfo", "Cube descriptor buffer info: transform")
cube_write_descriptor = StructNode("VkWriteDescriptorSet",
                                   "Cube descriptor set")
cube_update_descriptor = CommandNode("vkUpdateDescriptor", "Cube descriptor")

edge_list.extend([
    (cube_descriptor_pool_create_info, cube_descriptor_pool),
    (cube_descriptor_pool, cube_descriptor_set_allocate_info),
    (cube_descriptor_set_layout, cube_descriptor_set_allocate_info),
    (cube_descriptor_set_allocate_info, cube_descriptor_set),
    (cube_descriptor_set, cube_write_descriptor),
    (camera_uniform_buffer, camera_descriptor_buffer_info),
    (transform_uniform_buffer, transform_descriptor_buffer_info),
    (camera_descriptor_buffer_info, cube_write_descriptor),
    (transform_descriptor_buffer_info, cube_write_descriptor),
    (cube_write_descriptor, cube_update_descriptor),
])

# bind resources and draw cube
cube_render_pass_begin_info = StructNode("VkRenderPassBeginInfo",
                                         "Cube Rendering")
begin_cube_render_pass = CommandNode("vkCmdBeginRenderPass", "Cube Rendering")
end_cube_render_pass = CommandNode("vkCmdEndRenderPass", "Cube Rendering")
bind_cube_descriptor_set = CommandNode("vkCmdBindDescriptorSet",
                                       "Cube Rendering")
bind_cube_pipeline = CommandNode("vkCmdBindPipeline", "Cube Pipeline")
draw_cube = CommandNode("vkCmdDrawIndexed", "Draw Cube")

edge_list.extend([
    (cube_framebuffer, cube_render_pass_begin_info),
    (cube_render_pass, cube_render_pass_begin_info),
    (cube_render_pass_begin_info, begin_cube_render_pass),
    (begin_cube_render_pass, draw_cube),
    (cube_update_descriptor, bind_cube_descriptor_set),
    (bind_cube_descriptor_set, draw_cube),
    (cube_pipeline, bind_cube_pipeline),
    (bind_cube_pipeline, draw_cube),
    (draw_cube, end_cube_render_pass),
])


def build_graph(edge_list):
    assert isinstance(edge_list, list)
    G = pgv.AGraph(directed=True, strict=True)
    for e in edge_list:
        for item in e:
            if isinstance(item, Node):
                G.add_node(item, color=item.color())
        G.add_edge(e[0], e[1])
    return G


def write_graph(graph, output):
    assert isinstance(graph, pgv.AGraph)
    assert isinstance(output, str)
    graph.layout('dot')
    graph.draw(output)


if len(sys.argv) > 1:
    output_name = sys.argv[1]
g = build_graph(edge_list)
write_graph(g, output_name)
