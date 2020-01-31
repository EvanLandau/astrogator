#Object for individual maneuvers to be performed by the spacecraft

class Maneuver:
    delta_v = 0.0 #Change in velocity of object, measured in meters per second
    direction = (0.0, 0.0, 0.0) #Direction of change of velocity relative to prograde (current direction of velocity vector)
    time = 0 #Time in MJD that maneuver should be executed
    body_id = -999 #Id of relevant body delta-v will be applied to
    def __init__(self, delta_v, direction, time, body_id):
        self.delta_v = delta_v
        self.direction = direction
        self. time = time
        self.body_id = body_id