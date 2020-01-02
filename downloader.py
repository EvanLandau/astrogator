#Function that actually downloads a given body's data
#Takes in the body's IAU number, and the start time in MJD (and mass in kilograms, if a major body), returns a body object

import bodies
import estimation_tools
#Uses astroquery
from astroquery.jplhorizons import Horizons

def download_Body(name, number, time, mass = -1):
    majorbody = (mass != -1) #Tests if a mass value is provided, and if it is, marks body as major
    if majorbody: #Creates actual body in astroquery
        working_body = Horizons(id=str(number), epochs=time, id_type='majorbody')
    else:
        working_body = Horizons(id=str(number), epochs=time) 
    body_table = working_body.vectors() #Returns astropy table of position/velocity vectors
    if (mass == -1): #Estimates mass using function in estimation_tools.py
        mass = estimation_tools.estimate_mass(body_table['H'][0], 'x')
    return bodies.Body(name, number, mass, body_table['x'][0], body_table['y'][0], body_table['z'][0], body_table['vx'][0], body_table['vy'][0], body_table['vz'][0])
