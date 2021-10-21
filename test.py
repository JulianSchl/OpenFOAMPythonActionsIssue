mySourceData = 0
myTargetData = 0

def performAction(time, dt, sourceData, targetData):

    # This function is called first at configured timing. It can be omitted, if not
    # needed. Its parameters are time, timestep size, the source data, followed by the target data.
    # Source and target data can be omitted (selectively or both) by not mentioning
    # them in the preCICE XML configuration.

    global mySourceData
    global myTargetData

    mySourceData = sourceData # store (reference to) sourceData for later use
    myTargetData = targetData # store (reference to) targetData for later use

    timeThreshold = 0.2 # Ramp up the pressure values until this point in time

    if time < timeThreshold:
        for i in range(myTargetData.size):
        # Ramp up pressure value
            myTargetData[i] = (time / timeThreshold) * mySourceData[i]

    else:
        for i in range(myTargetData.size):
            # Assign the computed physical pressure values
            myTargetData[i] = mySourceData[i]


def vertexCallback(id, coords, normal):
    # This function is called for every vertex in the configured mesh. It is called
    # after performAction, and can also be omitted.

    # Usage example:
    global mySourceData # Make global data set in performAction visible
    global myTargetData
    # Example usage, add data to vertex coords:
    # myTargetData[id] += coords[0] + mySourceData[id] 

def postAction():
    # This function is called at last, if not omitted.

    global mySourceData # Make global data set in performAction visible
    global myTargetData
    # Do something ...
