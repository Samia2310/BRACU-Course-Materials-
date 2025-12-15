#TASK1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

rain_bend = 0.0
rain_target_bend = 0.0
RAIN_BEND_CHANGE_RATE = 0.5
RAIN_BEND_SMOOTH_SPEED = 0.05

background_color_r = 0.0
background_color_g = 0.0
background_color_b = 0.0
DAY_NIGHT_CHANGE_RATE = 0.0030
day_night_current_target = 0.0

num_raindrops = 80
raindrops = []

def init_raindrops():
    global raindrops
    raindrops = []
    for _ in range(num_raindrops):
        x = random.uniform(-200, 1200 + 200)
        y = random.uniform(600, 1000)
        speed = random.uniform(4, 9)
        drop_type = random.choices([0, 1, 2], weights=[70, 10, 20], k=1)[0]
        raindrops.append({'x': x, 'y': y, 'speed': speed, 'type': drop_type})

def iterate():
    glViewport(0, 0, 1200, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1200.0, 0.0, 800.0, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def update_day_night_smoothly(value):
    global background_color_r, background_color_g, background_color_b, day_night_current_target, DAY_NIGHT_CHANGE_RATE

    step = DAY_NIGHT_CHANGE_RATE
    if day_night_current_target < background_color_r:
        step = -step

    background_color_r += step
    background_color_g += step
    background_color_b += step

    if step > 0:
        background_color_r = min(day_night_current_target, background_color_r)
        background_color_g = min(day_night_current_target, background_color_g)
        background_color_b = min(day_night_current_target, background_color_b)
    else:
        background_color_r = max(day_night_current_target, background_color_r)
        background_color_g = max(day_night_current_target, background_color_g)
        background_color_b = max(day_night_current_target, background_color_b)

    glutPostRedisplay()
    glutTimerFunc(10, update_day_night_smoothly, 0)

def update_rain_bend_smoothly(value):
    global rain_bend, rain_target_bend, RAIN_BEND_SMOOTH_SPEED

    if abs(rain_bend - rain_target_bend) > RAIN_BEND_SMOOTH_SPEED:
        if rain_bend < rain_target_bend:
            rain_bend += RAIN_BEND_SMOOTH_SPEED
        elif rain_bend > rain_target_bend:
            rain_bend -= RAIN_BEND_SMOOTH_SPEED
    else:
        rain_bend = rain_target_bend

    glutPostRedisplay()
    glutTimerFunc(10, update_rain_bend_smoothly, 0)

def keyboardListener(key, x, y):
    global day_night_current_target
    if key == b'd':
        day_night_current_target = 1.0
    elif key == b'n':
        day_night_current_target = 0.0
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global rain_target_bend, RAIN_BEND_CHANGE_RATE
    if key == GLUT_KEY_LEFT:
        rain_target_bend = max(-15.0, rain_target_bend - RAIN_BEND_CHANGE_RATE)
    elif key == GLUT_KEY_RIGHT:
        rain_target_bend = min(15.0, rain_target_bend + RAIN_BEND_CHANGE_RATE)
    glutPostRedisplay()

def showScreen():
    global background_color_r, background_color_g, background_color_b, rain_bend, raindrops

    glClearColor(background_color_r, background_color_g, background_color_b, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    ground_height = 400
    glColor3f(0.435, 0.282, 0.078)
    glBegin(GL_TRIANGLES)
    glVertex2f(0, 0)
    glVertex2f(1200, 0)
    glVertex2f(1200, ground_height)
    glVertex2f(0, 0)
    glVertex2f(0, ground_height)
    glVertex2f(1200, ground_height)
    glEnd()

    tree_base_y = ground_height - 75
    tree_peak_y = tree_base_y + 60

    for i in range(-50, 1200 + 50, 50):
      glBegin(GL_TRIANGLES)
      glColor3f(0.4, 0.2, 0.1)
      glVertex2f(i + 25, tree_peak_y) 

      glColor3f(0.1, 0.8, 0.1)
      glVertex2f(i, tree_base_y)

      glColor3f(0.1, 1, 0.1)
      glVertex2f(i + 50, tree_base_y)
      glEnd()

    house_width = 400
    house_height = 130
    house_base_y = ground_height - 195
    house_center_x = 1200 / 2
    house_x_start = house_center_x - (house_width / 2)
    house_x_end = house_center_x + (house_width / 2)
    house_y_top = house_base_y + house_height

    glColor3f(1.0, 0.9, 0.8)
    glBegin(GL_TRIANGLES)
    glVertex2f(house_x_start, house_base_y)
    glVertex2f(house_x_end, house_base_y)
    glVertex2f(house_x_end, house_y_top)
    glVertex2f(house_x_start, house_base_y)
    glVertex2f(house_x_end, house_y_top)
    glVertex2f(house_x_start, house_y_top)
    glEnd()

    roof_base_y = house_y_top
    roof_x_left = house_x_start - 25
    roof_x_right = house_x_end + 25
    roof_apex_x = house_center_x
    roof_apex_y = roof_base_y + 100

    glColor3f(0.3, 0.2, 0.7)
    glBegin(GL_TRIANGLES)
    glVertex2f(roof_x_left, roof_base_y)
    glVertex2f(roof_x_right, roof_base_y)
    glVertex2f(roof_apex_x, roof_apex_y)
    glEnd()

    door_width = 50
    door_height = 80
    door_x_start = house_center_x - (door_width / 2)
    door_y_start = house_base_y
    door_x_end = house_center_x + (door_width / 2)
    door_y_end = door_y_start + door_height

    glColor3f(0.080, 0.50, 0.9)
    glBegin(GL_TRIANGLES)
    glVertex2f(door_x_start, door_y_start)
    glVertex2f(door_x_end, door_y_start)
    glVertex2f(door_x_end, door_y_end)
    glVertex2f(door_x_start, door_y_start)
    glVertex2f(door_x_end, door_y_end)
    glVertex2f(door_x_start, door_y_end)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(door_x_end - 15, door_y_start + (door_height / 2))
    glEnd()

    window_offset_x = 90
    window_size = 50
    window_y_pos = house_base_y + 50

    window_x_left = house_center_x - window_offset_x - (window_size / 2)
    window_x_right = house_center_x + window_offset_x - (window_size / 2)

    glColor3f(0.080, 0.50, 0.9)
    glBegin(GL_TRIANGLES)
    glVertex2f(window_x_left, window_y_pos)
    glVertex2f(window_x_left + window_size, window_y_pos)
    glVertex2f(window_x_left + window_size, window_y_pos + window_size)
    glVertex2f(window_x_left, window_y_pos)
    glVertex2f(window_x_left + window_size, window_y_pos + window_size)
    glVertex2f(window_x_left, window_y_pos + window_size)
    glEnd()
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(window_x_left + window_size/2, window_y_pos)
    glVertex2f(window_x_left + window_size/2, window_y_pos + window_size)
    glVertex2f(window_x_left, window_y_pos + window_size/2)
    glVertex2f(window_x_left + window_size, window_y_pos + window_size/2)
    glEnd()

    glColor3f(0.080, 0.50, 0.9)
    glBegin(GL_TRIANGLES)
    glVertex2f(window_x_right, window_y_pos)
    glVertex2f(window_x_right + window_size, window_y_pos)
    glVertex2f(window_x_right + window_size, window_y_pos + window_size)
    glVertex2f(window_x_right, window_y_pos)
    glVertex2f(window_x_right + window_size, window_y_pos + window_size)
    glVertex2f(window_x_right, window_y_pos + window_size)
    glEnd()
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(window_x_right + window_size/2, window_y_pos)
    glVertex2f(window_x_right + window_size/2, window_y_pos + window_size)
    glVertex2f(window_x_right, window_y_pos + window_size/2)
    glVertex2f(window_x_right + window_size, window_y_pos + window_size/2)
    glEnd()

    rain_line_length = 35

    glBegin(GL_LINES)
    for drop in raindrops:
        drop['y'] -= drop['speed']
        drop['x'] += rain_bend * 0.1

        re_spawn_x_min = -200
        re_spawn_x_max = 1200 + 200
        re_spawn_y_min = -rain_line_length

        if drop['y'] < re_spawn_y_min or drop['x'] < re_spawn_x_min or drop['x'] > re_spawn_x_max:
            drop['y'] = random.uniform(600, 800)

            horizontal_compensation = abs(rain_bend) * 15
            spawn_x_start = 0 - horizontal_compensation
            spawn_x_end = 1200 + horizontal_compensation
            spawn_x_start = max(-500, spawn_x_start)
            spawn_x_end = min(1200 + 500, spawn_x_end)
            drop['x'] = random.uniform(spawn_x_start, spawn_x_end)

            drop['type'] = random.choices([0, 1, 2], weights=[70, 10, 20], k=1)[0]

        if drop['type'] == 1:
            glColor3f(0.6, 0.4, 0.2)
        elif drop['type'] == 2:
            glColor3f(random.uniform(0.0, 0.4), random.uniform(0.5, 0.8), random.uniform(0.7, 1.0))
        else:
            glColor3f(0.5, 0.7, 1.0)

        glVertex2f(drop['x'], drop['y'])
        glVertex2f(drop['x'] + rain_bend * 5, drop['y'] + rain_line_length)
    glEnd()

    glutSwapBuffers()

init_raindrops()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(1200, 600)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Assignment 1 Task 1")

glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)

glutTimerFunc(10, update_rain_bend_smoothly, 0)
glutTimerFunc(10, update_day_night_smoothly, 0)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)

glutMainLoop()





















#TASK2

# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random
# import math

# screenWidth, screenHeight = 1300, 650
# all_points = []
# base_speed = 5
# speed_multiplier = 1.0
# min_speed_multiplier = 0.1
# max_speed_multiplier = 70.0
# point_radius = 3
# is_paused = False
# blinkingStatus = False
# blink_state = True 
# last_frame_time = 0
# last_blink_time = 0

# X_MIN, X_MAX = -screenWidth / 2, screenWidth / 2
# Y_MIN, Y_MAX = -screenHeight / 2, screenHeight / 2

# def convert_coordinate(x, y):
#     return x - (screenWidth / 2), (screenHeight / 2) - y

# def get_random_color():
#     return (random.random(), random.random(), random.random())

# def draw_square(x, y, size):
#     half_size = size / 2.0
#     glBegin(GL_QUADS)
#     glVertex2f(x - half_size, y - half_size)
#     glVertex2f(x + half_size, y - half_size)
#     glVertex2f(x + half_size, y + half_size)
#     glVertex2f(x - half_size, y + half_size)
#     glEnd()

# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.color = get_random_color()
#         self.dx = (1 if random.random() < 0.5 else -1) * base_speed
#         self.dy = (1 if random.random() < 0.5 else -1) * base_speed
#         self.speed = math.hypot(self.dx, self.dy)
#         self.radius = max(3, min(10, self.speed * 0.8))

#     def draw(self):
#         if blinkingStatus and not blink_state:
#             glColor3f(0.0, 0.0, 0.0)  
#         else:
#             glColor3f(*self.color)
#         draw_square(self.x, self.y, self.radius)

#     def update(self, delta_time_ms, current_speed_multiplier):
#         move_factor = (delta_time_ms / 16.66) * current_speed_multiplier
#         self.x += self.dx * move_factor
#         self.y += self.dy * move_factor

#         if self.x + self.radius / 2 > X_MAX:
#             self.x = X_MAX - self.radius / 2
#             self.dx *= -1
#         elif self.x - self.radius / 2 < X_MIN:
#             self.x = X_MIN + self.radius / 2
#             self.dx *= -1

#         if self.y + self.radius / 2 > Y_MAX:
#             self.y = Y_MAX - self.radius / 2
#             self.dy *= -1
#         elif self.y - self.radius / 2 < Y_MIN:
#             self.y = Y_MIN + self.radius / 2
#             self.dy *= -1

# def display():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glClearColor(0.0, 0.0, 0.0, 0.0)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()

#     for point in all_points:
#         point.draw()

#     glutSwapBuffers()

# def animate():
#     global last_frame_time, last_blink_time, blink_state

#     current_time_ms = glutGet(GLUT_ELAPSED_TIME)
#     delta_time_ms = current_time_ms - last_frame_time
#     last_frame_time = current_time_ms

#     if not is_paused:
#         if blinkingStatus and (current_time_ms - last_blink_time >= 500):
#             blink_state = not blink_state
#             last_blink_time = current_time_ms

#         for point in all_points:
#             point.update(delta_time_ms, speed_multiplier)

#     glutPostRedisplay()

# def keyboardListener(key, x, y):
#     global is_paused

#     if key == b' ':
#         is_paused = not is_paused
#         print("Paused" if is_paused else "Resumed")

#     glutPostRedisplay()

# def specialKeyListener(key, x, y):
#     global speed_multiplier

#     if not is_paused:
#         if key == GLUT_KEY_UP:
#             speed_multiplier = min(speed_multiplier + 0.1, max_speed_multiplier)
#             print(f"Speed Increased: {speed_multiplier:.1f}x")
#         elif key == GLUT_KEY_DOWN:
#             speed_multiplier = max(speed_multiplier - 0.1, min_speed_multiplier)
#             print(f"Speed Decreased: {speed_multiplier:.1f}x")
#     else:
#         print("Paused. Cannot change speed.")

#     glutPostRedisplay()

# def mouseListener(button, state, x, y):
#     global blinkingStatus

#     if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
#         if not is_paused:
#             gl_x, gl_y = convert_coordinate(x, y)
#             all_points.append(Point(gl_x, gl_y))
#             print(f"New point at ({gl_x:.2f}, {gl_y:.2f})")
#         else:
#             print("Paused. Cannot add point.")

#     elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
#         if not is_paused:
#             blinkingStatus = not blinkingStatus
#             print("Blinking status:", blinkingStatus)

#     glutPostRedisplay()

# def init():
#     glClearColor(0, 0, 0, 0)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluOrtho2D(-screenWidth / 2, screenWidth / 2, -screenHeight / 2, screenHeight / 2)
#     glMatrixMode(GL_MODELVIEW)

# if __name__ == '__main__':
#     glutInit()
#     glutInitWindowSize(screenWidth, screenHeight)
#     glutInitWindowPosition(0, 0)
#     glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
#     glutCreateWindow(b"Assignment1 Task2")

#     init()

#     glutDisplayFunc(display)
#     glutIdleFunc(animate)
#     glutKeyboardFunc(keyboardListener)
#     glutSpecialFunc(specialKeyListener)
#     glutMouseFunc(mouseListener)

#     last_frame_time = glutGet(GLUT_ELAPSED_TIME)
#     last_blink_time = last_frame_time

#     glutMainLoop()



