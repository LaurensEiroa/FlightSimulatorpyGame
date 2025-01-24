import pygame
import pygame.camera
from pygame.locals import *
import numpy as np
import cv2
from config import Config

from src.coms.udp.udp_reciever import UDPReceiver
from src.Flight_simulator.utils import project_3D_to_2D

def numpy_to_surface(array):
    return pygame.surfarray.make_surface(array)

class Drone:
    def __init__(self,receiver,init_position=[0.,0.,0.],init_angle=[0.,0.,0.],length_width_height = [90,60,20]):
        self.position = np.asarray(init_position)
        self.angle = np.asarray(init_angle)
        self.length_width_height = np.asarray(length_width_height)
        self.udp_data_receiver = UDPReceiver(receiver_ip=Config.IPs[receiver], port=Config.UDP_DATA_PORT)
        self.udp_frame_receiver = UDPReceiver(receiver_ip=Config.IPs[receiver], port=Config.UDP_FRAME_PORT)
        self.frame = None

    def display_camera(self, screen, position=(0, 0)):
        try:
            surface = numpy_to_surface(self.frame)
            screen.blit(surface, position)
        except ValueError:
            print("Non valid surface")

    async def get_drone_view(self):
        frame = await self.udp_frame_receiver.receive_data(data_type="frame")
        if frame:
            np_frame = np.frombuffer(frame, dtype=np.uint8)
            # Decode frame
            self.frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)

    async def get_drone_data(self):
        data = await self.udp_data_receiver.receive_data(data_type="data")
        if data:
            data = data.decode('utf-8')
            angle, position = data.split("$$$")[0],data.split("$$$")[1]
            angle, position = angle.split("//"), position.split("//")
            self.angle = np.asarray([float(a) for a in angle])
            self.position = np.asarray([float(p) for p in position])

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
            rotated_vectors.append(rotated_vector)
        return np.asarray(rotated_vectors)


    def draw_object(self,screen,center_position):
        axis_length = 30
        # vertices of object
        vertices = np.asarray([
            [-self.length_width_height[0],  -self.length_width_height[1],   self.position[2]],
            [-self.length_width_height[0],  self.length_width_height[1],    self.position[2]],
            [self.length_width_height[0],   self.length_width_height[1],    self.position[2]],
            [self.length_width_height[0],   -self.length_width_height[1],   self.position[2]],
            [-self.length_width_height[0],  -self.length_width_height[1],   self.position[2] + self.length_width_height[2]],
            [-self.length_width_height[0],  self.length_width_height[1],    self.position[2] + self.length_width_height[2]],
            [self.length_width_height[0],   self.length_width_height[1],    self.position[2] + self.length_width_height[2]],
            [self.length_width_height[0],   -self.length_width_height[1],   self.position[2] + self.length_width_height[2]],
            # Drone axes
            [0,             0,              self.position[2] + self.length_width_height[2]],
            [axis_length,   0,              self.position[2] + self.length_width_height[2]],
            [0,             axis_length,    self.position[2] + self.length_width_height[2]],
            [0,             0,              self.position[2] + self.length_width_height[2] + axis_length],
        ])

        rotated_vertices = self.apply_rotation(vertices)

        edges = np.asarray([[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7],
                            [8,9],[8,10],[8,11]])

        for i, (x,y) in enumerate(edges):
            start = project_3D_to_2D(rotated_vertices[x,0], rotated_vertices[x,1], rotated_vertices[x,2])
            end = project_3D_to_2D(rotated_vertices[y,0], rotated_vertices[y,1], rotated_vertices[y,2])
            if i >= edges.shape[0]-3:
                color = "green"
            else:
                color = "blue"
            pygame.draw.line(screen, color, (center_position[0] + start[0], center_position[1] + start[1]), (center_position[0] + end[0], center_position[1] + end[1]), 2)






