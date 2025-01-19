import pygame
import math

class FlightSimulator:
    def __init__(self,size = (800,600)):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.running = True

        # Colors
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        
        # Rectangle height
        self.center = (size[0]//2,size[1]//2)
        self.hz = 100

        self.alfa = 2*math.pi/3 # = 120º
    
    def project_to_2D(self,_x,_y,_z):
        x = _x - _z*math.sin(self.alfa)
        y = _y + _z*math.cos(self.alfa)
        return (int(x),-int(y))
    
    def draw_coords(self):
        length = 1000

        end_x_axis = self.project_to_2D(length,0,0)
        pygame.draw.line(self.screen,"red",self.center,(self.center[0]+end_x_axis[0],self.center[1]+end_x_axis[1]),2)

        end_y_axis = self.project_to_2D(0,length,0)
        pygame.draw.line(self.screen,"red",self.center,(self.center[0]+end_y_axis[0],self.center[1]+end_y_axis[1]),2)

        end_z_axis = self.project_to_2D(0,0,length)
        pygame.draw.line(self.screen,"red",self.center,(self.center[0]+end_z_axis[0],self.center[1]+end_z_axis[1]),2)

    def draw_body(self, h0=0, _angles=[0, 0,0]):
        angles = [angle * math.pi / 180 for angle in _angles]
    
        vr = math.sqrt(angles[0] ** 2 + angles[1] ** 2 + angles[2] ** 2)
        if vr > 0:
            theta = math.acos(angles[2] / vr)
            phi = math.atan2(angles[1], angles[0])
        else:
            theta, phi = 0, 0

        print(f"vr: {vr}\t\ttheta: {theta}\tphi:{phi}\t\tangles: {angles}")

        length = 90
        width = 80
        height = 10
        
        # Corrected vertices calculation
        vertices = [
            [-length, h0, -width],
            [-length, h0, width],
            [length, h0, width],
            [length, h0, -width],
            [-length, h0 + height, -width],
            [-length, h0 + height, width],
            [length, h0 + height, width],
            [length, h0 + height, -width]
        ]

        # Apply rotation
        rotated_vertices = []
        for vertex in vertices:
            x, y, z = vertex
            rotated_x = x * math.cos(theta) * math.cos(phi) - y * math.sin(theta) + z * math.cos(theta) * math.sin(phi)
            rotated_y = x * math.sin(theta) * math.cos(phi) + y * math.cos(theta) + z * math.sin(theta) * math.sin(phi)
            rotated_z = -x * math.sin(phi) + z * math.cos(phi)
            rotated_vertices.append([rotated_x, rotated_y, rotated_z])

        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]
        ]

        for edge in edges:
            start = self.project_to_2D(rotated_vertices[edge[0]][0], rotated_vertices[edge[0]][1], rotated_vertices[edge[0]][2])
            end = self.project_to_2D(rotated_vertices[edge[1]][0], rotated_vertices[edge[1]][1], rotated_vertices[edge[1]][2])
            pygame.draw.line(self.screen, "blue", (self.center[0] + start[0], self.center[1] + start[1]), (self.center[0] + end[0], self.center[1] + end[1]), 2)



    def draw_rectangle(self, hz): 
        rect_width = hz 
        rect_height = hz 
        top_left = (self.center[0] - rect_width // 2, self.center[1] - rect_height // 2) 
        pygame.draw.rect(self.screen, self.red, (*top_left, rect_width, rect_height), 2)

    def run(self):
        white = (255, 255, 255)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Clear screen
            self.screen.fill('white')

            # Draw axes
            #self.draw_axes()
            self.draw_coords()
            # Draw rectangle
            #self.draw_rectangle(self.hz)
            self.draw_body()

            # Update display
            pygame.display.flip()

            # Control frame rate
            self.clock.tick(60)  # Run at 60 frames per second

        pygame.quit()

if __name__=="__main__":
    # Create an instance of the FlightSimulator class and run it
    simulator = FlightSimulator()
    simulator.run()
