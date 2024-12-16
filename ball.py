import turtle
import math

class Ball:
    def __init__(self, size, x, y, vx, vy, color, id, ax=0, ay=0, fx=0, fy =0, coefficient = 1):
        self.size = size
        self.radius = size*10
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.mass = 100 * self.radius**2
        self.count = 0
        self.id = id
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        turtle.speed(0)
        turtle.tracer(0)
        turtle.colormode(255)
        self.turtle = turtle.Turtle()
        self.turtle.shape('circle')
        self.turtle.shapesize(size,size)
        self.turtle.color(color)
        self.turtle.penup()
        self.ax = ax
        self.ay = ay
        self.fx = fx
        self.fy = fy
        self.elasticity = coefficient

    def bounce_off(self, that):
        # error check
        'beforex,beforey = self.vx**2+that.vx**2, self.vy**2+that.vy**2'

        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy
        correct_dist = self.radius + that.radius
        c_distance = self.distance(that)
        mass_sum = self.mass + that.mass

        magnitude = 2 * self.mass * that.mass * dvdr / (mass_sum * c_distance**2)

        fx = magnitude * dx * self.elasticity
        fy = magnitude * dy * self.elasticity

        self.vx += fx / self.mass
        self.vy += fy / self.mass
        that.vx -= fx / that.mass
        that.vy -= fy / that.mass

        self.count += 1
        that.count += 1

        """afterx,aftery = self.vx**2 + that.vx**2, self.vy**2 + that.vy**2
        if round(beforex + beforey,10) != round(afterx + aftery,10):
            print('error')
            print('before',beforex+beforey)
            print('after',afterx+aftery"""

        # move balls away from each other so they don't overlap
        overlap = correct_dist - c_distance
        cos = (self.x - that.x) / c_distance
        sin = (self.y - that.y) / c_distance
        self_ratio = self.mass / mass_sum
        that_ratio = that.mass / mass_sum
        self.x += overlap * cos * self_ratio
        self.y += overlap * sin * self_ratio
        that.x -= overlap * cos * that_ratio
        that.y -= overlap * sin * that_ratio

    def distance(self, that):
        x1 = self.x
        y1 = self.y
        x2 = that.x
        y2 = that.y
        d = math.sqrt((y2-y1)**2 + (x2-x1)**2)
        return d

    def ball_collision(self,that):
        if self.distance(that) < (self.radius + that.radius):
            self.bounce_off(that)

    def update(self, dt):
        # F = ma
        # standard mass = 40000
        xx = self.fx / self.mass
        yy = self.fy / self.mass
        self.ax += xx
        self.ay += yy
        self.fx = 0
        self.fy = 0

        # update velocity
        self.vx += self.ax*dt
        self.vy += self.ay*dt

        self.ax -= xx
        self.ay -= yy

        # update position
        self.x += self.vx*dt
        self.y += self.vy*dt

        # check wall collision
        self.collision(self.canvas_height,self.canvas_width)

        # update graphic
        self.turtle.setx(self.x)
        self.turtle.sety(self.y)

    def collision(self,canvas_height,canvas_width):
        # move ball back into border
        if abs(self.x) > (canvas_width - self.radius):
            self.x = (canvas_width - self.radius) * math.copysign(1,self.x)
            self.vx = -self.vx * self.elasticity

        if abs(self.y) > (canvas_height - self.radius):
            self.y = (canvas_height - self.radius) * math.copysign(1, self.y)
            self.vy = -self.vy * self.elasticity

    def velocity(self):
        return math.sqrt(self.vx**2 + self.vy**2)

    def kinetic_energy(self):
        return (self.mass * self.velocity()**2) / 2

    def select(self,choice,value):
        if choice == 'size':
            i = 0.1*value
            self.size += i
            if self.size + i < 0.1:
                self.size = 0.1
            self.size = round(self.size,2)
            self.radius = self.size * 10
            self.turtle.shapesize(self.size,self.size)
        if choice == 'mass':
            i = 5000*value
            self.mass += i
            self.mass = round(self.mass,0)
            if self.mass <= 0:
                self.mass -= i
            self.mass = round(self.mass, 0)
        if choice == 'x':
            i = 10*value
            self.x += i
            self.turtle.setx(self.x)
        if choice == 'y':
            i = 10*value
            self.y += i
            self.turtle.sety(self.y)
        if choice == 'vx':
            i = 1*value
            self.vx += i
        if choice == 'vy':
            i = 1*value
            self.vy += i
        if choice == 'ax':
            i = 0.1*value
            self.ax += i
            self.ax = round(self.ax, 1)
        if choice == 'ay':
            i = 0.1*value
            self.ay += i
            self.ay = round(self.ay, 1)
        if choice == 'elasticity':
            i = 0.05*value
            self.elasticity += i
            if self.elasticity <= 0:
                self.elasticity = 0
            self.elasticity = round(self.elasticity,2)

    def __str__(self):
        return f'hi im ball {self.id}'