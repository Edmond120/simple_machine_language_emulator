import turtle
class Turtle_interface:
	def __init__(self):
		self.turtle = turtle.Turtle()
		self.screen = turtle.Screen()
		turtle.setup(500,500)

	def forward(self,value):
		self.turtle.forward(value)
		return 0

	def left(self,value):
		self.turtle.left(value)
		return 0

	def right(self,value):
		self.turtle.right(value)
		return 0

	def setheading(self,value):
		self.turtle.setheading(value)
		return 0

	def setx(self,value):
		self.turtle.setx(value)
		return 0

	def sety(self,value):
		self.turtle.sety(value)
		return 0

	def speed(self,value):
		self.turtle.speed(value)
		return 0

	def pendown(self,value):
		self.turtle.pendown()
		return 0

	def penup(self,value):
		self.turtle.penup()
		return 0
