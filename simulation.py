from modulefinder import packagePathMap

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
        self.click = False
        self.click_x = 0
        self.click_y = 0
        self.dt = 0.2
        self.color = False
        self.energy = False

        self.mass = 0
        self.rvl = -1.0
        self.rvu = 1.0
        self.vx = 10 * random.uniform(self.rvl, self.rvu)
        self.vy = 10 * random.uniform(self.rvl, self.rvu)
        self.random_velocity = True
        self.ax = 0
        self.ay = 0
        self.coefficient = 1
        self.p_size = 2.0
        self.rsl = 1.5
        self.rsu = 2.5
        self.random_size = False

        self.text = {}

        self.screen = turtle.Screen()
        self.start = False
        self.choice = None
        self.selected_ball = None
        self.reset_color = False

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
                change = int(b.velocity()*15)
                if change > 255:
                    change = 255
                if change < 0:
                    change = 0
                blue -= change
                red += change
            b.turtle.color(red,0,blue)

    def energy_mode(self):
        for b in self.ball_list:
            blue = 255
            red = 0
            change = int(b.kinetic_energy() / 15000)
            if change > 255:
                change = 255
            if change < 0:
                change = 0
            blue -= change
            red += change
            b.turtle.color(0, red, blue)

    def color_bool(self):
        self.energy = False
        if self.color:
            self.color = False
            self.reset_color = True
        else:
            self.color = True

    def energy_bool(self):
        self.color = False
        if self.energy:
            self.energy = False
            self.reset_color = True
        else:
            self.energy = True

    def ui_start(self):
        self.text['title'] = text.Text()
        self.text['title'].text.goto(0,200)
        self.text['title'].write('Particle Simulation',write_type='bold',write_size=48)
        for i in range(10):
            self.text[f'{i}'] = text.Text(id=i)
            self.text[f'{i}'].text.goto(-200,100-i*50)
        self.text['0'].write('Start setup',write_size=24)
        self.text['1'].write('Edit global parameters', write_size=24)
        self.screen.onkeypress(self.start_setup, '0')
        self.screen.onkeypress(self.edit_parameter, '1')

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
        self.text['color'] = text.Text()
        self.text['color'].text.goto(-400, 325)
        self.text['color'].write('z: velocity display / x: energy display',write_align='left')
        self.screen.onkeypress(self.color_bool, 'z')
        self.screen.onkeypress(self.energy_bool, 'x')

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
            if qwerty[i] == 'p':
                self.text[select_ui_list[i]].write(qwerty[i]+':  '+
                                                   select_ui_list[i]+f' {getattr(self.ball_list[id],select_ui_list[i])}',
                                                   write_align='left',write_size=13)
            else:
                self.text[select_ui_list[i]].write(qwerty[i] + ':  ' +
                                                   select_ui_list[
                                                       i] + f' {getattr(self.ball_list[id], select_ui_list[i]):.2f}',
                                                   write_align='left', write_size=13)
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
            if self.reset_color:
                for ba in self.ball_list:
                    ba.turtle.color(ba.color)
                self.reset_color = False

    def start_setup(self):
        # create balls in a grid pattern
        grid_size = 1
        while self.num_balls > grid_size ** 2:
            grid_size += 1
        i = 0
        for k in range(grid_size):
            for p in range(grid_size):
                if i < self.num_balls:
                    x = -self.canvas_width + (p + 1) * (2 * self.canvas_width / (grid_size + 1))
                    y = -self.canvas_height + (k + 1) * (2 * self.canvas_height / (grid_size + 1))
                    if self.random_velocity:
                        vx = 10 * random.uniform(self.rvl, self.rvu)
                        vy = 10 * random.uniform(self.rvl, self.rvu)
                    else:
                        vx = self.vx
                        vy = self.vy

                    ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                    if self.random_size:
                        ball_radius = random.uniform(self.rsl, self.rsu)
                    else:
                        ball_radius = self.p_size

                    self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, i,
                                                    ay=self.ay,ax=self.ax, coefficient=self.coefficient))
                    self.ball_list[i].turtle.hideturtle()
                    i += 1
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
        self.screen.onkeypress(None, '1')
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

    def particle_velocity(self):
        while True:
            print(f'\n1. Uniform velocity\n'
                  f'2. Random velocity\n'
                  f'3. Exit')
            i = input('Input option: ')
            if i == '1':
                print(f'\nVertical velocity\n'
                      f'Normal range: (-10, 10)\n'
                      f'(positive is up)')
                vv = float(input('Enter velocity value: '))
                self.vy = vv
                print(f'\nHorizontal velocity\n'
                      f'Normal range: (-10, 10)\n'
                      f'(positive is right)')
                hv = float(input('Enter velocity value: '))
                self.vx = hv
                self.random_velocity = False
            if i == '2':
                print(f'\nRandom velocity\n'
                      f'Default range: (-1.0, 1.0)')
                rvl = float(input('Enter velocity lower limit: '))
                self.rvl = rvl
                while True:
                    rvu = float(input('Enter velocity upper limit: '))
                    if rvu > rvl:
                        self.rvu = rvu
                        self.random_velocity = True
                        break
            if i == '3':
                break

    def particle_size(self):
        while True:
            print(f'\n1. Uniform size\n'
                  f'2. Random size\n'
                  f'3. Exit')
            i = input('Input option: ')
            if i == '1':
                while True:
                    print(f'\nParticle size\n'
                          f'Default value: 2.0\n'
                          f'Normal range: (1.0, 3.0)')
                    ps = float(input('Enter size value: '))
                    if ps > 0:
                        self.p_size = ps
                        self.random_size = False
                        break
            if i == '2':
                while True:
                    print(f'\nRandom particle size\n'
                          f'Normal range: (1.00, 3.00)')
                    rsl = float(input('Enter size lower limit: '))
                    if rsl > 0:
                        rsu = float(input('Enter size upper limit: '))
                        if rsu > 0:
                            self.rsl = rsl
                            self.rsu = rsu
                            self.random_size = True
                            break
            if i == '3':
                break

    def edit_parameter(self):
        while True:
            print(f'\n1. Amount of particles\n'
                  f'2. Particle size\n'
                  f'3. Particle velocity\n'
                  f'4. Gravity\n'
                  f'5. Elasticity\n'
                  f'6. Exit')
            i = input('Input option: ')
            if i == '1':
                while True:
                    print(f'\nAmount of particles\n'
                          f'Default value: 25\n'
                          f'Range: (1, 100)')
                    pa = int(input('Enter particle amount: '))
                    if pa > 0:
                        self.num_balls = pa
                        break
            if i == '2':
                self.particle_size()
            if i == '3':
                self.particle_velocity()
            if i == '4':
                while True:
                    print(f'\nVertical gravity\n'
                          f'Default Value: 0.0\n'
                          f'Normal range: (-1.0, 1.0)\n'
                          f'(positive is up)')
                    vg = float(input('Enter gravity value: '))
                    self.ay = vg
                    print(f'\nHorizontal gravity\n'
                          f'Default Value: 0.0\n'
                          f'Normal range: (-1.0, 1.0)\n'
                          f'(positive is right)')
                    hg = float(input('Enter gravity value: '))
                    self.ax = hg
                    break
            if i == '5':
                while True:
                    print(f'\nElasticity\n'
                          f'Default value: 1.00\n'
                          f'Normal range: (0.00, 1.00)')
                    e = float(input('Enter elasticity value: '))
                    if e >= 0:
                        self.coefficient = e
                        break
            if i == '6':
                break

num_balls = 25
my_simulator = Simulation(num_balls)
my_simulator.start_sim()
