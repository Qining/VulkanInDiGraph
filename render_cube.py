import sys
import os
from vulkan_node import *
from vulkan_node import EdgeStyles
from vulkan_node import NodeStyles

output_name = "render_cube.png"
edge_list = []

# cube rendering descriptor set layouts and pipeline layout
uniform_buffer_descriptor_type = VkDescriptorType("Uniform Buffer")
vertex_shader_stage_flag = VkShaderStageFlags("Vertex")
camera_binding = VkDescriptorSetLayoutBinding("Camera")
transform_binding = VkDescriptorSetLayoutBinding("Transform")
cube_descriptor_set_layout_create_info = VkDescriptorSetLayoutCreateInfo(
    "Cube Rendering")
cube_descriptor_set_layout = VkDescriptorSetLayout("Cube Rendering")
cube_pipeline_layout_create_info = VkPipelineLayoutCreateInfo("Cube Rendering")
cube_pipeline_layout = VkPipelineLayout("Cube Rendering")

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
cube_depth_attachment_ref = VkAttachmentReference("Depth at 0")
cube_color_attachment_ref = VkAttachmentReference("Color at 1")
cube_subpass_desc = VkSubpassDescription("Cube Rendering")
cube_sample_bit = VkSampleCountFlagBits("4 bits")
cube_depth_format = VkFormat("Depth format")
cube_depth_attachment_desc = VkAttachmentDescription("For Depth")
cube_color_attachment_desc = VkAttachmentDescription("For Color")
cube_color_format = VkFormat("Color format")
cube_render_pass_create_info = VkRenderPassCreateInfo("Cube Rendering")
cube_render_pass = VkRenderPass("Cube render pass")

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
    # implicit dependency between attachment reference and attachment desciption
    (cube_color_attachment_ref, cube_color_attachment_desc, EdgeStyles.implicit_match),
    (cube_depth_attachment_ref, cube_depth_attachment_desc, EdgeStyles.implicit_match),
    # Renderpass create info
    (cube_depth_attachment_desc, cube_render_pass_create_info),
    (cube_color_attachment_desc, cube_render_pass_create_info),
    (cube_subpass_desc, cube_render_pass_create_info),
    (cube_render_pass_create_info, cube_render_pass),
])

# Create framebuffer for cube rendering
cube_depth_image_create_info = VkImageCreateInfo("Cube Depth Image")
cube_color_image_create_info = VkImageCreateInfo("Cube Color Image")
cube_depth_image = VkImage("Cube Depth Image", NodeStyles.render_output)
cube_color_image = VkImage("Cube Color Image", NodeStyles.render_output)
cube_depth_view_create_info = VkImageViewCreateInfo("Cube Depth view")
cube_color_view_create_info = VkImageViewCreateInfo("Cube Color view")
cube_depth_view = VkImageView("Cube Depth view")
cube_color_view = VkImageView("Cube Color view")
cube_framebuffer_create_info = VkFramebufferCreateInfo(
    "Cube rendering framebuffer")
cube_framebuffer = VkFramebuffer("Cube rendering framebuffer")

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

    # implicit matches
    (cube_depth_image, cube_depth_attachment_desc, EdgeStyles.implicit_match),
    (cube_color_image, cube_color_attachment_desc, EdgeStyles.implicit_match),
])


# build pipeline for cube rendering
cube_vertex_binding_desc = VkVertexBindingDescription(
    "cube model vertex buffers")
cube_vertex_attribute_desc = VkVertexAttributeDescription(
    "cube model vertex info for each \'location\'")
cube_pipeline_vertex_input_state_create_info = VkPipelineVertexInputStateCreateInfo(
    "cube model vertex info")
cube_pipeline_create_info = VkGraphicsPipelineCreateInfo(
    "cube pipeline create info")
cube_pipeline = VkGraphicsPipeline("cube pipeline")
edge_list.extend([
    (cube_vertex_binding_desc, cube_pipeline_vertex_input_state_create_info),
    (cube_vertex_attribute_desc, cube_pipeline_layout_create_info),
    (cube_pipeline_vertex_input_state_create_info, cube_pipeline_create_info),
    (cube_pipeline_layout, cube_pipeline_create_info),
    (cube_pipeline_create_info, cube_pipeline),
])

# Allocate cube rendering descriptor sets and update the descriptor sets
cube_descriptor_pool_create_info = VkDescriptorPoolCreateInfo(
    "Cube descriptor pool")
cube_descriptor_pool = VkDescriptorPool("Cube descriptor pool")
cube_descriptor_set_allocate_info = VkDescriptorSetAllocateInfo(
    "Cube descriptor set")
cube_descriptor_set = VkDescriptorSet("Cube descriptor set")
camera_uniform_buffer = VkBuffer("Cube Rendering Camera data")
transform_uniform_buffer = VkBuffer("Cube Rendering Transform data")
camera_descriptor_buffer_info = VkDescriptorBufferInfo(
    "Cube descriptor buffer info: camera")
transform_descriptor_buffer_info = VkDescriptorBufferInfo(
    "Cube descriptor buffer info: transform")
cube_write_descriptor = VkWriteDescriptorSet("Cube descriptor set")
cube_update_descriptor = vkUpdateDescriptor("Cube descriptor")

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

    # implicit matches
    (camera_binding, camera_descriptor_buffer_info, EdgeStyles.implicit_match),
    (transform_binding, transform_descriptor_buffer_info, EdgeStyles.implicit_match),
])

# bind resources and draw cube
cube_render_pass_begin_info = VkRenderPassBeginInfo("Cube Rendering")
begin_cube_render_pass = vkCmdBeginRenderPass("Cube Rendering")
end_cube_render_pass = vkCmdEndRenderPass("Cube Rendering")
bind_cube_descriptor_set = vkCmdBindDescriptorSet("Cube Rendering")
bind_cube_pipeline = vkCmdBindPipeline("Cube Pipeline")
draw_cube = vkCmdDrawIndexed("Draw Cube")

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

if __name__ == "__main__":
    output_name = os.path.splitext(os.path.basename(sys.argv[0]))[0] + '.png'
    if len(sys.argv) > 1:
        output_name = sys.argv[1]
    g = build_graph(edge_list)
    write_graph(g, output_name)
