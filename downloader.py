#Function that actually downloads a given body's data
#Takes in the body's IAU number, and the start time in MJD (and mass in kilograms, if a major body), returns a body object
import os
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
    return bodies.Body(name, number, float(mass), float(body_table['x'][0]), float(body_table['y'][0]), float(body_table['z'][0]), float(body_table['vx'][0]), float(body_table['vy'][0]), float(body_table['vz'][0]))

def download_all(time):
    bodies = [] #List of bodies- what is returned (this will be quite large)
    manifest = open(os.path.join('data', 'object_files'), 'r') #Most of the code here is just to get a relative filepath
    to_read = manifest.read().split() #Gets list of files to read from
    manifest.close()
    for filename in to_read: #Open each file
        body_file = open(os.path.join('data', filename), 'r')
        for line in body_file:
            line = line.split()
            #print("Downloading " + line[0]) #Debug print statment for each body downloaded
            bodies.append(download_Body(line[0], line[1], time=time,mass=line[2]))
    return bodies