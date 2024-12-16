import ball
import turtle
import random
import math

class Simulation:
    def __init__(self, num_balls):
        self.num_balls = num_balls
        self.ball_list = []
        turtle.speed(0)
        turtle.tracer(0)
        turtle.colormode(255)
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        print(self.canvas_width, self.canvas_height)
        self.ay = -0
        self.coefficient = 1
        self.click = False
        self.click_x = 0
        self.click_y = 0
        self.dt = 0.2
        self.color = False
        self.energy = True

        ball_radius = 2

        # create balls in a grid pattern
        grid_size = 1
        while num_balls > grid_size**2:
            grid_size += 1
        i = 0
        for k in range(grid_size):
            for p in range(grid_size):
                if i < self.num_balls:
                    x = -self.canvas_width + (p + 1) * (2 * self.canvas_width / (grid_size + 1))
                    y = -self.canvas_height + (k + 1)*(2 * self.canvas_height / (grid_size + 1))
                    vx = 0 * random.uniform(-1.0, 1.0)
                    vy = 0 * random.uniform(-1.0, 1.0)
                    if i == 21:
                        vx = 10
                        vy = 10
                    ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                    ball_radius = random.uniform(2,2)

                    self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color,i,
                                                    ay=self.ay, coefficient = self.coefficient))
                    i += 1

        self.turtle = turtle.Turtle()

        self.screen = turtle.Screen()

    def __draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.color((0, 0, 0))
        for i in range(2):
            turtle.forward(2*self.canvas_width)
            turtle.left(90)
            turtle.forward(2*self.canvas_height)
            turtle.left(90)

    def mouse_down(self,x,y):
        self.click_x = x
        self.click_y = y
        self.click = True

    def right_click(self,x,y):
        self.click = False

    def speed_up(self):
        self.dt += 0.05
        self.turtle.clear()
        self.turtle.write(f'Speed: {round(self.dt * 5, 3):.2f}x', False,font=('Arial', 16, 'normal'))

    def speed_down(self):
        self.dt -= 0.05
        self.turtle.clear()
        self.turtle.write(f'Speed: {round(self.dt * 5, 3):.2f}x', False,font=('Arial', 16, 'normal'))

    def color_mode(self):
        for b in self.ball_list:
            blue = 255
            red = 0
            if b.velocity() > 1:
                change = int(b.velocity()*10)
                blue -= change
                if blue < 0:
                    blue = 0
                red += change
                if red > 255:
                    red = 255
            b.turtle.color(red,0,blue)

    def energy_mode(self):
        for b in self.ball_list:
            blue = 255
            red = 0
            change = int(b.kinetic_energy() / 10000)
            blue -= change
            if blue < 0:
                blue = 0
            red += change
            if red > 255:
                red = 255
            b.turtle.color(red, 0, blue)

    def ball_collision(self):
        pass

    def turtle_setup(self):
        self.screen.listen()
        self.screen.onscreenclick(self.mouse_down, 1)
        self.screen.onscreenclick(self.right_click, 3)
        self.screen.onkeypress(self.speed_up, 'Up')
        self.screen.onkeypress(self.speed_down, 'Down')
        self.turtle.penup()
        self.turtle.hideturtle()
        self.turtle.goto(self.canvas_width - 150, self.canvas_height + 25)
        self.turtle.write(f'Speed: {round(self.dt * 5, 3):.2f}x', False, font=('Arial', 16, 'normal'))

    def run(self):
        self.screen.tracer(0)
        self.__draw_border()

        for b in self.ball_list:
            b.turtle.goto(b.x,b.y)

        self.turtle_setup()
        while True:
            self.screen.update()
            if self.click:
                for i in self.ball_list:
                    dist = math.sqrt((i.x - self.click_x)**2 + (i.y - self.click_y)**2)
                    if dist <= 200:
                        cos = (i.x - self.click_x) / dist
                        sin = (i.y - self.click_y) / dist
                        piff = 1 - dist / 200
                        i.fx += -200000 * cos * piff
                        i.fy += -200000 * sin * piff
            start = 1
            for b in self.ball_list:
                b.update(self.dt)
                for ba in self.ball_list:
                    for c in range(start,len(self.ball_list)):
                        ba.ball_collision(self.ball_list[c])
                    start += 1
            if self.color:
                self.color_mode()
            if self.energy:
                self.energy_mode()

num_balls = 49
my_simulator = Simulation(num_balls)
my_simulator.run()
