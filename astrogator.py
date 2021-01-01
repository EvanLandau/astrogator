#Main simulation running file
import numpy
import downloader
import argparse
import datetime
import bodies
import maneuver

G = 6.67300E-11 #Gravitational constant

def current_time_julian(): #Returns it in Julian Date
    my_date = datetime.datetime.utcnow() #Gets current date and time
    reference_date = datetime.datetime(1858, 11, 17) #Create a reference date on, November 17, 1858 (Modified Julian date start time)
    MJD = my_date - reference_date #Days since
    return MJD / datetime.timedelta(days=1) + 2400000.5 #Convert difference to days, add to get to JD from MJD

def main(): #Main function
    #Argument parser setup - defines arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", type=str, help="Name of user data file, see documentation") #TODO: Write maneuver file format/documentation
    parser.add_argument("-l", "--steplength", type=int, default=3600, help="Sets standard steplength in seconds, otherwise default value will be used. The steplength will be shortened around thruster burns to improve accuracy.") #TODO: Determine default steplength?
    parser.add_argument("-s", "--starttime", type=float, default=current_time_julian(), help="Start time for simulation in julian date, otherwise will start at current date.")
    parser.add_argument("-e", "--endtime", type=float, help="Sets end time for simulation in julian date, otherwise simulation will stop after completion of maneuvers.")
    args = parser.parse_args()
    #Basic setup
    time = args.starttime
    #Load body files
    print ("Downloading solar system bodies...")
    body_dict = downloader.download_all(time)
    print("Download finished.")
    #Getting data from file
    infile = open(args.datafile)
    in_data = [ line.split() for line in infile.readlines() ]
    ship_ids = {}
    ship_list = []
    #Get ship location & info and create body file
    try:
        shipstart = in_data.index(['#SHIP'])
        shipend = in_data.index(['#ENDSHIP'])
    except:
        shipstart = 0
        shipend = 0
    for i in range(shipstart, shipend):
        row = in_data[i]
        if len(row) == 9:
            id_num = -(len(ship_ids) + 1)
            ship_ids.update({row[0]:id_num})
            created_ship = bodies.Ship(row[0], int(id_num), float(row[1]), body_dict[int(row[2])], float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]))
            ship_list += created_ship
            body_dict.update({created_ship.id_number:created_ship})
    #Load maneuver file & maneuvers, create maneuver list
    maneuver_list = []
    try:
        maneuverstart = in_data.index(['#MANEUVER'])
        maneuverend = in_data.index(['#ENDMANEUVER'])
    except:
        maneuverstart = 0
        maneuverend = 0
    for i in range(maneuverstart, maneuverend):
        row = in_data[i]
        if len(row == 6):
            ship_id = ship_ids[row[0]] #Get ship id from name
            direction_list = row[5].strip('[]()').split(',') #Turn direction string into numpy array/vector
            direction = numpy.array([direction_list[0],direction_list[1],direction_list[2]])
            direction = direction / numpy.linalg.norm(direction) #Convert to length 1 to be safe
            maneuver_list += maneuver.Maneuver(ship_id, float(row[1]), float(row[2]), float(row[3]), float(row[4]), direction)
    maneuver_list = sorted(maneuver_list) #Sort by time
    #Simulation loop
    try: #Tests if endtime exists- this should be removed once maneuvers are supported
      endtime
    except NameError:
        print("Simulation end time not set.") #End code to be removed
    steplength = args.steplength
    while True: #Simulation loop
        time += steplength
        energy = 0 #Calculates kinetic energy of the system
        for i in body_dict.values(): #Calculate sum of gravitational forces on each object
            i.force = numpy.array([0.0, 0.0, 0.0])
            for j in body_dict.values():
                if i.id_number != j.id_number: #F = Gmm/|r^3|*r
                    dx = i.position[0] - j.position[0]
                    dy = i.position[1] - j.position[1]
                    dz = i.position[2] - j.position[2]
                    r = numpy.array([dx, dy, dz])
                    i.force += (G * i.mass * j.mass)/(numpy.linalg.norm(r)**3)*r
        #Thruster burn code
        active_burn_list = []
        new_step_length = args.steplength
        for i in range(0, len(maneuver_list)):
            if maneuver_list[i].time >= current_time_julian:
                active_burn_list += i
            else:
                break
        for active_maneuver_id in active_burn_list:
            active_maneuver = maneuver_list[active_maneuver_id]
            #Convert thrust from storage in maneuver to system frame (Sx, Sy, Sz)
            thrustvalues = numpy.multiply(active_maneuver.direction, body_dict[active_maneuver.body_id]) * active_maneuver.mass_flow * active_maneuver.exhaustvel
            Sx = numpy.dot(thrustvalues, numpy.array([1,0,0]))
            Sy = numpy.dot(thrustvalues, numpy.array([0,1,0]))
            Sz = numpy.dot(thrustvalues, numpy.array([0,0,1]))
            body_dict[active_maneuver.body_id].force += numpy.array([Sx, Sy, Sz])
            #Determine more accurate step length
            if active_maneuver.length < new_step_length:
                new_step_length = active_maneuver.length
        for active_maneuver_id in active_burn_list: #Subtract new step length from thrust durations
            body_dict[maneuver_list[active_maneuver_id].body_id].mass -= new_step_length * maneuver_list[active_maneuver_id].mass_flow #Subtract mass change due to mass flow
            if maneuver_list[active_maneuver_id].length > new_step_length:
                maneuver_list[active_maneuver_id] -= new_step_length
            else: #If the maneuver is smaller than or equal to the new step length, remove it from the maneuver list. (In theory it should never be smaller)
                maneuver_list.pop(active_maneuver_id)
        #Integrate force/acceleration to create velocity
        for i in body_dict.values():
            acceleration = i.force/i.mass
            if isinstance(i, bodies.Ship): #Calculate frames for all ship-type bodies (this is done here because acceleration is known here)
                i.calc_frame(acceleration)
            i.position += i.velocity * new_step_length + acceleration / 2 * new_step_length ** 2 #d = 0.5at^2 + vt + d
            i.velocity += acceleration * new_step_length
            energy += numpy.linalg.norm(i.velocity) ** 2 * i.mass/2 #Kinetic energy added
        print(energy, time) #This is used to check if the system gains or loses kinetic energy, and is basically a debug statement
        if time >= args.endtime:
            break
main()