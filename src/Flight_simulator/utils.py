import math

def project_3D_to_2D(_x,_y,_z,alfa=30):
    a = alfa*math.pi/180
    x = _y - _x*math.cos(a)
    y = -_z + _x*math.sin(a)
    return (int(x),int(y))