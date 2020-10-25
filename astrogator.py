#Main simulation running file
import simulator
import downloader
import argparse
import datetime
import maneuver

def current_time_julian(): #Returns it in Julian Date
    my_date = datetime.datetime.utcnow() #Gets current date and time
    reference_date = datetime.datetime(1858, 11, 17) #Create a reference date on, November 17, 1858 (Modified Julian date start time)
    MJD = my_date - reference_date #Days since
    return MJD / datetime.timedelta(days=1) + 2400000.5 #Convert difference to days, add to get to JD from MJD

def main(): #Main function
    #Argument parser setup - defines arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("maneuverfile", type=str, help="Name of maneuver file") #TODO: Write maneuver file format/documentation
    parser.add_argument("-l", "--steplength", type=int, default=3600, help="Sets explicit steplength in seconds, otherwise default value will be used.") #TODO: Determine default steplength
    parser.add_argument("-s", "--starttime", type=float, default=current_time_julian(), help="Start time for simulation in julian date, otherwise will start at current date.")
    parser.add_argument("-e", "--endtime", type=float, help="Sets end time for simulation in julian date, otherwise simulation will stop after completion of maneuvers.")
    args = parser.parse_args()
    #Basic setup
    time = args.starttime
    #Load maneuver file & maneuvers
    #TODO: Get ship location & info and create body file
    #TODO: Produce maneuver list "manuevers"
    #Load body files
    print ("Downloading solar system bodies...")
    body_list = downloader.download_all(time)
    print("Download finished.")
    #Simulation loop
    try: #Tests if endtime exists- this should be removed once maneuvers are supported
      endtime
    except NameError:
        print("Simulation end time not set.") #End code to be removed
    while True:
        time += args.steplength
        body_list = simulator.simulate(body_list, args.steplength)
        #TODO: Include spacecraft maneuvers
        print(time)
        if time >= args.endtime:
            break

main()