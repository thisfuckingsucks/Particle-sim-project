import ball
import turtle
import random
import math
import text

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
        self.ay = -0.2
        self.coefficient = 0.8
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
                    self.ball_list[i].turtle.hideturtle()
                    i += 1

        self.text = {}

        self.screen = turtle.Screen()
        self.start = False
        self.start_setup_bool = False
        self.choice = None
        self.selected_ball = None

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
        self.text['speed'].text.clear()
        self.text['speed'].text.write(f'Speed: {round(self.dt * 5, 3):.2f}x', False,font=('Arial', 16, 'normal'))

    def speed_down(self):
        self.dt -= 0.05
        self.text['speed'].text.clear()
        self.text['speed'].text.write(f'Speed: {round(self.dt * 5, 3):.2f}x', False,font=('Arial', 16, 'normal'))

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

    def ui_start(self):
        self.text['title'] = text.Text()
        self.text['title'].text.goto(0,200)
        self.text['title'].write('Particle Simulation',write_type='bold',write_size=48)
        for i in range(10):
            self.text[f'{i}'] = text.Text(id=i)
            self.text[f'{i}'].text.goto(-200,100-i*50)
        size = 24
        self.text['0'].write('Start setup',write_size=24)
        self.text['1'].write('Particle amount', write_size=24)
        self.text['2'].write('Particle size', write_size=24)
        self.text['3'].write('Particle mass', write_size=24)
        self.text['4'].write('Particle elasticity', write_size=24)
        self.text['5'].write('Gravity', write_size=24)
        self.text['6'].write('Simulation speed', write_size=24)
        self.text['7'].write('Appearance/Color', write_size=24)
        self.screen.onkeypress(self.start_setup, '0')

    def start_simulation(self):
        self.start = True

    def turtle_setup(self):
        self.screen.onscreenclick(self.mouse_down, 1)
        self.screen.onscreenclick(self.right_click, 3)
        self.screen.onkeypress(self.speed_up, 'Up')
        self.screen.onkeypress(self.speed_down, 'Down')
        self.text['speed'] = text.Text()
        self.text['speed'].text.goto(self.canvas_width - 150, self.canvas_height + 25)
        self.text['speed'].text.write(f'Speed: {round(self.dt * 5, 3):.2f}x', False, font=('Arial', 16, 'normal'))

    def select_right(self):
        if self.text['selector'].selector_id+1 == self.num_balls:
            self.text['selector'].selector_id -= self.num_balls
        self.text['selector'].text.goto(self.ball_list[self.text['selector'].selector_id+1].x,
                                        self.ball_list[self.text['selector'].selector_id+1].y)
        self.text['selector'].selector_id += 1
        self.select_ui(self.text['selector'].selector_id)

    def select_left(self):
        if self.text['selector'].selector_id-1 == -1:
            self.text['selector'].selector_id += self.num_balls
        self.text['selector'].text.goto(self.ball_list[self.text['selector'].selector_id-1].x,
                                        self.ball_list[self.text['selector'].selector_id-1].y)
        self.text['selector'].selector_id -= 1
        self.select_ui(self.text['selector'].selector_id)

    def select_ui(self,id):
        select_ui_list = ['size','mass','x','y','vx','vy','ax','ay','elasticity','color']
        qwerty = ['q','w','e','r','t','y','u','i','o','p']
        j = 0
        k = 0
        for i in range(len(select_ui_list)):
            self.text[select_ui_list[i]].text.clear()
            if i == 5:
                k = 0
                j = 1
            self.text[select_ui_list[i]].text.goto(-420+160*k,-340-40*j)
            self.text[select_ui_list[i]].write(qwerty[i]+':  '+
                                               select_ui_list[i]+f' {getattr(self.ball_list[id],select_ui_list[i])}',
                                               write_align='left',write_size=14)
            k += 1

    def value_change(self):
        self.selected_ball = self.ball_list[self.text['selector'].selector_id]
        self.selected_ball.select(self.choice,1)
        self.select_ui(self.text['selector'].selector_id)
    def value_down(self):
        self.selected_ball = self.ball_list[self.text['selector'].selector_id]
        self.selected_ball.select(self.choice,-1)
        self.select_ui(self.text['selector'].selector_id)

    def select_size(self):
        self.choice = 'size'
        self.screen.onkeypress(self.value_change, 'Up')
        self.screen.onkeypress(self.value_down, 'Down')
    def select_mass(self):
        self.choice = 'mass'
        self.screen.onkeypress(self.value_change, 'Up')
        self.screen.onkeypress(self.value_down, 'Down')
    def select_x(self):
        self.choice = 'x'
        self.screen.onkeypress(self.value_change, 'Up')
        self.screen.onkeypress(self.value_down, 'Down')
    def select_y(self):
        self.choice = 'y'
        self.screen.onkeypress(self.value_change, 'Up')
        self.screen.onkeypress(self.value_down, 'Down')
    def select_vx(self):
        self.choice = 'vx'
        self.screen.onkeypress(self.value_change, 'Up')
        self.screen.onkeypress(self.value_down, 'Down')
    def select_vy(self):
        self.choice = 'vy'
        self.screen.onkeypress(self.value_change, 'Up')
        self.screen.onkeypress(self.value_down, 'Down')
    def select_ax(self):
        self.choice = 'ax'
        self.screen.onkeypress(self.value_change, 'Up')
        self.screen.onkeypress(self.value_down, 'Down')
    def select_ay(self):
        self.choice = 'ay'
        self.screen.onkeypress(self.value_change, 'Up')
        self.screen.onkeypress(self.value_down, 'Down')
    def select_elasticity(self):
        self.choice = 'elasticity'
        self.screen.onkeypress(self.value_change, 'Up')
        self.screen.onkeypress(self.value_down, 'Down')

    def select_change(self,choice):
        self.ball_list[self.text['selector'].selector_id].__getattribute__(choice)
        self.ball_list[0].ge = 1

    def run(self):
        # clear ui
        select_ui_list = ['size', 'mass', 'x', 'y', 'vx', 'vy', 'ax', 'ay', 'elasticity', 'color']
        for i in select_ui_list:
            self.text[i].text.clear()
        # clear controls
        qwerty = ['q','w','r','t','y','u','i','o','p']
        for i in qwerty:
            self.screen.onkeypress(None, i)
        self.screen.onkeypress(None, 'Up')
        self.screen.onkeypress(None, 'Down')
        self.screen.onkeypress(None, '0')
        self.screen.onkeypress(None, 'Right')
        self.screen.onkeypress(None, 'Left')
        self.text['selector'].text.hideturtle()

        self.screen.tracer(0)

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

    def start_setup(self):
        self.start_setup_bool = True
        self.text['title'].text.clear()
        for i in range(10):
            self.text[f'{i}'].text.clear()
        self.__draw_border()
        for i in self.ball_list:
            i.turtle.showturtle()
            i.turtle.goto(i.x,i.y)
        self.text['selector'] = text.Text()
        self.text['selector'].text.showturtle()
        self.text['selector'].text.left(90)
        self.text['selector'].text.color(255,0,0)
        self.text['selector'].text.goto(self.ball_list[0].x,self.ball_list[0].y)
        self.screen.onkeypress(self.run, '0')
        self.screen.onkeypress(self.select_right, 'Right')
        self.screen.onkeypress(self.select_left, 'Left')
        select_ui_list = ['size', 'mass', 'x', 'y', 'vx', 'vy', 'ax', 'ay', 'elasticity', 'color']
        for i in range(len(select_ui_list)):
            self.text[select_ui_list[i]] = text.Text()
        self.select_ui(self.text['selector'].selector_id)
        self.screen.onkeypress(self.select_size, 'q')
        self.screen.onkeypress(self.select_mass, 'w')
        self.screen.onkeypress(self.select_x, 'e')
        self.screen.onkeypress(self.select_y, 'r')
        self.screen.onkeypress(self.select_vx, 't')
        self.screen.onkeypress(self.select_vy, 'y')
        self.screen.onkeypress(self.select_ax, 'u')
        self.screen.onkeypress(self.select_ay, 'i')
        self.screen.onkeypress(self.select_elasticity, 'o')
        self.selected_ball = self.ball_list[self.text['selector'].selector_id]

    def start_sim(self):
        self.screen.listen()
        self.ui_start()
        turtle.hideturtle()
        while True:
            self.screen.update()

num_balls = 49
my_simulator = Simulation(num_balls)
my_simulator.start_sim()
