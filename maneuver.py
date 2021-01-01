#Object for individual maneuvers to be performed by the spacecraft

class Maneuver:
    thrust = 0 #Thrust of maneuver, in N
    mass_flow = 0 #Change in mass caused by maneuver, in kg/s
    exhaustvel = 0 #Velocity of exhaust
    direction = (0.0, 0.0, 0.0) #Thrust direction vector, in T, N, B coordinates
    time = 0 #Time in MJD that maneuver should be executed
    length = 0 #Length of maneuver, in seconds
    body_id = -999 #Id of relevant body delta-v will be applied to
    def __init__(self, body_id, time, length, exhaustvel, mass_flow, direction):
        self.exhaustvel = exhaustvel
        self.mass_flow = mass_flow
        self.direction = direction
        self.time = time
        self.length = length
        self.body_id = body_id
        self.thrust = mass_flow * exhaustvel
    
    #Stuff for comparisons, based on time
    def __lt__(self, other):
        if other.time < self.time:
            return True
        else:
            return False
    def __gt__(self, other):
        if other.time > self.time:
            return True
        else:
            return False