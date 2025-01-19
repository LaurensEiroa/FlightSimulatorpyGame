import pygame
import math

class FlightSimulator:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

        # Colors
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        
        # Rectangle height
        self.center = (400, 300)
        self.hz = 100

    def draw_axes(self):
        length = 200

        # Draw X axis (red)
        pygame.draw.line(self.screen, self.red, self.center, (self.center[0] + length, self.center[1]), 2)
        pygame.draw.line(self.screen, self.red, (self.center[0] + length, self.center[1]), (self.center[0] + length - 10, self.center[1] - 10), 2)
        pygame.draw.line(self.screen, self.red, (self.center[0] + length, self.center[1]), (self.center[0] + length - 10, self.center[1] + 10), 2)

        # Draw Y axis (green)
        pygame.draw.line(self.screen, self.green, self.center, (self.center[0], self.center[1] - length), 2)
        pygame.draw.line(self.screen, self.green, (self.center[0], self.center[1] - length), (self.center[0] - 10, self.center[1] - length + 10), 2)
        pygame.draw.line(self.screen, self.green, (self.center[0], self.center[1] - length), (self.center[0] + 10, self.center[1] - length + 10), 2)

        # Draw Z axis (blue)
        pygame.draw.line(self.screen, self.blue, self.center, (self.center[0] - length // 2, self.center[1] + length // 2), 2)

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
            self.draw_axes()

            # Draw rectangle
            self.draw_rectangle(self.hz)

            # Update display
            pygame.display.flip()

            # Control frame rate
            self.clock.tick(60)  # Run at 60 frames per second

        pygame.quit()

if __name__=="__main__":
    # Create an instance of the FlightSimulator class and run it
    simulator = FlightSimulator()
    simulator.run()
