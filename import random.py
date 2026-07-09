import turtle
screen = turtle.Screen()
screen.title("Turtle Screen")

t = turtle.Turtle()
t.speed(1)
t.color("blue")
t.shape("turtle")

t.forward(300)
t.backward(1)
t.right(90)
t.left(180)
t.goto(250, 100)
t.goto(-250,100)
t.goto(-250,-100)
t.goto(250,100)
t.goto(500,45)
t.goto(100,540)
t.goto(87,98)
t.goto()
t.penup
t.pendown
t.pensize
t.pencolor("brown")
screen.mainloop()

