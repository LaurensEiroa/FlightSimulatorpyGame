import pygame
import math
import numpy as np
from src.Flight_simulator.utils import project_3D_to_2D

class FlightSimulator:
    def __init__(self,size = (800,600),objects=[None]):
        self.objects = objects
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

    
    def draw_coords(self):
        length = 1000
        end_x_axis = project_3D_to_2D(length,0,0)
        pygame.draw.line(self.screen,"red",self.center,(self.center[0]+end_x_axis[0],self.center[1]+end_x_axis[1]),2)
        end_y_axis = project_3D_to_2D(0,length,0)
        pygame.draw.line(self.screen,"red",self.center,(self.center[0]+end_y_axis[0],self.center[1]+end_y_axis[1]),2)
        end_z_axis = project_3D_to_2D(0,0,length)
        pygame.draw.line(self.screen,"red",self.center,(self.center[0]+end_z_axis[0],self.center[1]+end_z_axis[1]),2)

    def update_screen(self):
        # Clear screen
            self.screen.fill('white')
            # Draw axes
            self.draw_coords()
            # Draw objects
            for obj in self.objects:
                obj.draw_object(self.screen,self.center)
                obj.display_webcam(self.screen)
            # Update display
            pygame.display.flip()

    def record_event(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def test(self):
        import numpy as np
        steps = 1000
        vy, vz,h = np.linspace(0,6*math.pi,steps), np.linspace(0,2*math.pi,steps),np.ones(steps)
        #vz,h = np.ones(steps),np.ones(steps)
        t = -1
        while self.running:
            t+=1
            self.objects[0].update_status([0,vy[t],vz[t]],h[t])
            self.record_event()
            self.update_screen()
            # Control frame rate
            self.clock.tick(60)  # Run at 60 frames per second
            if t == steps:
                 pygame.quit()

        pygame.quit()

    async def run(self):
        while self.running:
            await self.objects[0].get_drone_data()
            self.record_event()
            self.update_screen()
            # Control frame rate
            self.clock.tick(60)  # Run at 60 frames per second
        pygame.quit()

if __name__=="__main__":
    # Create an instance of the FlightSimulator class and run it
    from src.Flight_simulator.drone import Drone
    drone = Drone()
    simulator = FlightSimulator(objects=[drone])
    simulator.run()
