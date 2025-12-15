#TASK2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

screenWidth, screenHeight = 1300, 650
all_points = []
base_speed = 5
speed_multiplier = 1.0
min_speed_multiplier = 0.1
max_speed_multiplier = 70.0
point_radius = 3
is_paused = False
blinkingStatus = False
blink_state = True 
last_frame_time = 0
last_blink_time = 0

X_MIN, X_MAX = -screenWidth / 2, screenWidth / 2
Y_MIN, Y_MAX = -screenHeight / 2, screenHeight / 2

def convert_coordinate(x, y):
    return x - (screenWidth / 2), (screenHeight / 2) - y

def get_random_color():
    return (random.random(), random.random(), random.random())

def draw_square(x, y, size):
    half_size = size / 2.0
    glBegin(GL_QUADS)
    glVertex2f(x - half_size, y - half_size)
    glVertex2f(x + half_size, y - half_size)
    glVertex2f(x + half_size, y + half_size)
    glVertex2f(x - half_size, y + half_size)
    glEnd()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = get_random_color()
        self.dx = (1 if random.random() < 0.5 else -1) * base_speed
        self.dy = (1 if random.random() < 0.5 else -1) * base_speed
        self.speed = math.hypot(self.dx, self.dy)
        self.radius = max(3, min(10, self.speed * 0.8))

    def draw(self):
        if blinkingStatus and not blink_state:
            glColor3f(0.0, 0.0, 0.0)  
        else:
            glColor3f(*self.color)
        draw_square(self.x, self.y, self.radius)

    def update(self, delta_time_ms, current_speed_multiplier):
        move_factor = (delta_time_ms / 16.66) * current_speed_multiplier
        self.x += self.dx * move_factor
        self.y += self.dy * move_factor

        if self.x + self.radius / 2 > X_MAX:
            self.x = X_MAX - self.radius / 2
            self.dx *= -1
        elif self.x - self.radius / 2 < X_MIN:
            self.x = X_MIN + self.radius / 2
            self.dx *= -1

        if self.y + self.radius / 2 > Y_MAX:
            self.y = Y_MAX - self.radius / 2
            self.dy *= -1
        elif self.y - self.radius / 2 < Y_MIN:
            self.y = Y_MIN + self.radius / 2
            self.dy *= -1

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    for point in all_points:
        point.draw()

    glutSwapBuffers()

def animate():
    global last_frame_time, last_blink_time, blink_state

    current_time_ms = glutGet(GLUT_ELAPSED_TIME)
    delta_time_ms = current_time_ms - last_frame_time
    last_frame_time = current_time_ms

    if not is_paused:
        if blinkingStatus and (current_time_ms - last_blink_time >= 500):
            blink_state = not blink_state
            last_blink_time = current_time_ms

        for point in all_points:
            point.update(delta_time_ms, speed_multiplier)

    glutPostRedisplay()

def keyboardListener(key, x, y):
    global is_paused

    if key == b' ':
        is_paused = not is_paused
        print("Paused" if is_paused else "Resumed")

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed_multiplier

    if not is_paused:
        if key == GLUT_KEY_UP:
            speed_multiplier = min(speed_multiplier + 0.1, max_speed_multiplier)
            print(f"Speed Increased: {speed_multiplier:.1f}x")
        elif key == GLUT_KEY_DOWN:
            speed_multiplier = max(speed_multiplier - 0.1, min_speed_multiplier)
            print(f"Speed Decreased: {speed_multiplier:.1f}x")
    else:
        print("Paused. Cannot change speed.")

    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global blinkingStatus

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if not is_paused:
            gl_x, gl_y = convert_coordinate(x, y)
            all_points.append(Point(gl_x, gl_y))
            print(f"New point at ({gl_x:.2f}, {gl_y:.2f})")
        else:
            print("Paused. Cannot add point.")

    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not is_paused:
            blinkingStatus = not blinkingStatus
            print("Blinking status:", blinkingStatus)

    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-screenWidth / 2, screenWidth / 2, -screenHeight / 2, screenHeight / 2)
    glMatrixMode(GL_MODELVIEW)

if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(screenWidth, screenHeight)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutCreateWindow(b"Assignment1 Task2")

    init()

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)

    last_frame_time = glutGet(GLUT_ELAPSED_TIME)
    last_blink_time = last_frame_time

    glutMainLoop()
