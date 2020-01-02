#Class for astronomical bodies

class Body: #Class representing all astronomical bodies.
    position = [0, 0, 0] #Position x, y, z (in AU)
    velocity = [0, 0, 0] #Velocity x, y, z (in AU/day)
    mass = 0
    IAU_number = -1
    def __init__(self, name, number, mass, x, y, z, dx, dy, dz):
        self.name = name
        self.IAU_number = number
        self.position = [x, y, z]
        self.velocity = [dx, dy, dz]
        self.mass = mass
    