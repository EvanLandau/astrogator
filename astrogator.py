#Main simulation running file
import simulator
import downloader
import argparse
import datetime
import maneuver

def current_time_julian(): #Thank you to Code Highlights https://code-highlights.blogspot.com/2013/01/julian-date-in-python.html
    my_date = datetime.datetime.now() #Gets current date and time
    a = (14 - my_date.month)//12
    y = my_date.year + 4800 - a
    m = my_date.month + 12*a - 3
    return my_date.day + ((153*m + 2)//5) + 365*y + y//4 - y//100 + y//400 - 32045

def main(): #Main function
    #Argument parser setup - defines arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("maneuverfile", type=str, help="Name of maneuver file") #TODO: Write maneuver file format/documentation
    parser.add_argument("-l", "--steplength", type=int, default=3600, help="Sets explicit steplength in seconds, otherwise default value will be used.") #TODO: Determine default steplength
    parser.add_argument("-s", "--starttime", type=float, default=current_time_julian(), help="Start time for simulation in MJD, otherwise will start at current date.")
    parser.add_argument("-e", "--endtime", type=float, help="Sets end time for simulation in MJD, otherwise simulation will stop after completion of maneuvers.")
    args = parser.parse_args()
    #Basic setup
    time = args.starttime
    #Load maneuver file & maneuvers
    #TODO: Get ship location & info and create body file
    #TODO: Produce maneuver list "manuevers"
    #Load body files
    body_list = downloader.download_all(time)
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