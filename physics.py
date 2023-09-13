import math


g = 0.0000000000667408

#test


def gravity(mass1, x1, y1, mass2, x2, y2):
    # F = ( GMm ) / r^2
    # Newtons
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) + 0.1
    g = 0.0000000000667408
    fg = g * ((mass1 * mass2) / dist ** 2)
    theta = math.atan2(y2 - y1, x2 - x1)
    return fg * math.cos(theta), fg * math.sin(theta)




def centripetal():
    pass




def torque(length,force_vector):
    #t = F*r*sin(theta)
    pass




def ang_acceleration(torque,shape):
    pass




def acceleration(mass, fx, fy):
    return fx / mass, fy / mass




def collision2d(v1x,v1y,v2x,v2y,m1,m2,ang_norm_to_surf):
    phi = math.radians(ang_norm_to_surf)
    theta1 = math.radians(Vector(v1x,v1y)[1])
    theta2 = math.radians(Vector(v2x,v2y)[1])
    v1fx = ((Vector(v1x,v1y)[0]*math.cos(theta1-phi)*(m1-m2)+2*m2*Vector(v2x,v2y)[0]*math.cos(theta2-phi))/(m1+m2))*math.cos(phi)+Vector(v1x,v1y)[0]*math.sin(theta1-phi)*math.cos(phi+math.pi/2)
    v1fy = ((Vector(v1x,v1y)[0]*math.cos(theta1-phi)*(m1-m2)+2*m2*Vector(v2x,v2y)[0]*math.cos(theta2-phi))/(m1+m2))*math.sin(phi)+Vector(v1x,v1y)[0]*math.sin(theta1-phi)*math.sin(phi+math.pi/2)
    v2fx = (m1*v1x+m2*v2x-m1*v1fx)/m2
    v2fy = (m1*v1y+m2*v2y-m1*v1fy)/m2
    return round(v1fx,2), round(v1fy,2), round(v2fx,2), round(v2fy,2)




def quadratics(vel, direction:'degrees', mass:'planet', increments, x, y, start, stop, height, scale, blitx, blity, force=None, rounded=False):
    if force:
        k = -((vel * math.sin(math.radians(direction)))**2) / (2 * force)
    else:
        k = -((vel * math.sin(math.radians(direction)))**2) / (2 * -((g * mass) / height**2))
    if force:
        if rounded:
            tta = -vel*math.sin(math.radians(direction)) / force
        else:
            tta = -vel*math.sin(math.radians(direction)) / force
    else:
        tta = -vel*math.sin(math.radians(direction)) / -((g * mass) / height**2)
    if rounded:
        h = vel * math.cos(math.radians(direction)) * round(tta)
    else:
        h = vel * math.cos(math.radians(direction)) * tta
    a = (-y - k) / (x - h)**2
    return [(xn / scale + blitx, ((a*(xn - h)**2 + k) / scale - blity)*-1) for xn in range(start, stop, increments)]




def projectile(ivel, ivel_direction, acceleration, iterations, blitx, blity, scale):
    # graphs projectile motion with x relative to time and y relative to time
    vix = ivel * math.cos(math.radians(ivel_direction))
    viy = ivel * math.sin(math.radians(ivel_direction))
    y_graph = [-((viy * t + acceleration/2 * t ** 2 / scale + blity)) for t in range(iterations)]
    x_graph = [(vix * t) / scale + blitx for t in range(iterations)]
    return list(zip(x_graph, y_graph))




#For pygame coordinates
def VectorDecomposition(magnitude,direction:'degrees'):
    return magnitude*math.sin(math.radians(direction)), magnitude*math.cos(math.radians(direction))




#For cartesian coordinates
def VectorDecomposition2(magnitude, direction:'degrees'):
    return magnitude*math.cos(math.radians(direction)), magnitude*math.sin(math.radians(direction))




def Vector(x,y):
    #Forms vector from x and y components
    #returns magnitude, direction in degrees
    return math.sqrt(x**2 + y**2), math.degrees(math.atan2(y,x))




def VectorAddition(vec1,vec2):
    return vec1[0]+vec2[0],vec1[1]+vec2[1]




def VectorSubtract(vec1,vec2):
    return vec1[0]-vec2[0],vec1[1]-vec2[1]




def Scale(vec,scaler):
    return vec[0]*scaler,vec[1]*scaler


def normalize(vec):
    mag = math.sqrt(vec[0]**2+vec[1]**2)
    return vec[0]/mag,vec[1]/mag




class Vec2D:


    def __init__(self,x,y):
        self.vector = [x,y]
   
    def __repr__(self):
        return str(self.vector)
   
    def __iter__(self):
        yield from self.vector


    def __add__(self,vec2):
        return Vec2D(*VectorAddition(self.vector,vec2.vector))
   
    def __sub__(self,vec2):
        return Vec2D(*VectorSubtract(self.vector,vec2.vector))
   
    def __mul__(self,scaler):
        return Vec2D(*Scale(self.vector,scaler))
   
    def magnitude(self):
        return Vector(*self.vector)[0]


    def direction(self):
        return Vector(*self.vector)[1]
   
    def normalize(self):
        self.vector = list(normalize(self.vector))




def CG(objs):
    #List of objects
    #[(x,y,weight)]
    # returns x and y
    upperx = 0
    uppery = 0
    for obj in objs:
        upperx = obj[0]*obj[2]
        uppery = obj[1]*obj[2]
    lower = [i[2] for i in objs]
    upperx /= math.fsum(lower)
    uppery /= math.fsum(lower)


    return upperx, uppery
   


#Calculate forces acting on a object and outputs updated x and y coords
class Object:


    def __init__(self,objects=None):
        self.objects = objects


    def update(self,list_objects):
        self.objects = list_objects


if __name__ == '__main__':
    #Testing
    collide = collision2d(3,0,0,0,10,5,-30)
    print(Vector(collide[0],collide[1]))
    vector = Vec2D(3,5)
    vector2 = Vec2D(1,2)
    print("vec1",vector)
    print("vec2",vector2)
    print(vector)
    vector = vector2 + vector
    print(vector)
    vector -= vector2
    print(vector)
    vector.normalize()
    print(vector)
    for component in vector2:
        print(component)
    for component in vector2.vector:
        print(component)
