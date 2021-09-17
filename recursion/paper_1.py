from turtle import *
from math import sqrt
## Ex. 2
### Shape 1
def square(c):
	for _ in range(4):
		forward(c) 
		left(90)

def shape_1(c):
	if c < 10: # Stop condition
		return
	square(c)
	forward(c / 2)
	left(45)
	shape_1(c / 2 * sqrt(2))

### Shape 2
def triangle(c):
	for _ in range(3):
		forward(c)
		left(120)

def shape_2(c):
	if c < 10: # Stop condition
		return
	triangle(c)
	forward(c / 2)
	left(60)
	shape_2(c / 2)

### Shape 3
def shape_3(c):
	if c < 10: 
		return
	fillcolor('black')
	begin_fill()
	circle(c)
	end_fill()
	fillcolor('white')
	begin_fill()
	left(45)
	square(c * sqrt(2))
	end_fill()
	forward(c / 2 * sqrt(2))
	shape_3(c / 2 * sqrt(2))
