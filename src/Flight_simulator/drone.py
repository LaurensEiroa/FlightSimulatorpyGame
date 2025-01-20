import pygame
import pygame.camera
from pygame.locals import *
import numpy as np

from src.Flight_simulator.utils import project_3D_to_2D


class Drone:
    def __init__(self,init_position=[0,0,0],init_angle=[0,0,0],length_width_height = [90,60,20]):
        self.position = np.asarray(init_position)
        self.angle = np.asarray(init_angle)
        self.length_width_height = np.asarray(length_width_height)
        self.cam = self.init_camera()

    def init_camera(self,window=(180,120)):
        pygame.camera.init()
        camlist = pygame.camera.list_cameras()
        if not camlist:
            raise ValueError("Sorry, no cameras detected.")
        cam = pygame.camera.Camera(camlist[0], window)
        cam.start()
        return cam

    def display_webcam(self, screen, position=(0, 0)):
        webcam_image = self.cam.get_image()
        screen.blit(webcam_image, position)

    def drone_to_3d_reference_frame_transform(self, gyro_readings):
        return np.asarray([-gyro_readings[1],gyro_readings[0],gyro_readings[2]])
    
    def update_orientation(self,rotation_3d_frame):
        self.angle = rotation_3d_frame # TODO += or = ??

    def update_heigth(self,h):
        self.position[2] = h

    def update_status(self,rotation,h):
        rotation_3d_frame = self.drone_to_3d_reference_frame_transform(rotation)
        self.update_orientation(rotation_3d_frame)
        self.update_heigth(h)
        pass

    def apply_rotation(self,vectors):
        x_rotation = np.asarray([   [1,   0,                        0                     ],
                                    [0,   np.cos(self.angle[0]),    -np.sin(self.angle[0]) ],
                                    [0,   np.sin(self.angle[0]),    np.cos(self.angle[0]) ]
        ])
        y_rotation = np.asarray([   [np.cos(self.angle[1]), 0,  np.sin(self.angle[1]) ],
                                    [0,                     1,  0                     ],
                                    [-np.sin(self.angle[1]), 0,  np.cos(self.angle[1]) ]
        ])
        z_rotation = np.asarray([   [np.cos(self.angle[2]), -np.sin(self.angle[2]),    0],
                                    [np.sin(self.angle[2]), np.cos(self.angle[2]),    0],
                                    [0,                       0,                      1]
        ])
        rotated_vectors = []
        for vector in vectors:
            rotated_vector =  z_rotation @ y_rotation @ x_rotation @ vector
            print(f"original_vector {vector}\trotated_vector {rotated_vector}")
            rotated_vectors.append(rotated_vector)

        return np.asarray(rotated_vectors)


    def draw_object(self,screen,center_position):
        
        # vertices of object
        vertices = np.asarray([
            [-self.length_width_height[0],  -self.length_width_height[1],   self.position[2]],
            [-self.length_width_height[0],  self.length_width_height[1],    self.position[2]],
            [self.length_width_height[0],   self.length_width_height[1],    self.position[2]],
            [self.length_width_height[0],   -self.length_width_height[1],   self.position[2]],
            [-self.length_width_height[0],  -self.length_width_height[1],   self.position[2] + self.length_width_height[2]],
            [-self.length_width_height[0],  self.length_width_height[1],    self.position[2] + self.length_width_height[2]],
            [self.length_width_height[0],   self.length_width_height[1],    self.position[2] + self.length_width_height[2]],
            [self.length_width_height[0],   -self.length_width_height[1],   self.position[2] + self.length_width_height[2]]
        ])

        rotated_vertices = self.apply_rotation(vertices)

        edges = np.asarray([[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]])

        for x,y in edges:
            start = project_3D_to_2D(rotated_vertices[x,0], rotated_vertices[x,1], rotated_vertices[x,2])
            end = project_3D_to_2D(rotated_vertices[y,0], rotated_vertices[y,1], rotated_vertices[y,2])
            pygame.draw.line(screen, "blue", (center_position[0] + start[0], center_position[1] + start[1]), (center_position[0] + end[0], center_position[1] + end[1]), 2)






