#Class for astronomical bodies
import numpy
from math import sqrt, sin, cos, tan, asin, acos, atan

G = 6.67300E-11 #Gravitational constant

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
    def eccentric_anomaly(self, M, e) -> float: #Numerically solves Kepler's equation (E - e sin(E) = M(E)), using Newton's method
        iteration_limit = 10
        estimate = M + 0.85 * e
        for i in range(0, iteration_limit):
            estimate = estimate - (estimate - e * sin(estimate) - M)/(1 - e * cos(estimate))
        return estimate
        
    def calc_xyz(self, parent: Body, e, a, M, i, omega, Omega) -> None: #Convert orbital elements to x, y, z coords, using method here: https://downloads.rene-schwarz.com/download/M001-Keplerian_Orbit_Elements_to_Cartesian_State_Vectors.pdf
        E = self.eccentric_anomaly(M, e)
        nu = 2 * atan(sqrt((1 + e)/(1 - e)*tan(E/2)))
        mu = parent.mass * G
        r = a*(1 - e * cos(E))
        o = r * numpy.array([cos(nu), sin(nu), 0])
        do = sqrt(mu * a) / r * numpy.array([-sin(E), sqrt(1-e^2) * cos(E), 0])
        #Convert from orbital frame to bodycentric frame
        x = o[0] * (cos(omega) * cos(Omega) - sin(omega) * cos(i) * sin(Omega)) - o[1] * (sin(omega) * cos(Omega) + cos(omega) * cos(i) * sin(Omega))
        y = o[0] * (cos(omega) * sin(Omega) + sin(omega) * cos(i) * cos(Omega)) - o[1] * (cos(omega) * cos(i) * cos(Omega) - sin(omega) * sin(Omega))
        z = o[0] * (sin(omega) + sin(i)) + o[1] * (cos(omega) * sin(i))
        dx = do[0] * (cos(omega) * cos(Omega) - sin(omega) * cos(i) * sin(Omega)) - do[1] * (sin(omega) * cos(Omega) + cos(omega) * cos(i) * sin(Omega))
        dy = do[0] * (cos(omega) * sin(Omega) + sin(omega) * cos(i) * cos(Omega)) - do[1] * (cos(omega) * cos(i) * cos(Omega) - sin(omega) * sin(Omega))
        dz = do[0] * (sin(omega) + sin(i)) + do[1] * (cos(omega) * sin(i))
        #Convert to system frame and store
        self.position = numpy.array([x + parent.position[0], y + parent.position[1], z + parent.position[2]])
        self.velocity = numpy.array([dx + parent.velocity[0], dy + parent.velocity[1], dz + parent.velocity[2]])
        
    def __init__(self, name, number, mass, parent, e, a, M, i, omega, Omega):
        self.name = name
        self.id_number = number
        self.mass = mass
        self.maneuvers = [] #Empty list for maneuver objects, which can be added elsewhere
        self.calc_xyz(parent, e, a, M, i, omega, Omega)

    #T, N, B are all unit vectors defining a TNB frame - this frame will be used for doing maneuvers later
    def calc_frame(self, acceleration) -> None:
        Tr = self.velocity #r'
        self.T = Tr/numpy.linalg.norm(Tr) #T = r'/|r'|
        Nr = numpy.cross(self.velocity, (numpy.cross(acceleration, self.velocity))) #r' x (r'' x r')
        self.N = Nr/(numpy.linalg.norm(self.velocity)*numpy.linalg.norm(numpy.cross(acceleration, self.velocity))) #N = (r' x (r'' x r'))/(|r'||r'' x r'|)
        self.B = numpy.cross(self.T, self.N)
    