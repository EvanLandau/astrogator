#Main simulation running file
import simulator
import downloader
import argparse
import datetime
import bodies
import maneuver

def current_time_julian(): #Returns it in Julian Date
    my_date = datetime.datetime.utcnow() #Gets current date and time
    reference_date = datetime.datetime(1858, 11, 17) #Create a reference date on, November 17, 1858 (Modified Julian date start time)
    MJD = my_date - reference_date #Days since
    return MJD / datetime.timedelta(days=1) + 2400000.5 #Convert difference to days, add to get to JD from MJD

def main(): #Main function
    #Argument parser setup - defines arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", type=str, help="Name of user data file, see documentation") #TODO: Write maneuver file format/documentation
    parser.add_argument("-l", "--steplength", type=int, default=3600, help="Sets explicit steplength in seconds, otherwise default value will be used.") #TODO: Determine default steplength
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
    #TODO: Get ship location & info and create body file
    shipstart = in_data.index(['#SHIP'])
    shipend = in_data.index(['#ENDSHIP'])
    for i in range(shipstart, shipend):
        row = in_data[i]
        if len(row) == 9:
            id_num = -(len(ship_ids) + 1)
            ship_ids.update({row[0]:id_num})
            created_ship = bodies.Ship(row[0], id_num, row[1], body_dict[row[2]], row[3], row[4], row[5], row[6], row[7], row[8]) #TODO: Turn things into correct values
            ship_list += created_ship
            body_dict.update({created_ship.id_number:created_ship})
    #TODO: Load maneuver file & maneuvers, create maneuver list
    maneuver_list = []
    maneuverstart = in_data.index(['#MANEUVER'])
    maneuverend = in_data.index(['#ENDMANEUVER'])
    for i in range(maneuverstart, maneuverend):
        row = in_data[i]
        if len(row == 6):
            ship_id = ship_ids[row[0]]
            maneuver_list += maneuver.Maneuver(ship_id, row[1], row[2], row[3], row[4], row[5])
    #Simulation loop
    try: #Tests if endtime exists- this should be removed once maneuvers are supported
      endtime
    except NameError:
        print("Simulation end time not set.") #End code to be removed
    while True:
        time += args.steplength
        body_list = simulator.simulate(body_dict, maneuver_list, args.steplength)
        #TODO: Include spacecraft maneuvers
        print(time)
        if time >= args.endtime:
            break

main()