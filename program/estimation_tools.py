#Tools for estimating asteroid size, given magnitude (and ideally albdeo as well)

import math

def estimate_radius(magnitude, albedo = 0.2): #Equation taken from http://www.physics.sfasu.edu/astro/asteroids/sizemagnitude.html
    magic_number = 1329/2
    return (magic_number/math.sqrt(albedo))*(10**(-0.2*magnitude))

def estimate_mass(magnitude, spectral_type, albedo = 0.2): #Some equations from https://en.wikipedia.org/wiki/Standard_asteroid_physical_characteristics
    radius = estimate_radius(magnitude, albedo)
    #Densities are estimated based on spectral type, defaulting to the moderate value. Values in g/cm^3
    if (spectral_type == "C"):
        density = 1.38 * 1000
    if (spectral_type == "M"):
        density = 5.32 * 1000
    else:
        density = 2.71 * 1000
    mass = math.pi * ((2*radius) ** 3) * density / 6
    return mass