import math

def project_3D_to_2D(_x,_y,_z,alfa=30):
    x = _x - _z*math.sin(alfa)
    y = _y + _z*math.cos(alfa)
    return (int(x),-int(y))