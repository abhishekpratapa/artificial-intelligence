from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random

global pathTaken;
pathTaken = [];

#class simple_problem_solving_agent:

class Points:
	x = 0;
	y = 0;
	def __init__(self, xcord, ycord):
		self.x = xcord;
		self.y = ycord;

class Lines:
	def __init__(self, begline, endline):
		self.beg = begline;
		self.end = endline;
	def distance(self):
		return math.sqrt((self.beg.x-self.end.x)*(self.beg.x-self.end.x)+(self.beg.y-self.end.y)*(self.beg.y-self.end.y));

def greedy(cCity, cLines, startNode):
	global pathTaken;

	if not cCity:
		print(pathTaken);
		return pathTaken;

	leastOne = Lines(Points(0, 0), Points(width, height));

	xcoordinate = cCity[startNode].x;
	ycoordinate = cCity[startNode].y;

	for pnt in cLines:
		if((((pnt.beg.x == xcoordinate) and (pnt.beg.y == ycoordinate)) or ((pnt.end.x == xcoordinate) and (pnt.end.y == ycoordinate))) and (pnt.distance() < leastOne.distance())):
			leastOne = pnt;

	print("Point 	"+str(leastOne.beg.x)+", "+str(leastOne.beg.y));
	pathTaken.append(leastOne);
	cLines.remove(leastOne);
	cCity.remove(cCity[startNode]);

	the_city = [];

	for knw in cCity:
		print("City 	"+str(knw.x)+", "+str(knw.y));

		if(((leastOne.beg.x == knw.x) and (leastOne.beg.y == knw.y)) or ((leastOne.end.x == knw.x) and (leastOne.end.y == knw.y))):
			the_city.append(knw);
			break;

	sn = cCity.index(the_city[0]);

	return greedy(cCity, cLines, sn);

def create_city(number):
	counter = 0;
	listVariable = [];
	#return value
	city_point = [];

	number = number + 1;
	#find square
	while True:
		if(counter*counter > number):
			for x in range(0, counter*counter):
				listVariable.append(1);
			break;
		else:
			counter = counter + 1;
	#random squares
	for z in range(1, number):
		while True:
			choice = random.randrange(0, counter*counter, 1)+1; #one indexed
			if(listVariable[choice-1] == 1): #zero indexed
				row = math.floor(((choice*1.0)/counter)%counter)+1;
				column = (choice%counter)+1;
				
				rowWidth = width/counter;
				columnHeight = height/counter;

				startRow = int(rowWidth*row - rowWidth);
				startColumn = int(columnHeight*column - columnHeight);

				EndRow = int(rowWidth*row);
				EndColumn = int(columnHeight*column);

				ycordCity = random.randrange(startColumn, EndColumn, 1);
				xcordCity = random.randrange(startRow, EndRow, 1);

				city_point.append(Points(xcordCity, ycordCity));

				listVariable[choice-1] = 0;
				break;
	return city_point;

def drawCities(city_point):
	lines = [];
	glColor3f(1.0, 1.0, 1.0);
	for i in city_point:
		distanceTotal = width+height;
		
		for z in city_point:
			if (city_point.index(i) != city_point.index(z)):
				intersectionValue = False;
				#check line intersection
				for u in lines:
					I1 = [min(i.x, z.x), max(i.x, z.x)];
					I2 = [min(u.beg.x, u.end.x), max(u.beg.x, u.end.x)];

					Ia = [max( min(i.x, z.x), min(u.beg.x, u.end.x)), min( max(i.x, z.x), max(u.beg.x, u.end.x))];
					
					if((i.x == u.beg.x)and(i.y == u.beg.y)) or ((z.x == u.beg.x)and(z.y == u.beg.y)) or ((i.x == u.end.x)and(i.y == u.end.y)) or ((z.x == u.end.x)and(z.y == u.end.y)):
						intersectionValue = False;
					else:
						if (max(i.x, z.x) < min(u.beg.x, u.end.x)):
							intersectionValue = False;
						else:
							A1 = 0;
							A2 = 0;

							#set A1
							if (i.x-z.x) == 0:
								A1 = 100000;
							else:
								A1 = (i.y-z.y)/(i.x-z.x);

							#set A2
							if (u.beg.x-u.end.x) == 0:
								A2 = 100000;
							else:
								A2 = (u.beg.y-u.end.y)/(u.beg.x-u.end.x);

							b1 = i.y-A1*i.x
							b2 = u.beg.y-A2*u.beg.x

							if (A1 == A2):
								intersectionValue =  False;
							else:
								Xa = (b2 - b1) / (A1 - A2);
								Ya = A1 * Xa + b1;
								Ya = A2 * Xa + b2;

								if ((Xa < max(min(i.x,z.x), min(u.beg.x, u.end.x))) or (Xa > min(max(i.x,z.x), max(u.beg.x, u.end.x)))):
									intersectionValue = False;
								else:
									intersectionValue = True;
									break;
				#draw Graph
				if not(intersectionValue):
					lines.append(Lines(Points(i.x, i.y), Points(z.x, z.y)));
					drawLines(Points(i.x, i.y), Points(z.x, z.y));
	
	glColor3f(1.0, 0.0, 0.0);
	for i in city_point:
		drawCircle(Points(i.x, i.y), 10);

	return lines;
		

def squareDraw(startpoints, size):
	glBegin(GL_QUADS)
	glVertex2f(startpoints.x, startpoints.y);
	glVertex2f(startpoints.x, startpoints.y+size.y);
	glVertex2f(startpoints.x+size.x, startpoints.y+size.y);
	glVertex2f(startpoints.x+size.x, startpoints.y);
	glEnd();

def drawCircle(pointVersion, radius):
	glBegin(GL_POLYGON);
	for i in range(0,360, 30):
		xpoint = (radius*math.cos(math.radians(i))+pointVersion.x);
		ypoint = (radius*math.sin(math.radians(i))+pointVersion.y);
		glVertex2f(xpoint, ypoint);
	glEnd();

def drawLines(start, end):
	glBegin(GL_LINES);
	glVertex2f(start.x, start.y);
	glVertex2f(end.x, end.y);
	glEnd();

def refresh2d(width, height):
	glViewport(0, 0, width, height);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho(0.0, width, 0.0, height, 0.0, 1.0);
	glMatrixMode (GL_MODELVIEW);
	glLoadIdentity();

def update(value):
	glutSetWindow(window);
	glutPostRedisplay();
	glutTimerFunc(1000, update, 0)

def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glLoadIdentity();
	refresh2d(width, height);

	glColor3f(1.0, 0.0, 0.0);
	drawCityCommand(coordinatesCity);
	print(ptcloud);
	glColor3f(1.0, 1.0, 1.0);
	#TODO: Create Simulation

	glutSwapBuffers();

#initiate GLUT#
width, height = 500, 400;
glutInit();
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH);
glutInitWindowSize(width, height);
glutInitWindowPosition(0, 0);

#initiate new window#
window = glutCreateWindow("2d track");
glutDisplayFunc(draw);
glutSetWindow(window);
glutPostRedisplay();

#create a city
coordinatesCity = create_city(5);
cityLines = drawCities(coordinatesCity);
startingNode = 1;
ptcloud = greedy(coordinatesCity, cityLines, startingNode);

#animate#
glutTimerFunc(100, update, 0);

#initiate main#
glutMainLoop();
