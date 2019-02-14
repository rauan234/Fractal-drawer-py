import random
import numpy
import time

import pygame
pygame.init()



pi = 3.141592

XSize = 1500
YSize = 900

MaximalNumberOfPoints = 2 ** 15



main_screen = pygame.display.set_mode((XSize, YSize))



class vector:
    def __init__(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    
    def __sub__(self, other):
        return vector(
            self.x - other.x,
            self.y - other.y
            )
    def __add__(self, other):
        return vector(
            self.x + other.x,
            self.y + other.y
            )    
class phasor:
    def __init__(self, new_magnitude, new_phase):
        self.magnitude = new_magnitude
        self.phase = new_phase



def phasor_to_vector(p):
    out = vector(0, 0)
    
    out.x = p.magnitude * numpy.cos(p.phase)
    out.y = p.magnitude * numpy.sin(p.phase)  
    
    return out
def vector_to_phasor(v):
    out = phasor(0, 0)
    
    out.phase = numpy.arctan(v.y / v.x)
    out.magnitude = numpy.sqrt(v.y ** 2 + v.x ** 2)    
    
    return out

def clear_screen():
    main_screen.fill((0, 0, 0))
def display():
    pygame.display.flip()
def wait_for_termination():
    running = True
    
    while(running):
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            running = False
                    
                    time.sleep(0.01)
def draw_point(x, y, color):
    main_screen.set_at((int(x), int(y)), color)
def input_int(text):
    while(1):
        inp = input(text)
        
        try:
            return int(inp)
        
        except Exception:
            print("    Enter integer value")
    
    
    
class Fractal:
    # Existing variables:
    #     number_of_start_points - determines number of points
    #     start_radius - desctibes distance from the start points
    #       to the center of the screen
    #     point_color - describes color of fractal points
    #     point_profile - describes the fractal base
    
    def __init__(self, new_number_of_points, new_number_of_additional_points, new_start_radius=100, new_point_color=(255, 255, 255)):
        self.number_of_start_points = new_number_of_points
        self.number_of_additional_points = new_number_of_additional_points
        self.start_radius = new_start_radius
        self.point_color = new_point_color
        
        self.set_point_profile()
        self.set_points()
        
    def set_points(self):
        self.points = []
        
        angle = 0
        while(angle < 2 * pi):
            self.points.append((
                XSize / 2 + self.start_radius * numpy.sin(angle),
                YSize / 2 + self.start_radius * numpy.cos(angle),
            ))
            
            angle += 2 * pi / self.number_of_start_points
    
    def set_point_profile(self):
        self.point_profile = []
        
        for point_id in range(self.number_of_additional_points):
            x = random.random()
            y = random.random()
            
            phs = phasor(x, y)
            self.point_profile.append(phs)
    
    def render(self):
        for point in self.points:
            draw_point(*point, self.point_color)
        
    def calculate(self, number_of_iterations):
        for iteration in range(number_of_iterations):
            new_points = []
            
            for point_id in range(len(self.points) - 1):
                new_points.append(self.points[point_id])
                new_points += self.newpoints(
                    self.points[point_id], self.points[point_id + 1]
                )
            new_points.append(self.points[-1])
            new_points += self.newpoints(self.points[-1], self.points[0])
            
            self.points = new_points.copy()
        
    def newpoints(self, pointA, pointB):
        out = []
        
        A = vector(pointA[0], pointA[1])
        B = vector(pointB[0], pointB[1])
        
        prime_line = vector_to_phasor(A - B)
        
        for point in self.point_profile:
            phs = phasor(
                prime_line.magnitude * point.magnitude,
                prime_line.phase + point.phase
            )
            if(A.x >= B.x):
                phs.phase += pi
            phs = vector_to_phasor(A + phasor_to_vector(phs))
            
            new_point = phasor_to_vector(phs)
            
            out.append((
                new_point.x,
                new_point.y
            ))
            
        return out
                


def main():
    clear_screen()
    
    print("Welcome to the fractal generator!")
    print("This program created pseudo - random fractals.")
    print()
    
    print("Enter parameters of a fractal:")
    number_of_start_points =      input_int("Enter number of start points: (try 3)                   ")
    number_of_additional_points = input_int("Enter number of points added every iteration: (try 1)   ")
    start_radius =                input_int("Enter fractal`s start size: (try 200)                   ")
    print()
    
    print("Started creating the fractal")
    fract = Fractal(number_of_start_points, number_of_additional_points, new_start_radius=start_radius)
    print("Finished initialisation of a fractal")
    fract.calculate(int(numpy.log(MaximalNumberOfPoints / number_of_start_points) / numpy.log(1 + number_of_additional_points)))
    print("Finished calculating the fractal")
    fract.render()
    print("Finished rendering the fractal")
    print()
    
    display()
    print("Finished drawing the fractal")
    print()
    
    filename = ("Fractal" + str(int(time.time())) + ".jpeg")
    pygame.image.save(main_screen, filename)
    print("Saved image into '" + filename + "' file")
    print()
    
    print("Close the window to exit")
    wait_for_termination()
    pygame.quit()
    


main()