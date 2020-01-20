#The actual simulator that moves bodies in steps
G = 6.67300E-11 #Gravitational constant
import bodies
import numpy

def simulate(bodies, step_length): #Body array and step length, in seconds
    energy = 0 #Calculates kinetic energy of the system
    for i in bodies: #Calculate sum of gravitational forces on each object
        i.force = numpy.array([0.0, 0.0, 0.0])
        for j in bodies:
            if i.id_number != j.id_number: #F = Gmm/r^3*r^
                dx = i.position[0] - j.position[0]
                dy = i.position[1] - j.position[1]
                dz = i.position[2] - j.position[2]
                r = numpy.array([dx, dy, dz])
                i.force += (G * i.mass * j.mass)/(numpy.linalg.norm(r)**3)*r

        #Put code for thruster burns here when working with spacecraft (this may require some minor tweaks to earlier code)
    for i in bodies: #Integrate force/acceleration to create velocity
        acceleration = i.force/i.mass
        i.position += i.velocity * step_length + acceleration / 2 * step_length ** 2 #d = 0.5at^2 + vt + d
        i.velocity += acceleration * step_length
        energy += numpy.linalg.norm(i.velocity) ** 2 * i.mass/2 #Kinetic energy added
    print(energy)
    return bodies