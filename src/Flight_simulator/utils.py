import math

def project_3D_to_2D(_x,_y,_z,alfa=30):
    x = _y - _x*math.cos(alfa)
    y = -_z + _x*math.sin(alfa)
    return (int(x),int(y))