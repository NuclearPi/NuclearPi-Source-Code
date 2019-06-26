def HiRad(RxPower, StartupRange, InterRange, PowerRange):
    HiRad = False
    if (StartupRange == True):
        if (RxPower > 7.29e-03):
            HiRad = True
    if (InterRange == True):
        if (RxPower < 3.48e-03) or (RxPower > 12.6):
            HiRad = True
    if (PowerRange == True):
        if (RxPower < 0.0747):
            HiRad = True
    if ((StartupRange == False) and (InterRange == False) and (PowerRange == False)):
        HiRad = True

    return HiRad

def HiRadTrip(RxPower, StartupRange, InterRange, PowerRange):
    HiRadTrip = False
    if (StartupRange == True):
        if (RxPower > (7.29e-03 * 1.1)):
            HiRadTrip = True
    if (InterRange == True):
        if (RxPower < (3.48e-03 * 0.9)) or (RxPower > (12.6 * 1.1)):
            HiRadTrip = True
    if (PowerRange == True):
        if (RxPower < (0.0747 * 0.9)):
            HiRadTrip = True

    return HiRadTrip



    
