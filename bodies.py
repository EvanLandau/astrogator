#Class for astronomical bodies
import numpy

class Body: #Class representing all astronomical bodies.
    #position = Position x, y, z (in AU)
    #velocity = Velocity x, y, z (in AU/day)
    #mass = mass in kg
    #ID number- used for HORIZONS (also- this is the correct way to check identities of objects, since ID must be unique)
    #Force = Force applied to the object at any given time in newtons
    def __init__(self, name, number, mass, x, y, z, dx, dy, dz):
        self.name = name
        self.id_number = number
        self.position = numpy.array([x, y, z])
        self.velocity = numpy.array([dx, dy, dz])
        self.mass = mass

class Ship(Body): #Class for bodies that undergo thrust (i.e. spacecraft)
    #T, N, B are all unit vectors defining a TNB frame
    def calc_frame(self, acceleration):
        Tr = self.velocity #r'
        self.T = Tr/numpy.linalg.norm(Tr) #T = r'/|r'|
        Nr = numpy.cross(self.velocity, (numpy.cross(acceleration, self.velocity))) #r' x (r'' x r')
        self.N = Nr/(numpy.linalg.norm(self.velocity)*numpy.linalg.norm(numpy.cross(acceleration, self.velocity))) #N = (r' x (r'' x r'))/(|r'||r'' x r'|)
        self.B = numpy.cross(self.T, self.N)