import pygame
import math
from src.Flight_simulator.utils import project_3D_to_2D

class Drone:
    def __init__(self,initial_position=[0,0,0],initial_orientation=[0,0,0],length_width_height = [90,60,20]):
        self.initial_position = initial_position
        self.initial_orientation = initial_orientation
        self.length = length_width_height[0]
        self.width = length_width_height[1]
        self.height = length_width_height[2]

        self.position = self.initial_position
        self.orientation = None
        pass

    def update_status(self,gyro,h):
        self.position[2] = h
        self.orientation = gyro

        pass

    def draw_object(self,screen,center_position):
        angles = self.orientation
    
        vr = math.sqrt(angles[0] ** 2 + angles[1] ** 2 + angles[2] ** 2)
        if vr > 0:
            theta = math.acos(angles[2] / vr)
            phi = math.atan2(angles[1], angles[0])
        else:
            theta, phi = 0, 0

        print(f"vr: {vr}\t\ttheta: {theta}\tphi:{phi}\t\tangles: {angles}")
        
        # Corrected vertices calculation
        vertices = [
            [-self.length, self.position[2], -self.width],
            [-self.length, self.position[2], self.width],
            [self.length, self.position[2], self.width],
            [self.length, self.position[2], -self.width],
            [-self.length, self.position[2] + self.height, -self.width],
            [-self.length, self.position[2] + self.height, self.width],
            [self.length, self.position[2] + self.height, self.width],
            [self.length, self.position[2] + self.height, -self.width]
        ]

        # Apply rotation
        rotated_vertices = []
        for vertex in vertices:
            x, y, z = vertex
            rotated_x = x * math.cos(theta) * math.cos(phi) - y * math.sin(theta) + z * math.cos(theta) * math.sin(phi)
            rotated_y = x * math.sin(theta) * math.cos(phi) + y * math.cos(theta) + z * math.sin(theta) * math.sin(phi)
            rotated_z = -x * math.sin(phi) + z * math.cos(phi)
            rotated_vertices.append([rotated_x, rotated_y, rotated_z])

        edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]

        for edge in edges:
            start = project_3D_to_2D(rotated_vertices[edge[0]][0], rotated_vertices[edge[0]][1], rotated_vertices[edge[0]][2])
            end = project_3D_to_2D(rotated_vertices[edge[1]][0], rotated_vertices[edge[1]][1], rotated_vertices[edge[1]][2])
            pygame.draw.line(screen, "blue", (center_position[0] + start[0], center_position[1] + start[1]), (center_position[0] + end[0], center_position[1] + end[1]), 2)
        pass