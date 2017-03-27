import math

REACTION_TIME = 1.5 #in seconds includes both perception and realization
ROAD_FRICTION_COEFF = 0.7 #unitless
ACCELERATION_GRAVITY = 9.8 #in m/s^2

#speed in mph return distance in ft
def getReactionDistance(speed):
    reactionDistance = REACTION_TIME * speed * (22/15)
    return reactionDistance

#speed in mph return distance in ft
def getStoppingDistance(speed):
    s = speed * 0.44704 #convert to m/s
    stoppingDistance = (math.pow(s,2))/(2 * \
                       ACCELERATION_GRAVITY * \
                       ROAD_FRICTION_COEFF) #stopping distance in meters
    return stoppingDistance * 3.28084 #meters to ft

#sum of Reaction distance + stopping distance in ft
def getSafeDistance(speed):
    safeDistance = getReactionDistance(speed) + \
                   getStoppingDistance(speed)
    return safeDistance
