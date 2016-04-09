#!/usr/bin/python
#
# This is a quick and dirty example of how distance affects the timing
# of the sensors being hit by lighthouse. With these timings, we can
# determine distance and angle from the lighthouses.
#

import math
import pyglet
import time

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 720
BG_COLOR = (20, 20, 20)
LINE_COLOR = (255, 200, 200)
LINE_WIDTH = 5
AMPLITUDE = SCREEN_WIDTH
LH_ROTATION_SPEED = 0.003
CIRCLE_SIZE = 4

config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, caption='LibLighthouse-Mocap',
                              config=config)
fps_display = pyglet.clock.ClockDisplay()

step = 0

# Set up our lighthouse sweep line
line_start_x = int(SCREEN_WIDTH / 2)
line_start_y = SCREEN_HEIGHT
line_end_x = 0
line_end_y = 0

# Distance between our sensors
sensor_distance = 80
back_sensor_distance = 300

class Circle(object):
    def __init__(self, numPoints=200, x=0, y=0, color=[1, 1, 0]):
        self.verts = []
        for i in range(numPoints):
            self.angle = math.radians(float(i)/numPoints * 360.0)
            self.x = CIRCLE_SIZE*math.cos(self.angle) + x
            self.y = CIRCLE_SIZE*math.sin(self.angle) + y
            self.verts += [self.x, self.y]
        self.circle = pyglet.graphics.vertex_list(numPoints, ('v2f', self.verts))
        self.color = color
        self.was_hit = False
        self.time_elapsed = 0.0

    def draw(self):
        r, g, b = self.color
        pyglet.gl.glColor3f(r,g,b)
        self.circle.draw(pyglet.gl.GL_LINE_LOOP)

def slope(x1, y1, x2, y2):
    return (y1 - y2) / float(x1 - x2)

def update(dt):
    global line_start_x
    global line_start_y
    global line_end_x
    global line_end_y
    global step
    line_end_x = int(math.cos(step) * AMPLITUDE + (SCREEN_WIDTH / 2))
    line_end_y = int(-1 * math.sin(step) * AMPLITUDE + SCREEN_HEIGHT)
    try:
        lighthouse_slope = round(slope(line_end_x, line_end_y, line_start_x, line_start_y))
    except ZeroDivisionError:
        lighthouse_slope = 0

    # Find slope from circle to line start
    i = 0
    for circle in circles:
        circle_slope = round(slope(circle.x, circle.y, line_start_x, line_start_y))
        if circle_slope == lighthouse_slope and not circle.was_hit:
            print "Circle %i hit" % i
            circle.color = [1, 0, 0]
            circle.was_hit = True
            circle.time_hit = time.time()
            circle.time_elapsed = circle.time_hit - start_time
            print "  Time since start:", circle.time_hit - start_time
        elif circle.was_hit:
            pass
        else:
            circle.time_elapsed = time.time() - start_time
        labels[i].text = str(round(circle.time_elapsed, 2)) + " ms"
        i += 1

    #step += dt #0.02
    step += LH_ROTATION_SPEED
    step %= 2 * math.pi

@window.event
def on_draw():
    window.clear()
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)

    #device1_sprite.draw()
    device2_sprite.draw()

    pyglet.gl.glLineWidth(LINE_WIDTH)
    pyglet.gl.glColor3f(1,1,1)
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        ('v2i', (line_start_x, line_start_y, line_end_x, line_end_y))
    )

    for circle in circles:
        circle.draw()


    for label in labels:
        label.draw()

    #fps_display.draw()

start_time = time.time()

# Sensor circles
circles = []
#circles.append(Circle(x=SCREEN_WIDTH/2 - sensor_distance, y=SCREEN_HEIGHT/2))
#circles.append(Circle(x=SCREEN_WIDTH/2 + sensor_distance, y=SCREEN_HEIGHT/2))
circles.append(Circle(x=SCREEN_WIDTH/2 - sensor_distance, y=SCREEN_HEIGHT/2 - back_sensor_distance))
circles.append(Circle(x=SCREEN_WIDTH/2 + sensor_distance, y=SCREEN_HEIGHT/2 - back_sensor_distance))

# Timer labels
label_distance = 15
labels = []
#labels.append(pyglet.text.Label("", font_size=11,
#                                x=SCREEN_WIDTH/2 - sensor_distance + label_distance,
#                                y=SCREEN_HEIGHT/2 + label_distance,
#                                anchor_x='left', anchor_y='center'))
#labels.append(pyglet.text.Label("", font_size=11,
#                                x=SCREEN_WIDTH/2 + sensor_distance + label_distance,
#                                y=SCREEN_HEIGHT/2 + label_distance,
#                                anchor_x='left', anchor_y='center'))
labels.append(pyglet.text.Label("", font_size=11,
                                x=SCREEN_WIDTH/2 - sensor_distance + label_distance,
                                y=SCREEN_HEIGHT/2 - back_sensor_distance + label_distance,
                                anchor_x='left', anchor_y='center'))
labels.append(pyglet.text.Label("", font_size=11,
                                x=SCREEN_WIDTH/2 + sensor_distance + label_distance,
                                y=SCREEN_HEIGHT/2 - back_sensor_distance + label_distance,
                                anchor_x='left', anchor_y='center'))

# Device sprites
device = pyglet.image.load('device.png')
#device1_sprite = pyglet.sprite.Sprite(device, x=SCREEN_WIDTH//2 - (device.width/2),
#                                      y=SCREEN_HEIGHT//2 - (device.height/2))
device2_sprite = pyglet.sprite.Sprite(device, x=SCREEN_WIDTH//2 - (device.width/2),
                                      y=SCREEN_HEIGHT//2 - back_sensor_distance - (device.height/2))

pyglet.clock.schedule_interval(update, 0.016)
pyglet.app.run()

