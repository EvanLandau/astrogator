#Class for astronomical bodies
import numpy

class Body: #Class representing all astronomical bodies.
    position = numpy.array([0.0, 0.0, 0.0]) #Position x, y, z (in AU)
    velocity = numpy.array([0.0, 0.0, 0.0]) #Velocity x, y, z (in AU/day)
    mass = 0
    id_number = -1 #ID number- used for HORIZONS (also- this is the correct way to check identities of objects, since ID must be unique)
    force = numpy.array([0.0, 0.0, 0.0]) #Force applied to the object at any given time in newtons
    def __init__(self, name, number, mass, x, y, z, dx, dy, dz):
        self.name = name
        self.id_number = number
        self.position = numpy.array([x, y, z])
        self.velocity = numpy.array([dx, dy, dz])
        self.mass = mass