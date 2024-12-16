import turtle

class Text:
    def __init__(self,font_size=16,id=-1,selector_id = 0):
        self.text = turtle.Turtle()
        self.text.penup()
        self.text.hideturtle()
        self.font = ('Arial',font_size,'normal')
        self.id = id
        self.selector_id = selector_id

    def write(self,text,write_size=16,write_align='center',write_type='normal'):
        if self.id in range(10):
            write_align = 'left'
            text = f'{self.id} '+text
        self.text.write(text,font=('Arial',write_size,write_type),align=write_align)