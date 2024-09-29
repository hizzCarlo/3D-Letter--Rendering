import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

# SHADERS GLSL
vertex_src = """
# version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;

uniform mat4 model;

out vec3 v_color;

void main()
{
    gl_Position = model * vec4(position, 1.0);
    v_color = color;
}
"""

fragment_src = """
# version 330

in vec3 v_color;

out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0);
}
"""

# window initialization

glfw.init()
window = glfw.create_window(800, 600, "MIDTERM PROJECT", None, None)

if not window:
    glfw.terminate()
    exit()

glfw.make_context_current(window)

# OBJECT CREATION
# HIZOLA, JOHN CARLO A.
H_vertices = [#front
                    -0.2, -0.25, 0.05, 1.0, 0.0, 0.0,
                       -0.2,  0.25, 0.05, 0.0, 1.0, 0.0,
                        -0.1,  0.25, 0.05, 0.0, 0.0, 1.0,
                        -0.1,  0.05, 0.05, 1.0, 1.0, 0.0,

                       0.1,  0.05, 0.05, 0.0, 1.0, 1.0,
                       0.1, 0.25, 0.05, 1.0, 0.0, 1.0,
                        0.2, 0.25, 0.05, 1.0, 0.0, 0.0,
                        0.2, -0.25, 0.05, 0.0, 1.0, 0.0,

                        0.1, -0.25, 0.05, 0.0, 0.0, 1.0,
                        0.1,  -0.05, 0.05, 1.0, 1.0, 0.0,
                        -0.1,  -0.05, 0.05, 0.0, 1.0, 1.0,
                        -0.1, -0.25, 0.05, 1.0, 0.0, 1.0,

                        # Back
                       -0.2, -0.25, -0.05, 1.0, 0.0, 0.0,
                       -0.2,  0.25, -0.05, 0.0, 1.0, 0.0,
                        -0.1,  0.25, -0.05, 0.0, 0.0, 1.0,
                        -0.1,  0.05, -0.05, 1.0, 1.0, 0.0,

                       0.1,  0.05, -0.05, 0.0, 1.0, 1.0,
                       0.1, 0.25, -0.05, 1.0, 0.0, 1.0,
                        0.2, 0.25, -0.05, 1.0, 0.0, 0.0,
                        0.2, -0.25, -0.05, 0.0, 1.0, 0.0,

                        0.1, -0.25, -0.05, 0.0, 0.0, 1.0,
                        0.1,  -0.05, -0.05, 1.0, 1.0, 0.0,
                        -0.1,  -0.05, -0.05, 0.0, 1.0, 1.0,
                        -0.1, -0.25, -0.05, 1.0, 0.0, 1.0]
                        #^ left and right
                                #^ up and down
                                        #^ near and far

H_indices = [
                    #front
                  0, 1, 11,
                  1, 2, 11,

                  5, 7, 8,
                  7, 5, 6,

                  3, 9, 4,
                  9, 3, 10,



                      #back
                  12, 23, 13,
                  14, 13, 23,

                  17, 19, 18,
                  17, 20, 19,

                  15, 16, 21,
                  22, 21, 15,

                    #top
                    1, 2, 13,
                    13, 2, 14,

                    5, 6, 17,
                    17, 6, 18,

                    3, 4, 16,
                    16, 3, 15,

                    #bot
                    0, 11, 12,
                    12, 11, 23,

                    8, 7, 20,
                    20, 7, 19,

                    10, 9, 22,
                    22, 9, 21,

                    #sides
                    2, 3, 15,
                    15, 2, 14,

                    10, 11, 23,
                    23, 10, 22,

                    9, 8, 20,
                    20, 9, 21,

                    0, 1, 12,
                    12, 1, 13,

                    5, 4, 17,
                    17, 4, 16,

                    6, 7, 19,
                    19, 6, 18]

# PAMINTUAN, XYRELL DAVE
P_vertices = [-0.2, 0.25, 0.05, 1.0, 0.0, 0.0,
            -0.2, 0.15, 0.05, 0.0, 1.0, 0.0,
            -0.2, -0.25, 0.05, 0.0, 0.0, 1.0,
            -0.1, -0.25, 0.05, 1.0, 1.0, 0.0,
            -0.1, -0.05, 0.05, 0.0, 1.0, 1.0,
            0.1, -0.05, 0.05, 1.0, 0.0, 1.0,
            0.2, 0.05, 0.05, 1.0, 0.0, 0.0,
            0.2, 0.15, 0.05, 0.0, 1.0, 0.0,
            0.1, 0.25, 0.05, 0.0, 0.0, 1.0,
            -0.1, 0.15, 0.05, 1.0, 1.0, 0.0,
            0.1, 0.15, 0.05, 0.0, 1.0, 1.0,
            -0.1, 0.05, 0.05, 1.0, 0.0, 1.0,
            0.1, 0.05, 0.05, 1.0, 0.0, 0.0,

            -0.2, 0.25, -0.05, 0.0, 1.0, 0.0,
            -0.2, 0.15, -0.05, 0.0, 0.0, 1.0,
            -0.2, -0.25, -0.05, 1.0, 1.0, 0.0,
            -0.1, -0.25, -0.05, 0.0, 1.0, 1.0,
            -0.1, -0.05, -0.05, 1.0, 0.0, 1.0,
            0.1, -0.05, -0.05, 1.0, 0.0, 0.0,
            0.2, 0.05, -0.05, 0.0, 1.0, 0.0,
            0.2, 0.15, -0.05, 0.0, 0.0, 1.0,
            0.1, 0.25, -0.05, 1.0, 1.0, 0.0,
            -0.1, 0.15, -0.05, 0.0, 1.0, 1.0,
            0.1, 0.15, -0.05, 1.0, 0.0, 1.0,
            -0.1, 0.05, -0.05, 1.0, 0.0, 0.0,
            0.1, 0.05, -0.05, 0.0, 1.0, 0.0]

# Indices for the letter "I" with horizontal bars and solid vertical
P_indices = [0, 8, 10, 0, 10, 1,
           1, 2, 3, 1, 3, 9,
           11, 4, 5, 11, 5, 12,
           5, 12, 6,
           10, 12, 6, 10, 6, 7,
           10, 8, 7,

           13, 21, 23, 13, 23, 14,
           14, 15, 16, 14, 16, 22,
           24, 17, 18, 24, 18, 25,
           18, 25, 19,
           23, 25, 19, 23, 19, 20,
           23, 21, 20,

           0, 13, 21, 0, 21, 8,
           8, 21, 20, 8, 20, 7,
           7, 20, 19, 7, 19, 6,
           6, 19, 18, 6, 18, 5,
           5, 18, 17, 5, 17, 4,
           4, 17, 16, 4, 16, 3,
           3, 16, 15, 3, 15, 2,
           2, 15, 13, 2, 13, 0,
           9, 22, 23, 9, 23, 10,
           10, 23, 25, 10, 25, 12,
           12, 25, 24, 12, 24, 11,
           11, 24, 22, 11, 22, 9]

# ROA CHRIS JEN IAN DAVA
R_vertices = [
    # Front face (outer outline)
    -0.2, 0.25, 0.05, 1.0, 0.0, 0.0,  # 0 (Red)
    0.2, 0.25, 0.05, 0.0, 1.0, 0.0,  # 1 (Green)
    0.2, -0.05, 0.05, 0.0, 0.0, 1.0,  # 2 (Blue)
    0.0, -0.05, 0.05, 1.0, 1.0, 0.0,  # 3 (Yellow)
    0.1, -0.25, 0.05, 0.0, 1.0, 1.0,  # 4 (Cyan)
    0.0, -0.25, 0.05, 1.0, 0.0, 1.0,  # 5 (Magenta)
    -0.1, -0.05, 0.05, 1.0, 0.0, 0.0,  # 6 (Red)
    -0.1, -0.25, 0.05, 0.0, 1.0, 0.0,  # 7 (Green)
    -0.2, -0.25, 0.05, 0.0, 0.0, 1.0,  # 8 (Blue)
    -0.1, 0.15, 0.05, 1.0, 1.0, 0.0,  # 9 (Yellow)
    0.1, 0.15, 0.05, 0.0, 1.0, 1.0,  # 10 (Cyan)
    -0.1, 0.05, 0.05, 1.0, 0.0, 1.0,  # 11 (Magenta)
    0.1, 0.05, 0.05, 1.0, 0.0, 0.0,  # 12 (Red)

    # Back face (outer outline)
    -0.2, 0.25, -0.05, 1.0, 0.0, 0.0,  # 0 (Red)
    0.2, 0.25, -0.05, 0.0, 1.0, 0.0,  # 1 (Green)
    0.2, -0.05, -0.05, 0.0, 0.0, 1.0,  # 2 (Blue)
    0.0, -0.05, -0.05, 1.0, 1.0, 0.0,  # 3 (Yellow)
    0.1, -0.25, -0.05, 0.0, 1.0, 1.0,  # 4 (Cyan)
    0.0, -0.25, -0.05, 1.0, 0.0, 1.0,  # 5 (Magenta)
    -0.1, -0.05, -0.05, 1.0, 0.0, 0.0,  # 6 (Red)
    -0.1, -0.25, -0.05, 0.0, 1.0, 0.0,  # 7 (Green)
    -0.2, -0.25, -0.05, 0.0, 0.0, 1.0,  # 8 (Blue)
    -0.1, 0.15, -0.05, 1.0, 1.0, 0.0,  # 9 (Yellow)
    0.1, 0.15, -0.05, 0.0, 1.0, 1.0,  # 10 (Cyan)
    -0.1, 0.05, -0.05, 1.0, 0.0, 1.0,  # 11 (Magenta)
    0.1, 0.05, -0.05, 1.0, 0.0, 0.0,  # 12 (Red)
]

R_indices = [
    # Front View
    0, 1, 9, 1, 9, 10,
    10, 1, 12, 12, 1, 2,
    2, 12, 3, 3, 11, 12,
    3, 11, 6, 3, 6, 5,
    3, 5, 4, 9, 7, 8,
    0, 9, 8,

    # Back View
    13, 14, 22, 14, 22, 23,
    23, 14, 25, 25, 14, 15,
    15, 25, 16, 16, 24, 25,
    16, 24, 19, 16, 19, 18,
    16, 18, 17, 22, 20, 21,
    13, 22, 21,

    # Side
    0, 1, 13, 13, 14, 1,
    1, 2, 14, 14, 15, 2,
    3, 2, 15, 15, 16, 3,
    3, 4, 16, 16, 17, 4,
    4, 5, 17, 17, 18, 5,
    5, 6, 18, 18, 19, 6,
    6, 7, 19, 19, 20, 7,
    7, 8, 20, 20, 21, 8,
    9, 10, 22, 22, 23, 10,
    10, 12, 23, 23, 25, 12,
    11, 12, 24, 24, 25, 12,
    9, 11, 22, 22, 24, 11,
    0, 8, 13, 13, 21, 8,
]

# TRIUMFANTE, JAMES LEE MANALANSAN
T_vertices = [
    # Front face (outer outline)
    -0.25, 0.25, 0.05, 1.0, 0.0, 0.0,  # 0 (Red)
    0.25, 0.25, 0.05, 0.0, 1.0, 0.0,  # 1 (Green)
    0.25, 0.15, 0.05, 0.0, 0.0, 1.0,  # 2 (Blue)
    0.05, 0.15, 0.05, 1.0, 1.0, 0.0,  # 3 (Yellow)
    0.05, -0.25, 0.05, 0.0, 1.0, 1.0,  # 4 (Cyan)
    -0.05, -0.25, 0.05, 1.0, 0.0, 1.0,  # 5 (Magenta)
    -0.05, 0.15, 0.05, 1.0, 0.0, 0.0,  # 6 (Red)
    -0.25, 0.15, 0.05, 0.0, 1.0, 0.0,  # 7 (Green)

    # Back face (outer outline)
    -0.25, 0.25, -0.05, 1.0, 0.0, 0.0,  # 8 (Red)
    0.25, 0.25, -0.05, 0.0, 1.0, 0.0,  # 9 (Green)
    0.25, 0.15, -0.05, 0.0, 0.0, 1.0,  # 10 (Blue)
    0.05, 0.15, -0.05, 1.0, 1.0, 0.0,  # 11 (Yellow)
    0.05, -0.25, -0.05, 0.0, 1.0, 1.0,  # 12 (Cyan)
    -0.05, -0.25, -0.05, 1.0, 0.0, 1.0,  # 13 (Magenta)
    -0.05, 0.15, -0.05, 1.0, 0.0, 0.0,  # 14 (Red)
    -0.25, 0.15, -0.05, 0.0, 1.0, 0.0,  # 15 (Green)
]

T_indices = [
    # front
    0, 1, 2,
    0, 2, 7,
    3, 4, 5,
    3, 5, 6,

    # back
    8, 9, 10,
    8, 10, 15,
    11, 12, 13,
    11, 13, 14,

    # edges
    0, 1, 8,
    8, 9, 1,
    1, 2, 9,
    9, 10, 2,
    2, 3, 10,
    10, 11, 3,
    3, 4, 11,
    11, 12, 4,
    4, 5, 12,
    12, 13, 5,
    5, 6, 13,
    13, 14, 6,
    6, 7, 14,
    14, 15, 7,
    0, 7, 8,
    8, 15, 7,

]

H_vertices = np.array(H_vertices, dtype=np.float32)
H_indices = np.array(H_indices, dtype=np.uint32)
P_vertices = np.array(P_vertices, dtype=np.float32)
P_indices = np.array(P_indices, dtype=np.uint32)
R_vertices = np.array(R_vertices, dtype=np.float32)
R_indices = np.array(R_indices, dtype=np.uint32)
T_vertices = np.array(T_vertices, dtype=np.float32)
T_indices = np.array(T_indices, dtype=np.uint32)
# vertex definition

# triangle creation by indexing method

# SENDING DATA
# vao
H_vao = glGenVertexArrays(1)
glBindVertexArray(H_vao)

# vbo
H_vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, H_vbo)
glBufferData(GL_ARRAY_BUFFER, H_vertices.nbytes, H_vertices, GL_STATIC_DRAW)

# ebo
H_ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, H_ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, H_indices.nbytes, H_indices, GL_STATIC_DRAW)

# position
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

# color
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

# TRANSFORMATION
# translation
H_translation = pyrr.Matrix44.from_translation([-0.5, 0.5, 0])

# vao
P_vao = glGenVertexArrays(1)
glBindVertexArray(P_vao)

# vbo
P_vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, P_vbo)
glBufferData(GL_ARRAY_BUFFER, P_vertices.nbytes, P_vertices, GL_STATIC_DRAW)

# ebo
P_ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, P_ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, P_indices.nbytes, P_indices, GL_STATIC_DRAW)

# position
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

# color
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

# TRANSFORMATION
# translation
P_translation = pyrr.Matrix44.from_translation([0.5, 0.5, 0])

# vao
R_vao = glGenVertexArrays(1)
glBindVertexArray(R_vao)

# vbo
R_vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, R_vbo)
glBufferData(GL_ARRAY_BUFFER, R_vertices.nbytes, R_vertices, GL_STATIC_DRAW)

# ebo
R_ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, R_ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, R_indices.nbytes, R_indices, GL_STATIC_DRAW)

# position
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

# color
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

# TRANSFORMATION
# translation
R_translation = pyrr.Matrix44.from_translation([-0.5, -0.5, 0])

# vao
T_vao = glGenVertexArrays(1)
glBindVertexArray(T_vao)

# vbo
T_vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, T_vbo)
glBufferData(GL_ARRAY_BUFFER, T_vertices.nbytes, T_vertices, GL_STATIC_DRAW)
# ebo

T_ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, T_ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, T_indices.nbytes, T_indices, GL_STATIC_DRAW)

# position
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

# color
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

# TRANSFORMATION
# translation
T_translation = pyrr.Matrix44.from_translation([0.5, -0.5, 0])

# rotation
degree = 30
rot_x = pyrr.Matrix44.from_x_rotation(np.radians(degree))
degree1 = 30
rot_y = pyrr.Matrix44.from_y_rotation(np.radians(degree1))
# scaling
scale = pyrr.Matrix44.from_scale(pyrr.Vector3([1, 1, 1]))

# SHADER SPACE
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
glUseProgram(shader)

model_loc = glGetUniformLocation(shader, "model")

# RENDERING SPACE
# set up the color for background
glClearColor(0.1, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)  # activate the z-buffer
while not glfw.window_should_close(window):
    glfw.poll_events()  # get the events happening in the window
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # OBJECT TRANSFORMATION
    # HIZOLA, JOHN CARLO ARCEO
    H_rot_y = pyrr.Matrix44.from_y_rotation(np.radians(20 * glfw.get_time()))
    H_model = pyrr.matrix44.multiply(scale, H_rot_y)
    H_model = pyrr.matrix44.multiply(H_model, H_translation)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, H_model)
    # OBJECT ASSEMBLY AND RENDERING
    glBindVertexArray(H_vao)
    glDrawElements(GL_TRIANGLES, len(H_indices), GL_UNSIGNED_INT, None)

    # PAMINTUAN, XYRELL DAVE
    P_rot_y = pyrr.Matrix44.from_y_rotation(np.radians(20 * glfw.get_time()))
    P_model = pyrr.matrix44.multiply(scale, P_rot_y)
    P_model = pyrr.matrix44.multiply(P_model, P_translation)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, P_model)
    # OBJECT ASSEMBLY AND RENDERING
    glBindVertexArray(P_vao)
    glDrawElements(GL_TRIANGLES, len(P_indices), GL_UNSIGNED_INT, None)

    # ROA CHRIS JEN IAN DAVA
    R_rot_y = pyrr.Matrix44.from_y_rotation(np.radians(18 * glfw.get_time()))
    R_model = pyrr.matrix44.multiply(scale, R_rot_y)
    R_model = pyrr.matrix44.multiply(R_model, R_translation)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, R_model)
    # OBJECT ASSEMBLY AND RENDERING
    glBindVertexArray(R_vao)
    glDrawElements(GL_TRIANGLES, len(R_indices), GL_UNSIGNED_INT, None)

    # TRIUMFANTE, JAMES LEE MANALANSAN
    T_rot_y = pyrr.Matrix44.from_y_rotation(np.radians(28 * glfw.get_time()))
    T_model = pyrr.matrix44.multiply(scale, T_rot_y)
    T_model = pyrr.matrix44.multiply(T_model, T_translation)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, T_model)
    # OBJECT ASSEMBLY AND RENDERING
    glBindVertexArray(T_vao)
    glDrawElements(GL_TRIANGLES, len(T_indices), GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)

# CLEARING
glDeleteBuffers(2, [H_vbo, H_ebo, ])
glDeleteVertexArrays(1, [H_vao, ])
glDeleteBuffers(2, [P_vbo, P_ebo, ])
glDeleteVertexArrays(1, [P_vao, ])
glDeleteBuffers(2, [R_vbo, R_ebo, ])
glDeleteVertexArrays(1, [R_vao, ])
glDeleteBuffers(2, [T_vbo, T_ebo, ])
glDeleteVertexArrays(1, [T_vao, ])
glfw.terminate()