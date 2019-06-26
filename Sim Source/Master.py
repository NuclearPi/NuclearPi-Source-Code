from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
from ABE_ADCPi import ADCPi
import datetime
import time
from zellegraphics import *
from array import *
import Display_Data #display values on graphic
import random
import Radiation
import InitialConditions
import Halt



###########################################################################
# GLOBAL VARS
###########################################################################

global OffSitePower # offsite power status
global StartupTrans # startup transformer status
global AuxTrans # auxilliary transformer status
global Diesel # diesel status
global DieselBreaker # diesel breaker status
global switch_bus23 # bus for alarms
global AnnunFlash27 # flash 27annunciators
global AnnunFlash26 # flash 26 annunciators

###########################################################################
###########################################################################

###########################################################################
# Alarms Set and Reset
###########################################################################

def AS(): # set alarm
    switch_bus23.write_pin(15, 1) # set alarm pulse hi
    switch_bus23.write_pin(15, 0) # set alarm pulse lo    

def ARS(): # reset alarm
    switch_bus23.write_pin(16, 0) # set alarm pulse lo
    switch_bus23.write_pin(16, 1) # set alarm pulse hi        
 
###########################################################################
# Power Available
###########################################################################
def PA():
    if (OffSitePower == True) and (StartupTrans == True):
        return True
    else:
        if (OffSitePower == True) and (AuxTrans == True):
            return True
        else:
            if (Diesel == True) and (DieselBreaker == True):
                return True
            else:
                return False
            

###########################################################################
# INIT CARDS
###########################################################################
print ('\n' * 100) # clear screen - monitor screen
print ('init started')

i2c_helper = ABEHelpers()
i2c_bus = i2c_helper.get_smbus()


#rotary
print ('rotary started')
adc1 = ADCPi(i2c_bus, 0x68, 0x69, 12)
adc2 = ADCPi(i2c_bus, 0x6A, 0x6B, 12)
    
adc1.set_conversion_mode(1)
adc2.set_conversion_mode(1)

adc1.set_pga(1)
adc2.set_pga(1)
print ('rotary completed')

#status lights
print ('status lights started')
status_lights_bus24 = IoPi(i2c_bus, 0x24)
status_lights_bus25 = IoPi(i2c_bus, 0x25)
for i in range(1,17):
    status_lights_bus24.set_pin_direction(i, 0)  # set pin as an output
    status_lights_bus25.set_pin_direction(i, 0)  # set pin as an output
    status_lights_bus24.write_pin(i, 0) # default green
    status_lights_bus25.write_pin(i, 0) # default green
print ('status lights completed')

#annunciators
print ('annunciators started')
annun_bus26 = IoPi(i2c_bus, 0x26)
annun_bus27 = IoPi(i2c_bus, 0x27)
for i in range(1,17):
    annun_bus26.set_pin_direction(i, 0)  # set pin as an output
    annun_bus27.set_pin_direction(i, 0)  # set pin as an output
    annun_bus26.write_pin(i, 0) # default off
    annun_bus27.write_pin(i, 0) # default off
print ('annunciators completed')


#switches
print ('switches started')
switch_bus20 = IoPi(i2c_bus, 0x20)
switch_bus21 = IoPi(i2c_bus, 0x21)
switch_bus22 = IoPi(i2c_bus, 0x22)
switch_bus23 = IoPi(i2c_bus, 0x23)

for i in range(1,17):
    switch_bus20.set_pin_direction(i, 1)  # set card 1 bus 1 pin as input
    switch_bus20.set_pin_pullup(i, 1)
    switch_bus21.set_pin_direction(i, 1)  # set card 1 bus 2 pin as input
    switch_bus21.set_pin_pullup(i, 1)
    switch_bus22.set_pin_direction(i, 1)  # set card 2 bus 1 pin as input
    switch_bus22.set_pin_pullup(i, 1)

for i in range(1,15):
    switch_bus23.set_pin_direction(i, 1) # set card 2 bus 2 pins 1-14 as input
    switch_bus23.set_pin_pullup(i,1)
 
switch_bus23.set_pin_direction(15,0) # set card 2 bus 2 pin 15 as output (alarm)
switch_bus23.set_pin_direction(16,0) # set card 2 bus2 pin 16 as output (alarm clear)
switch_bus23.write_pin(15,0)
switch_bus23.write_pin(16,1)
print ('switches completed')

#graphics
print ('graphics started')
sim_win = GraphWin('Nuclear Pi',1500,900)
sim_win.setCoords(0, 0, 1500, 900)
zcolor = color_rgb(250, 1, 1)
sim_win.setBackground('white')

print ('graphics completed')

#########################################################################################
# check annunciators / status lights
#########################################################################################

print ('Annunciator / Status Lights Test')
print ('Hit q To Continue')
DispImage = Image(Point(750,450),'Annun_Check.gif')
DispImage.draw(sim_win)
for i in range(1,17):
    annun_bus26.write_pin(i, 1)
    annun_bus27.write_pin(i, 1)
z=0
while z==0:

    keyString = sim_win.checkKey()
    if keyString == "q": # exit
        print ('q for exit')
        z=1

    time.sleep(0.25)
    for i in range(1,17):
        status_lights_bus24.write_pin(i,1)
        status_lights_bus25.write_pin(i,1)
    time.sleep(0.25)
    for i in range(1,17):
        status_lights_bus24.write_pin(i,0)
        status_lights_bus25.write_pin(i,0)    
 
            
for i in range(1,17):
    annun_bus26.write_pin(i, 0) # 1
    annun_bus27.write_pin(i, 0) # 1   
    status_lights_bus24.write_pin(i,0)
    status_lights_bus25.write_pin(i,0)    
 
sim_win.close()
sim_win = GraphWin('Nuclear Pi',1500,900)
sim_win.setCoords(0, 0, 1500, 900)
zcolor = color_rgb(250, 1, 1)
sim_win.setBackground('white')

DispImage = Image(Point(750,450),'eventselection.gif')
DispImage.draw(sim_win)



Operation = 'x'
z=0

EventTimer = 0
EventRandomTimer = int(random.random()*600)
EventRandomPower = int(random.random()*100)
WhichPump = ''
WhichFeedValve = ''
RandomEvent = 'n/a'
RandomSelection = 0
while z==0:
    keyString = sim_win.checkKey()
    if (keyString == 'n'):
        z = 1
        Operation = 'Normal'
        print ('Normal Operations')
    if (keyString == '1'):
        z = 1
        Operation = 'LossPower'
        print ('Loss of Offsite Power Event')
    if (keyString == '2'):
        z = 1
        Operation = 'RcpTrip'
        print ('RCP Trip')
    if (keyString == '3'):
        z = 1
        Operation = 'MfpTrip'
        print ('MFP Trip')
    if (keyString == '4'):
        z = 1
        Operation = 'TurbineTrip'
        print ('Turbine Trip')
    if (keyString == '5'):
        z = 1
        Operation = 'CircWaterTrip'
        print ('Circ Water Trip')
    if (keyString == '6'):
        z = 1
        Operation = 'MFWV'
        print ('Main Feedwater Valve Fail')
        RandomSelection = int(random.random()*2) + 1
        if (RandomSelection == 1):
            WhichPump = 'Mfp1'
        else:
            WhichPump = 'Mfp2'
        RandomEvent = 'n/a'
        print ('Which Pump:', WhichPump)
    if (keyString == '7'):
        z = 1
        Operation = 'PriPorvOpen'
        print ('Primary PORV Open')
    if (keyString == '8'):
        z = 1
        Operation = 'SecPorvOpen'
        print ('Secondary PORV Open')
    if (keyString == '9'):
        z = 1
        Operation = 'Makeup/Letdown'
        print ('Makeup / Letdown Fail Selected')
        RandomSelection = int(random.random()*2) + 1
        if (RandomSelection == 1):
            WhichPump = 'LetDown'
        else:
            WhichPump = 'Charging'
        RandomEvent = 'n/a'
        print ('Which Pump:', WhichPump)
    if (keyString == '0'):
        z=1
        RandomEvent = int(random.random()*9) + 1
        if (RandomEvent == 1):
            Operation = 'LossPower'
            print ('Loss of Offsite Power Event (Random)')
        if (RandomEvent == 2):
            Operation = 'RcpTrip'
            print ('RCP Trip (Random)')
        if (RandomEvent == 3):
            Operation = 'MfpTrip'
            print ('MFP Trip (Random)')
        if (RandomEvent == 4):
            Operation = 'TurbineTrip'
            print ('Turbine Trip (Random)')
        if (RandomEvent == 5):
            Operation = 'CircWaterTrip'
            print ('Circ Water Trip (Random)')
        if (RandomEvent == 6):
            Operation = 'MFWV'
            print ('Main Feedwater Valve Fail (Random)')
            RandomSelection = int(random.random()*2) + 1
            if (RandomSelection == 1):
                WhichPump = 'Mfp1'
            else:
                WhichPump = 'Mfp2'
            RandomEvent = 'n/a'
        print ('Which Pump:', WhichPump)            
        if (RandomEvent == 7):
            Operation = 'PriPorvOpen'
            print ('Primary PORV Open (Random)')
        if (RandomEvent == 8):
            Operation = 'SecPorvOpen'
            print ('Secondary PORV Open (Random)')
        if (RandomEvent == 9):
            Operation = 'Makeup/Letdown'
            print ('Makeup / Letdown Fail Selected')
            RandomSelection = int(random.random()*2) + 1
            if (RandomSelection == 1):
                WhichPump = 'LetDown'
            else:
                WhichPump = 'Charging'
            RandomEvent = 'n/a'
            print ('Which Pump:', WhichPump) 





        
###########################################################################
# HARDWARE INITIAL CONDITIONS
###########################################################################
#InitialConditions.InitCond(sim_win, adc1, adc2, switch_bus21)



print ('hardware init completed')
###########################################################################
###########################################################################
DispImage = Image(Point(750,450),'nuke layout 1h.gif')
DispImage.draw(sim_win)

###########################################################################
# INITIAL CONDITIONS
###########################################################################

print ('initial conditions start')




#switch_bus23.write_pin(15, 1) # set alarm pulse hi
#switch_bus23.write_pin(15, 0) # set alarm pulse lo

print ('initial conditions completed')
###########################################################################
###########################################################################


ProcedureViolations = 0
OneTime_Transformer = True
OneTime_SgLevel = True
OneTime_FeedSource = True
OneTime_AccumulatorUnblock = True
OneTime_Permissive = True


OffSitePower = True
AuxTrans = False
StartupTrans = True
Diesel = False
DieselBreaker = False
CircWater = True
PrzrHeaters = False
PrzrSpray = False
PriPorv = False
SecPorv = False

# setup turbine startup status
ManTurbTrip = True
TurbineStatus = False
GenBreaker = False
GeneratorLoad = 0.0
MWH = 0.0

ManRxTrip = False

Rcp1 = False
Rcp1Thermal = 0.0
Rcp1_Demand = 0.0
xIncrement1 = 0.0

Rcp2 = False
Rcp2Thermal = 0.0
Rcp2_Demand = 0.0
xIncrement2 = 0.0

Mfp1 = False
Mfp2 = False
Afp1 = True
Afp2 = True
SdAfp = False
Sip = False
TurbTurnGear = True
TurbSpeed = 0
GenBreaker = False
GenSync = True

AnnunFlashToggle = True

PrzrLevel = 50

StartupRange = False
InterRange = True
PowerRange = False

RhrPump = False
SteamDump = False
Permissive = True
BlockValves = True
ControlRodsIn = False
ControlRodsOut = False
TurbineStatus = False
GeneratorSync = False
ReactorTrip = False
AccumulatorHasDischarged = False

Ann_CircWater = False
Ann_Diesel = False
Ann_OffSitePower = True
Ann_GenBreaker = False
Ann_GenOverPower = False
Ann_TurbOverUnderSpeed = True
Ann_TurbStatus = True
Ann_RxStatus = False
Ann_SteamDump = False
Ann_Permissive = False
Ann_SteamFeedMismatch = False
Ann_SgHiHiLoLo = False
Ann_SgHiLo = False
Ann_FeedwaterStatus = False
Ann_AuxFeedStatus = False
Ann_SecPorv = False
Ann_SecPressHiLo = False
Ann_Sip = False
Ann_HiRad = False
Ann_HiStartUpRate = False
Ann_RxOverPower = False
Ann_RxHiDeltaT = False
Ann_RxHiTemp = False
Ann_AccDischarge = False
Ann_PriPorv = False
Ann_PrimaryPressureHiLo = False
Ann_PrimaryPressureHiHiLoLo = False
Ann_PrzrLevelHiLo = False
Ann_PrzrLevelHiHiLoLo = False
Ann_RcsLoFlow = False
Ann_RcpTrip = False
Ann_ManRxTrip = False
Ann_RxTrip = False
Ann_HiRad = False
Ann_HiRadTrip = False

SdAfp_Flow=0
Mfp1_Flow=0
Mfp2_Flow=0
Afp1_Flow=0
Afp2_Flow=0
Loop1_Flow=0
Loop2_Flow=0
PriPorv_Display='Close'
SecPorv_Display='Close'
Rhr_Flow=0
Si_Flow=0
Charging_Flow=0
LetDown_Flow=0
Boron_Flow=0
Steam_Dump_Flow=0
Circ_Flow=0
Block_Valves_Display='Close'
TurbineSpeed_Display = 0
GeneratorVoltage = 0.0


HeaterSpray = 0

RxPowerPlusDelay = 0.0
RxPowerTotal = 0.0
PrimaryTemperature = 0.0
TotalFlow = 0.0
SecondaryTemperature = 0.0
PrimaryThermal = 0.0
EnergyPrimary = 0.0
EnergySecondary = 0.0
PrzrLevel = 50.0

# change back to 10 for startup
SgLevel = 10.0
SgLevel1 = 10.0
SgLevel2 = 10.0

SteamFeedMismatch = 0.0
Thot = 0.0
Tcold = 0.0
DeltaT = 0.0
TotalFeedWater = 0.0
RCSVolume = 134.0
PrimaryMass = 100.0
FlowStartUp = 0.0
xIncrement = 0.0
xIncrement1 = 0.0
xIncrement2 = 0.0
LetDownCharging = 0.0
FlowStartUpCounter = 0
FwFlow = 0.0
MWH = 0.0
SecondaryPressure = 0.0
PrimaryPressure = 0.0


#########################################################################################
# flow control variables
#########################################################################################
PriPorv_Demand = 0
PriPorv_Temp = 0

Rcp1_Demand = 0
Rcp1_Temp = 0

Rcp2_Demand = 0
Rcp2_Temp = 0

Charging_Demand = 0
Charging_Temp = 0
LetDown_Demand = 0
LetDown_Temp = 0
CircWater_Demand = 100
CircWater_Temp = 0
Boron_Demand = 0
Boron_Temp = 0
TurbineSpeed_Demand = 0
TurbineSpeed_Temp = 0
SteamDump_Demand = 0
SteamDump_Temp = 0
Mfp1_Demand = 0
Mfp1_Temp = 0
Mfp2_Demand = 0
Mfp2_Temp = 0
Afp1_Demand = 0
Afp1_Temp = 0
Afp2_Demand = 0
Afp2_Temp = 0
SdAfp_Demand = 0
SdAfp_Temp = 0
Rhr_Demand = 0
Rhr_Temp = 0
Si_Demand = 0
Si_Temp = 0

GeneratorLoad = 0.0
GeneratorLoad_Demand = 0.0


RxPower=0
global xTrans
xTrans=1

print ("int triggered")
endtime=datetime.datetime.now()

print ("Initial second: %d" % endtime.second)

#init screen
Display_Data.DisplayData('I',sim_win,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

# delay power init
DelayPower = array('d',[0])

for i in range(1,601):
    DelayPower.append(0)

# current annunciator arrays
Annun26 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Annun27 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
AnnunFlash26 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
AnnunFlash27 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
AnnunCounter=0     

print ("DelayPower array init completed")


# used to control main loop
z=0
    
start_time = time.time()

skipper=1 # init screen display control var
ControlRodSkip = 1 # timer to read control rods in/out

print ('Init Completed')
print ('q to exit simulation')
    

#BankA=0
#BankB=0
#BankC=0
#BankD=0

LastRxPower=0
RxPowerDelayPower=0

GeneratorSyncRandom = int(random.random()*100)
    
AdjVol=4.9



BankA = 228
BankB = 228
BankC = 120
BankD = 0

######################################################################################################################
######################################################################################################################
# MASTER LOOP
######################################################################################################################
######################################################################################################################

z=0
while z==0:
    keyString = sim_win.checkKey()

    if (keyString == 'h'): # help
        print ('-----------------------------')
        print ('q - Quit Simulation')
        print ('p - Pause Simulation')
        print ('a - Annunciator Light Check')
        print ('h - Help (This Menu)')
        print ('d - Data Dump')
        print ('e - Event')
        print ('-----------------------------')
        
    if (keyString == 'e'): # event
        print ('-----------------------------')
        print ('Event:',Operation)
        print ('Random Event Number:',RandomEvent)
        print ('Event Power Level %:', EventRandomPower)
        print ('Event Timer (sec) After Power Level:', EventRandomTimer)
        print ('-----------------------------')
        
    if (keyString == 'd'): # data dump
        print ('-----------------------------')
        print ('FlowStartUp', FlowStartUp)
        print ('TotalFlow', TotalFlow)
        print ('RxPower', RxPowerTotal)
        print ('EP',EnergyPrimary)
        print ('ES', EnergySecondary)
        print ('Mass', PrimaryMass)
        print ('LetdownCharging', LetDownCharging)
        print ('V2', V2)
        print ('Przr Level', PrzrLevel)
        print ('Generator Load', GeneratorLoad)
        print ('Steam Dump', SteamDump_Temp)
        print ('Circ water', Circ_Flow)
        print ('Total FW Flow', FwFlow)
        print ('Turbine Display Speed', TurbineSpeed_Display * 20)
        print ('FwFlow * 100', FwFlow * 100)
        print ('Random Timer', EventRandomTimer)
        print ('Random Power', EventRandomPower)
    
        print ('-----------------------------')

    if (keyString == 'p'): # pause
        pp = 0
        print ('Pausing Simulation')
        print ('Hit x to Continue')
        
        while pp == 0:
            keyString = sim_win.checkKey()
            if (keyString == 'x'):
                pp = 1
        print ('Resuming Simulation')        


    if (keyString == 'a'): # annun check
        print ('Annunciator Check')
        print ('Hit x to Exit')
        pp = 0
        for i in range(1,17):
            Annun26[i-1] = annun_bus26.read_pin(i)
            Annun27[i-1] = annun_bus27.read_pin(i)
            
        for i in range(1,17):
            annun_bus26.write_pin(i, 1)
            annun_bus27.write_pin(i, 1)
            
        while pp == 0:
            keyString = sim_win.checkKey()
            if (keyString == 'x'):
                pp = 1

        for i in range(1,17):
            annun_bus26.write_pin(i,Annun26[i-1])
            annun_bus27.write_pin(i,Annun27[i-1])
        print ('Annunciator Check Completed')
        
        
    if keyString == "q": # exit main sim loop
        print ('q for exit')
        z=1


###########################################################################
# TO DO
###########################################################################
# power off


###########################################################################
# Rotary - not Switch Triggered
###########################################################################

    if (PA()): # boron
        Boron_Demand=int(adc2.read_voltage(6)/AdjVol*100)
    else:
        Boron_Demand=0
    Boron_Temp = float(Boron_Temp) + float((Boron_Demand - Boron_Temp)/100)
    Boron_Flow = int(round(Boron_Temp))
    Power_Boron = (Boron_Flow*0.05/100)
    

    if (PA()): # charging
        Charging_Demand=int(adc1.read_voltage(5)/AdjVol*100)    
    else:
        Charging_Demand = 0
    Charging_Temp = float(Charging_Temp) + float((Charging_Demand-Charging_Temp)/20)
    Charging_Flow = int(round(Charging_Temp))

    if ((Operation == 'Makeup/Letdown') and (WhichPump == 'Charging') and (RxPowerTotal >= EventRandomPower)):
        EventTimer = EventTimer + 1
        if (EventTimer > EventRandomTimer):
            Charging_Flow = 50
            

    if (PA()): # letdown
        LetDown_Demand=int(adc1.read_voltage(2)/AdjVol*100)
    else:
        LetDown_Demand=0
    LetDown_Temp = float(LetDown_Temp) + float((LetDown_Demand-LetDown_Temp)/20)
    LetDown_Flow=int(round(LetDown_Temp))

    if ((Operation == 'Makeup/Letdown') and (WhichPump == 'LetDown') and (RxPowerTotal >= EventRandomPower)):
        EventTimer = EventTimer + 1
        if (EventTimer > EventRandomTimer):
            LetDown_Flow = 88


    LetDownCharging = (Charging_Flow - LetDown_Flow) / 100000

    

    if (PA() and Mfp1 == True): # mfp1
        Mfp1_Demand=int(adc1.read_voltage(4)/AdjVol*100)
    else:
        Mfp1_Demand=0
    Mfp1_Temp = float(Mfp1_Temp) + float((Mfp1_Demand - Mfp1_Temp)/75)
    Mfp1_Flow = int(round(Mfp1_Temp))
    if ((Operation == 'MFWV') and (WhichPump == 'Mfp1') and (RxPowerTotal >= EventRandomPower)):
        EventTimer = EventTimer + 1
        if (EventTimer > EventRandomTimer):
            Mfp1_Flow = 0        

    if (PA() and Mfp2 == True): # mfp2
        Mfp2_Demand=int(adc1.read_voltage(1)/AdjVol*100)
    else:
        Mfp2_Demand=0
    Mfp2_Temp = float(Mfp2_Temp) + float((Mfp2_Demand - Mfp2_Temp)/75)
    Mfp2_Flow = int(round(Mfp2_Temp))
    if ((Operation == 'MFWV') and (WhichPump == 'Mfp2') and (RxPowerTotal >= EventRandomPower)):
        EventTimer = EventTimer + 1
        if (EventTimer > EventRandomTimer):
            Mfp2_Flow = 100                



    if (PA() and Afp1 == True): # afp1
        Afp1_Demand=int(adc1.read_voltage(8)/AdjVol*100)
    else:
        Afp1_Demand=0
    Afp1_Temp = float(Afp1_Temp) + float((Afp1_Demand - Afp1_Temp)/50)
    Afp1_Flow = int(round(Afp1_Temp))

    if (PA() and Afp2 == True): # afp2
        Afp2_Demand=int(adc1.read_voltage(3)/AdjVol*100)
    else:
        Afp2_Demand=0
    Afp2_Temp = float(Afp2_Temp) + float((Afp2_Demand - Afp2_Temp)/50)
    Afp2_Flow = int(round(Afp2_Temp))

    if (PA() and SdAfp == True): # adafp      
        SdAfp_Demand=int(adc1.read_voltage(7)/AdjVol*100)
    else:
        SdAfp_Demand=0
    SdAfp_Temp = float(SdAfp_Temp) + float((SdAfp_Demand - SdAfp_Temp)/50)
    SdAfp_Flow = int(round(SdAfp_Temp))

    if (PA() and Sip == True): # si
        Si_Demand=int(adc2.read_voltage(3)/AdjVol*100)        
    else:
        Si_Demand=0
    Si_Temp = float(Si_Temp) + float((Si_Demand - Si_Temp)/50)
    Si_Flow = int(round(Si_Temp))
        
    if (PA() and RhrPump == True): # rhr
        Rhr_Demand=int(adc2.read_voltage(2)/AdjVol*100)
    else:
        Rhr_Demand=0
    Rhr_Temp = float(Rhr_Temp) + float((Rhr_Demand - Rhr_Temp)/100)
    Rhr_Flow = int(round(Rhr_Temp))

    if (PA() and SteamDump == True): # steam dump
        SteamDump_Demand=int(adc1.read_voltage(6)/AdjVol*100)
    else:
        SteamDump_Demand=0
    SteamDump_Temp = float(SteamDump_Temp) + float((SteamDump_Demand - SteamDump_Temp)/100)
    Steam_Dump_Flow = int(round(SteamDump_Temp))    
    Steam_Dump_Flow = Steam_Dump_Flow * Circ_Flow / 100
    
    if (PA() and TurbineStatus == True and ManTurbTrip != True): # turbine speed
        TurbineSpeed_Demand=int(adc2.read_voltage(1)/AdjVol*100)
    else:
        TurbineSpeed_Demand=0
    TurbineSpeed_Temp = float(TurbineSpeed_Temp) + float((TurbineSpeed_Demand - TurbineSpeed_Temp)/75)

    if (TurbTurnGear == True):
        TurbineSpeed_Display = 0.25
    else:
        TurbineSpeed_Display = int(round(TurbineSpeed_Temp))

        
    if (PA() and TurbineStatus == True and int(TurbineSpeed_Display*20) == 1800): # sync turbine speed
        TurbineFine=int(adc2.read_voltage(5)/AdjVol*100)
        if (TurbineFine == GeneratorSyncRandom):
            status_lights_bus25.write_pin(15, 1)
        else:
            if (GenBreaker == True):
                status_lights_bus25.write_pin(15, 1)
            else:
                status_lights_bus25.write_pin(15, 0)
            
    if (PA() and TurbineStatus == True and int(TurbineSpeed_Display*20) == 1800): # gen voltage when turbine = 1800
        GeneratorVoltage=(int(adc2.read_voltage(4)/AdjVol*100)*40)+22000
        if (GeneratorVoltage == 24000):
            status_lights_bus25.write_pin(14, 1)
        else:
            status_lights_bus25.write_pin(14, 0)

    if (PA() and TurbineStatus == True and GenBreaker == True): # gen load
        GeneratorLoad_Demand=(int(adc2.read_voltage(7)/AdjVol*100))
    else:
        GeneratorLoad_Demand = 0

    GeneratorLoad = float(GeneratorLoad) + float((GeneratorLoad_Demand - GeneratorLoad)/100) 
    GeneratorLoad = GeneratorLoad * Circ_Flow / 100
    if (GenBreaker == False):
        GeneratorLoad = 0.0
    



        
###########################################################################
# SWITCHES
###########################################################################
    if (switch_bus21.read_pin(10) == 0): # aux trans closed
        AuxTrans = True
    if (switch_bus20.read_pin(5) == 0): # aux trans open
        AuxTrans = False

    if (switch_bus20.read_pin(3) == 0): # startup trans closed
        StartupTrans = True
    if (switch_bus20.read_pin(6) == 0): # startup trans open
        StartupTrans = False


# should reserve var OffSitePower for events - default is True: OffSitePower is available

#    if ((AuxTrans == False) and (StartupTrans == False)):
#        OffSitePower = False
#    else:
#        OffSitePower = True
        

    if (switch_bus20.read_pin(1) == 0): # diesel start
        Diesel = True
    if (switch_bus20.read_pin(4) == 0): # diesel stop
        Diesel = False
        DieselBreaker = False

    if (switch_bus20.read_pin(8) == 0) and (Diesel == True): # diesel breaker close
        DieselBreaker = True
    if (switch_bus20.read_pin(2) == 0): # diesel breaker open
        DieselBreaker = False
                    
    if (switch_bus22.read_pin(15) == 0) and PA(): # circ water pump
        CircWater = True
        CircWater_Demand = 100
    if (switch_bus23.read_pin(7) == 0):
        CircWater = False
        CircWater_Demand = 0
    CircWater_Temp = float(CircWater_Temp) + float((CircWater_Demand - CircWater_Temp)/75)
    Circ_Flow = int(round(CircWater_Temp))

    if (switch_bus21.read_pin(7) == 0) and PA(): # przr heaters
        PrzrHeaters = True
    if (switch_bus21.read_pin(11) == 0):
        PrzrHeaters = False

    if (switch_bus21.read_pin(13) == 0) and PA(): # pzrz spray
        PrzrSpray = True
    if (switch_bus21.read_pin(9) == 0):
        PrzrSpray = False

    if (switch_bus21.read_pin(15) == 0) and PA(): # pri porv
        PriPorv = True
        PriPorv_Demand = 100.0
        PriPorv_Display='Open'
    if (switch_bus21.read_pin(5) == 0):
        PriPorv = False
        PriPorv_Demand = 0.0
        PriPorv_Display='Close'
    PriPorv_Temp = float(PriPorv_Temp) + float((PriPorv_Demand - PriPorv_Temp)/100)
    
    if (switch_bus23.read_pin(1) == 0) and PA(): # sec porv
        SecPorv = True
        SecPorv_Display='Open'
    if (switch_bus22.read_pin(11) == 0):
        SecPorv = False
        SecPorv_Display='Close'

    if (switch_bus20.read_pin(9) == 0) and PA(): # man turb trip
        ManTurbTrip = True
        TurbineStatus = False
        GenBreaker = False
        GeneratorLoad = 0.0
        MWH = 0.0
    if (switch_bus21.read_pin(16) == 0):
        ManTurbTrip = False
        TurbineStatus = True

    if (switch_bus22.read_pin(14) == 0) and PA(): # man rx trip
        ReactorTrip = True
        print ('Manual Rx Trip')
        ManRxTrip = True
        BankA = 0
        BankB = 0
        BankC = 0
        BankD = 0
        
    if (switch_bus20.read_pin(16) == 0):
        ManRxTrip = False
        ReactorTrip = False

    if (switch_bus22.read_pin(4) == 0) and PA(): # rcp 1
        Rcp1 = True
        Rcp1Thermal = 2.5
        Rcp1_Demand = 100.0
        xIncrement1 = 0.5
        
    if (switch_bus22.read_pin(6) == 0):
        Rcp1 = False
        Rcp1Thermal = 0.0        
        Rcp1_Demand = 0.0

        
    Rcp1_Temp = float(Rcp1_Temp) + float((Rcp1_Demand - Rcp1_Temp)/75)
    Loop1_Flow=int(round(Rcp1_Temp))
    
    if (switch_bus22.read_pin(12) == 0) and PA(): # rcp 2
        Rcp2 = True
        Rcp2Thermal = 2.5        
        Rcp2_Demand = 100.0
        xIncrement2 = 0.5
    if (switch_bus22.read_pin(10) == 0):
        Rcp2 = False
        Rcp2Thermal = 0.0        
        Rcp2_Demand = 0.0

        
    Rcp2_Temp = float(Rcp2_Temp) + float((Rcp2_Demand - Rcp2_Temp)/75)
    Loop2_Flow=int(round(Rcp2_Temp))
        

    if (switch_bus22.read_pin(7) == 0) and PA(): # mfp 1
        Mfp1 = True
    if (switch_bus23.read_pin(2) == 0): # mfp 1
        Mfp1 = False

    if (switch_bus23.read_pin(3) == 0) and PA(): # mfp 2
        Mfp2 = True      
    if (switch_bus23.read_pin(6) == 0): # mfp 2
        Mfp2 = False
              
    if (switch_bus22.read_pin(9) == 0) and PA(): # afp 1
        Afp1 = True
    if (switch_bus23.read_pin(10) == 0):
        Afp1 = False
        
    if (switch_bus22.read_pin(13) == 0) and PA(): # afp 2
        Afp2 = True
    if (switch_bus23.read_pin(8) == 0):
        Afp2 = False

    if (switch_bus23.read_pin(4) == 0) and PA(): # sdafp
        SdAfp = True
    if (switch_bus23.read_pin(5) == 0):
        SdAfp = False

    if (switch_bus21.read_pin(6) == 0) and PA(): # sip
        Sip = True
        Afp1 = True
        Afp2 = True
    if (switch_bus21.read_pin(1) == 0):
        Sip = False

    if (switch_bus20.read_pin(11) == 0) and PA() and (ManTurbTrip) and (TurbSpeed == 0): # turb turn gear
        TurbTurnGear = True
    if (switch_bus20.read_pin(15) == 0):
        TurbTurnGear = False


    if (switch_bus20.read_pin(13) == 0) and PA() and GenSync: # generator breaker
        GenBreaker = True
    if (switch_bus20.read_pin(7) == 0):
        GenBreaker = False
        GeneratorLoad = 0.0
        MWH = 0.0

# moved this to rotary controls section
#    if (GenBreaker == True): # this locks in sync light when gen breaker is closed
#        status_lights_bus25.write_pin(15, 1)
    

    if (switch_bus20.read_pin(14) == 0) and PA(): # startup range detector
        StartupRange = True
    if (switch_bus22.read_pin(16) == 0):
        StartupRange = False

    if (switch_bus22.read_pin(3) == 0) and PA(): # inter range detector
        InterRange = True
    if (switch_bus22.read_pin(2) == 0):
        InterRange = False

    if (switch_bus22.read_pin(8) == 0) and PA(): # power range detector
        PowerRange = True
    if (switch_bus20.read_pin(10) == 0):
        PowerRange = False

    if (switch_bus21.read_pin(4) == 0) and PA(): # rhr pump
        RhrPump = True
    if (switch_bus21.read_pin(2) == 0):
        RhrPump = False

    if (switch_bus23.read_pin(9) == 0) and PA(): # steam dump
        SteamDump = True
    if (switch_bus22.read_pin(5) == 0):
        SteamDump = False

    if (switch_bus21.read_pin(3) == 0) and PA(): # block valves
        BlockValves = True
        Block_Valves_Display = 'Close'
    if (switch_bus21.read_pin(8) == 0):
        BlockValves = False
        Block_Valves_Display = 'Open'
        
    if (switch_bus20.read_pin(12) == 0) and PA(): # permissive
        Permissive = True
    if (switch_bus22.read_pin(1) == 0):
        Permissive = False
        if (PrimaryPressure < 2000):
            ReactorTrip = True
            print ('Rx Trip - Primary Pressure Lo Lo')
        if (SgLevel < 10):
            ReactorTrip = True
            print ('Rx Trip - SG Level Lo Lo')
        if (PrzrLevel < 20):
            ReactorTrip = True
            print ('Rx Trip - Pressurizer Level Lo Lo')
            

        

###########################################################################
# STATUS LIGHTS
###########################################################################

    if (AuxTrans == True): # aux trans
        status_lights_bus25.write_pin(10, 1) 
    else:
        status_lights_bus25.write_pin(10, 0)

    if (StartupTrans == True): # startup trans
        status_lights_bus25.write_pin(9, 1)
    else:
        status_lights_bus25.write_pin(9, 0)
        
    if (Diesel == True): #diesel
        status_lights_bus25.write_pin(7, 1) # diesel
    else:
        status_lights_bus25.write_pin(7, 0)

    if (DieselBreaker == True): # diesel breaker
        status_lights_bus25.write_pin(8, 1)
    else:
        status_lights_bus25.write_pin(8, 0)

    if (CircWater == True): # circ water
        status_lights_bus25.write_pin(13, 1) 
    else:
        status_lights_bus25.write_pin(13, 0)

    if (PrzrHeaters == True): # przr heaters
        status_lights_bus25.write_pin(1, 1) 
    else:
        status_lights_bus25.write_pin(1, 0)

    if (PrzrSpray == True): # przr spray
        status_lights_bus25.write_pin(2, 1)
    else:
        status_lights_bus25.write_pin(2, 0)
        
    if (PriPorv == True): # pri porv
        status_lights_bus24.write_pin(4, 1) 
    else:
        status_lights_bus24.write_pin(4, 0)
        
    if (SecPorv == True): # sec porv
        status_lights_bus24.write_pin(14, 1)
    else:
        status_lights_bus24.write_pin(14, 0)
        
    if (ManTurbTrip == True): # man turb trip
        status_lights_bus25.write_pin(5, 1)
    else:
        status_lights_bus25.write_pin(5, 0)

    if (ManRxTrip == True): # man rx trip
        status_lights_bus24.write_pin(1, 1)
    else:
        status_lights_bus24.write_pin(1, 0)

    if (Rcp1 == True): # rcp 1
        status_lights_bus24.write_pin(2, 1)
    else:
        status_lights_bus24.write_pin(2, 0)

    if (Rcp2 == True): # rcp 2
        status_lights_bus24.write_pin(3, 1)
    else:
        status_lights_bus24.write_pin(3, 0)
        
    if (Mfp1 == True): # mfp 1
        status_lights_bus24.write_pin(5, 1)
    else:
        status_lights_bus24.write_pin(5, 0)
        
    if (Mfp2 == True): # mfp 2
        status_lights_bus24.write_pin(6, 1)
    else:
        status_lights_bus24.write_pin(6, 0)

    if (Afp1 == True): # afp 1
        status_lights_bus24.write_pin(7, 1)
    else:
        status_lights_bus24.write_pin(7, 0)
        
    if (Afp2 == True): # afp 2
        status_lights_bus24.write_pin(8, 1)
    else:
        status_lights_bus24.write_pin(8, 0)

    if (SdAfp == True): # sdafp
        status_lights_bus24.write_pin(16, 1)
    else:
        status_lights_bus24.write_pin(16, 0)

    if (Sip == True): # sip
        status_lights_bus24.write_pin(9, 1)
    else:
        status_lights_bus24.write_pin(9, 0)

    if (TurbTurnGear == True): # turb turn gear
        status_lights_bus25.write_pin(6, 1)
    else:
        status_lights_bus25.write_pin(6, 0)
        
    if (GenBreaker == True): # generator breaker
        status_lights_bus25.write_pin(16, 1)
    else:
        status_lights_bus25.write_pin(16, 0)

    if (StartupRange == True): # startup range detector
        status_lights_bus24.write_pin(10, 1)
    else:
        status_lights_bus24.write_pin(10, 0)

    if (InterRange == True): # inter range detector
        status_lights_bus24.write_pin(11, 1)
    else:
        status_lights_bus24.write_pin(11, 0)

    if (PowerRange == True): # startup range detector
        status_lights_bus24.write_pin(12, 1)
    else:
        status_lights_bus24.write_pin(12, 0)

    if (RhrPump == True): # rhr pump
        status_lights_bus24.write_pin(13, 1)
    else:
        status_lights_bus24.write_pin(13, 0)

    if (SteamDump == True): # steam dump
        status_lights_bus24.write_pin(15, 1)
    else:
        status_lights_bus24.write_pin(15, 0)

    if (BlockValves == True): # block valves
        status_lights_bus25.write_pin(4, 1)
    else:
        status_lights_bus25.write_pin(4, 0)

    if (Permissive == True): # permissive
        status_lights_bus25.write_pin(3, 1)
    else:
        status_lights_bus25.write_pin(3, 0)

    if (TurbineStatus == True): # turbine status (manual trip / other trips / power avail)
        status_lights_bus25.write_pin(12, 1)
    else:
        status_lights_bus25.write_pin(12, 0)


###########################################################################
# ANNUNCIATORS
###########################################################################

# circ water
    if (CircWater == False): 
        if (Ann_CircWater == False):
            AS()
            Ann_CircWater = True
        annun_bus27.write_pin(10, 1)
    else:
        if (Ann_CircWater == True):
            ARS()
            Ann_CircWater = False
        annun_bus27.write_pin(10, 0)
        
 # diesel
    if (Diesel == True):
        if (Ann_Diesel == False):
            AS()
            Ann_Diesel = True
        annun_bus27.write_pin(12, 1)                
    else:
        if (Ann_Diesel == True):
            ARS()
            Ann_Diesel = False
        annun_bus27.write_pin(12, 0)        

# off site power
    if (OffSitePower == False): 
        if (Ann_OffSitePower == False):
            AS()
            Ann_OffSitePower = True
        annun_bus27.write_pin(13, 1)                
    else:
        if (Ann_OffSitePower == True):
            ARS()
            Ann_OffSitePower = False
        annun_bus27.write_pin(13, 0)

# gen breaker open
    if (GenBreaker == False): 
        if (Ann_GenBreaker == False):
            AS()
            Ann_GenBreaker = True
        annun_bus27.write_pin(16, 1)                
    else:
        if (Ann_GenBreaker == True):
            ARS()
            Ann_GenBreaker = False
        annun_bus27.write_pin(16, 0)

# gen over power
    if (GeneratorLoad > 100): 
        if (Ann_GenOverPower == False):
            AS()
            Ann_GenOverPower = True
        annun_bus27.write_pin(8, 1)
    else:
        if (Ann_GenOverPower == True):
            ARS()
            Ann_GenOverPower = False
        annun_bus27.write_pin(8,0)
     
# turbine over/underspeed
    if ((20 * TurbineSpeed_Display < 1800) or (20 * TurbineSpeed_Display >1800)): 
# need rx trip if no permissive
        if (Ann_TurbOverUnderSpeed == False):
            AS()
            Ann_TurbOverUnderSpeed = True
        annun_bus27.write_pin(2, 1)
    else:
        if (Ann_TurbOverUnderSpeed == True):
            ARS()
            Ann_TurbOverUnderSpeed = False
        annun_bus27.write_pin(2, 0)                    
        
# turbine status 
    if (TurbineStatus == False):
        if (Ann_TurbStatus == False):
            AS()
            Ann_TurbStatus = True
        annun_bus27.write_pin(4, 1)
    else:
        if (Ann_TurbStatus == True):
            ARS()
            Ann_TurbStatus = False
        annun_bus27.write_pin(4, 0)

# steam dump
    if (SteamDump == True): 
        if (Ann_SteamDump == False):
            AS()
            Ann_SteamDump = True
        annun_bus27.write_pin(6, 1)                
    else:
        if (Ann_SteamDump == True):
            ARS()
            Ann_SteamDump = False
        annun_bus27.write_pin(6, 0)        


# sec pressure hi hi / lo lo
    if (SecondaryPressure > 1300): 
        if (Ann_SecPressHiLo == False):
            AS()
            Ann_SecPressHiLo = True
        annun_bus27.write_pin(15, 1)                
    else:
        if (Ann_SecPressHiLo == True):
            ARS()
            Ann_SecPressHiLo = False
        annun_bus27.write_pin(15, 0)        


# sec porv
    if (SecPorv == True): 
        if (Ann_SecPorv == False):
            AS()
            Ann_SecPorv = True
        annun_bus27.write_pin(14, 1)                
    else:
        if (Ann_SecPorv == True):
            ARS()
            Ann_SecPorv = False
        annun_bus27.write_pin(14, 0)        


# aux feed status
    if (Afp1 == True) or (Afp2 == True) or (SdAfp == True): 
        if (Ann_AuxFeedStatus == False):
            AS()
            Ann_AuxFeedStatus = True
        annun_bus27.write_pin(11, 1)                
    if (Afp1 == False) and (Afp2 == False) and (SdAfp == False):
        if (Ann_AuxFeedStatus == True):
            ARS()
            Ann_AuxFeedStatus = False
        annun_bus27.write_pin(11, 0)        


# main feed status
    if (Mfp1 == False) or (Mfp2 == False): 
        if (Ann_FeedwaterStatus == False):
            AS()
            Ann_FeedwaterStatus = True
        annun_bus27.write_pin(9, 1)                
    if (Mfp1 == True) and (Mfp2 == True):
        if (Ann_FeedwaterStatus == True):
            ARS()
            Ann_FeedwaterStatus = False
        annun_bus27.write_pin(9, 0)        

#  s/g  hi lo
    if (SgLevel < 30 or SgLevel > 80): 
        if (Ann_SgHiLo == False):
            AS()
            Ann_SgHiLo = True
        annun_bus27.write_pin(3, 1)                
    else:
        if (Ann_SgHiLo == True):
            ARS()
            Ann_SgHiLo  = False
        annun_bus27.write_pin(3, 0)        

# s/g  hi hi lo lo
    if (SgLevel < 20 or SgLevel > 90): 
        if (SgLevel > 90):
            TurbineStatus = False
        if (Permissive == False):
            ReactorTrip = True
            if (SgLevel < 20):
                print ('Rx Trip - Steam Generator Level Lo Lo')
            if (SgLevel > 90):
                print ('Rx Trip - Steam Generator Level Hi Hi')
        if (Ann_SgHiHiLoLo == False):
            AS()
            Ann_SgHiHiLoLo = True
        annun_bus27.write_pin(7, 1)                
    else:
        if (Ann_SgHiHiLoLo == True):
            ARS()
            Ann_SgHiHiLoLo  = False
        annun_bus27.write_pin(7, 0)

        
# steam/feed  mismatch
    if (((FwFlow * 100) < 0.5 * EnergySecondary) or ((FwFlow * 100) > 1.5 * EnergySecondary) or
    (EnergySecondary < (0.5 * FwFlow * 100)) or (EnergySecondary > (1.5 * FwFlow * 100))):
        if (Ann_SteamFeedMismatch == False):
            AS()
            Ann_SteamFeedMismatch = True
        annun_bus27.write_pin(1, 1)
    else:
        if (Ann_SteamFeedMismatch == True):
            ARS()
            Ann_SteamFeedMismatch = False
        annun_bus27.write_pin(1, 0)

# permissive
    if (Permissive == True): 
        if (Ann_Permissive == False):
            AS()
            Ann_Permissive = True
        annun_bus27.write_pin(5, 1)                
    else:
        if (Ann_Permissive == True):
            ARS()
            Ann_Permissive = False
        annun_bus27.write_pin(5, 0)        

# primary porv
    if (PriPorv == True): 
        if (Ann_PriPorv == False):
            AS()
            Ann_PriPorv = True
        annun_bus26.write_pin(11, 1)                
    else:
        if (Ann_PriPorv == True):
            ARS()
            Ann_PriPorv = False
        annun_bus26.write_pin(11, 0)        


# accumulator discharge
    if ((PrimaryPressure < 1900) and (BlockValves == False)):
        AccumulatorHasDischarged = True
        ReactorTrip = True
        print ('Rx Trip - Accumulator Discharge')
        if (Ann_AccDischarge == False):
            AS()
            Ann_AccDischarge = True
        annun_bus26.write_pin(13,1)
    else:
        if (Ann_AccDischarge == True):
            ARS()
            Ann_AccDischarge = False
        annun_bus26.write_pin(13,0)
        

# rx high temp
    if (PrimaryTemperature > 575):
        if (Ann_RxHiTemp == False):
            AS()
            Ann_RxHiTemp = True
        annun_bus26.write_pin(15,1)
    else:
        if (Ann_RxHiTemp == True):
            ARS()
            Ann_RxHiTemp = False
        annun_bus26.write_pin(15,0)

    if (PrimaryTemperature > 600):
        print ('Rx Trip - Primary Temperature Hi Hi')
        ReactorTrip = True


            
# rx high deltaT
    if (DeltaT > 63):
        if (Ann_RxHiDeltaT == False):
            AS()
            Ann_RxHiDeltaT = True
        annun_bus26.write_pin(9,1)
    else:
        if (Ann_RxHiDeltaT == True):
            ARS()
            Ann_RxHiDeltaT = False
        annun_bus26.write_pin(9,0)

# rx overpower
    if (RxPowerPlusDelay > 105): 
        if (Ann_RxOverPower == False):
            AS()
            Ann_RxOverPower = True
        annun_bus26.write_pin(7, 1)                
    else:
        if (Ann_RxOverPower == True):
            ARS()
            Ann_RxOverPower = False
        annun_bus26.write_pin(7, 0)
        
# high startup rate


# cont high radiation - this is handled in switch section


# safety injection
    if (Sip == True): 
        if (Ann_Sip == False):
            AS()
            Ann_Sip = True
        annun_bus26.write_pin(1, 1)                
    else:
        if (Ann_Sip == True):
            ARS()
            Ann_Sip = False
        annun_bus26.write_pin(1, 0)        


# rx pressure hi lo
    if ((PrimaryPressure > 2400) or (PrimaryPressure < 2000)):
        if (Ann_PrimaryPressureHiLo == False):
            AS()
            Ann_PrimaryPressureHiLo = True
        annun_bus26.write_pin(3,1)
    else:
        if (Ann_PrimaryPressureHiLo == True):
            ARS()
            Ann_PrimaryPressureHiLo = False
        annun_bus26.write_pin(3,0)
        

        
# rx pressure hihi lolo
    if ((PrimaryPressure > 2500) or (PrimaryPressure < 1900)):
        if (Ann_PrimaryPressureHiHiLoLo == False):
            AS()
            Ann_PrimaryPressureHiHiLoLo = True
            if (Permissive == False):
                ReactorTrip = True
                if (PrimaryPressure > 2500):
                    print ('Rx Trip - Primary Pressure Hi Hi')
                if (PrimaryPressure < 1900):
                    print ('Rx Trip - Primary Pressure Lo Lo')
                    
        annun_bus26.write_pin(6,1)
    else:
        if (Ann_PrimaryPressureHiHiLoLo == True):
            ARS()
            Ann_PrimaryPressureHiHiLoLo = False
        annun_bus26.write_pin(6,0)

        
# przr level hi lo
    if ((PrzrLevel < 30) or (PrzrLevel > 80 )):
        if (Ann_PrzrLevelHiLo == False):
            AS()
            Ann_PrzrLevelHiLo = True
        annun_bus26.write_pin(10,1)
    else:
        if (Ann_PrzrLevelHiLo == True):
            ARS()
            Ann_PrzrLevelHiLo = False
        annun_bus26.write_pin(10,0)
            
# przr level hihi lolo
    if ((PrzrLevel < 20) or (PrzrLevel > 90 )):
        if (Ann_PrzrLevelHiHiLoLo == False):
            AS()
            Ann_PrzrLevelHiHiLoLo = True
            if (Permissive == False):
                ReactorTrip = True
                if (PrzrLevel < 20):
                    print ('Rx Trip - Pressurizer Level Lo Lo')
                if (PrzrLevel > 90):
                    print ('Rx Trip - Pressurizer Level Hi Hi')
        annun_bus26.write_pin(2,1)
    else:
        if (Ann_PrzrLevelHiHiLoLo == True):
            ARS()
            Ann_PrzrLevelHiHiLoLo = False
        annun_bus26.write_pin(2,0)
            
            


# rcs low flow
    if (Loop1_Flow < 100) or (Loop2_Flow < 100):      
        if (Ann_RcsLoFlow == False):
            AS()
            Ann_RcsLoFlow = True
        annun_bus26.write_pin(14, 1)                
    if (Loop1_Flow == 100) and (Loop2_Flow == 100):
        if (Ann_RcsLoFlow == True):
            ARS()
            Ann_RcsLoFlow = False
        annun_bus26.write_pin(14, 0)

# rcp trip
    if (Rcp1 == False) or (Rcp2 == False): 
        if (Ann_RcpTrip == False):
            AS()
            Ann_RcpTrip = True
        annun_bus26.write_pin(12, 1)                
    if (Rcp1 == True) and (Rcp2 == True):
        if (Ann_RcpTrip == True):
            ARS()
            Ann_RcpTrip = False
        annun_bus26.write_pin(12, 0)


# manual rx trip
    if (ManRxTrip == True): 
        if (Ann_ManRxTrip == False):
            AS()
            Ann_ManRxTrip = True
        annun_bus26.write_pin(16, 1)                
    else:
        if (Ann_ManRxTrip == True):
            ARS()
            Ann_ManRxTrip = False
        annun_bus26.write_pin(16, 0)    



    if (ReactorTrip == True): 
        if (Ann_RxTrip == False):
            AS()
            Ann_RxTrip = True
        annun_bus26.write_pin(8, 1)                
    else:
        if (Ann_RxTrip == True):
            ARS()
            Ann_RxTrip = False
        annun_bus26.write_pin(8, 0)
        
###########################################################################
###########################################################################

    ControlRodSkip=ControlRodSkip+1
    if (ControlRodSkip == 10):
        ControlRodSkip = 1

        if (switch_bus21.read_pin(12) == 0) and PA(): # control rods in
            ControlRodsIn = True
        else:
            ControlRodsIn = False

        if (switch_bus21.read_pin(14) == 0) and PA(): # control rods out
            ControlRodsOut = True
        else:
            ControlRodsOut = False

    # control rods up/out

        if (ControlRodsOut == True): #cr up
            if (BankA<228):
                BankA=BankA+1
                if (BankA>199):
                    BankB=BankB+1
            else:
                if (BankB<228):
                    BankB=BankB+1
                    if (BankB>199):
                        BankC=BankC+1
                else:
                    if (BankC<228):
                        BankC=BankC+1
                        if (BankC>199):
                            BankD=BankD+1
                    else:
                        if (BankD<228):
                            BankD=BankD+1
                                
    # control rods down/in

        if (ControlRodsIn == True): #cr down
            if (BankD>0):
                BankD=BankD-1
                if (BankD<28):
                    BankC=BankC-1
            else:
                if (BankC>0):
                    BankC=BankC-1
                    if (BankC<28):
                        BankB=BankB-1
                else:
                    if (BankB>0):
                        BankB=BankB-1
                        if (BankB<28):
                            BankA=BankA-1
                    else:
                        if (BankA>0):
                            BankA=BankA-1
                                            

        
    BankA=float(BankA)
    BankB=float(BankB)
    BankC=float(BankC)
    BankD=float(BankD)
    
    skipper=skipper+1
    if skipper == 8: # this needs to be around 1 second - adjust as program gets longer

 #       for i in range(1,17):
 #           if (AnnunFlash27[10] == 'flash'):
 #               AnnunCounter=AnnunCounter+1
 #               if (AnnunCounter<11):
 #                   if (AnnunFlashToggle == True):
 #                       AnnunFlashToggle = False
 #                       annun_bus27.write_pin(i,0)
 #                   else:
 #                       AnnunFlashToggle = True
 #                       annun_bus27.write_pin(i,0)
 #               else:
 #                   AnnunFlash27[10] == 'on'
 #                   AnnunCounter = 0


        if (PrzrHeaters == True):
            PrzrLevel = PrzrLevel - 0.01
            #HeaterSpray = HeaterSpray + 0.25
        if (PrzrSpray == True):
            PrzrLevel = PrzrLevel + 0.01
            #HeaterSpray = HeaterSpray - 0.25


# reactor power calcs based on control rods
        RxPower=(BankA/228)*125*0.000009 + (BankB/228)*125*0.00009 + (BankC/228)*125*0.0009 + (BankD/228)*125*0.999 - 0.000844

        if (AccumulatorHasDischarged == True):  # if acc dump, heavy concentration of boron
            RxPower = RxPower*0.75
            
        if (ReactorTrip == True):
            start_time = time.time()
            run_time = 0
        else:
            run_time=int(time.time()-start_time)        

        skipper=1

# startup rate calculation
# only calculate for source/intermediate range

        if (LastRxPower!=0):
            StartUpRate=(RxPower-LastRxPower)/LastRxPower
        else:
            StartUpRate=0
                
        if (StartUpRate>2):
            print ('Hi Startup Rate" ', BankA, BankB, BankC, BankD, StartUpRate)

        LastRxPower=RxPower


# calculate delay power


        RxPowerDelayPower=RxPower*0.05

        for i in range(1,600):
            DelayPower[i]=DelayPower[i+1]

        DelayPower[600]=RxPowerDelayPower
        RxPowerPlusDelay = RxPower + DelayPower[1]
        RxPowerPlusDelay = RxPowerPlusDelay - (Power_Boron * RxPowerPlusDelay) # add in boron factor
        
# check radiation annun and trip
 
        temp = Radiation.HiRad(RxPowerPlusDelay, StartupRange, InterRange, PowerRange)
        if (temp == True):
            if (Ann_HiRad == False):
                print ('Procedure Violation - Power Detector Overange')
                ProcedureViolations = ProcedureViolations + 1
                AS()
                Ann_HiRad = True
            annun_bus26.write_pin(5, 1) # hi rad
        else:
            if (Ann_HiRad == True):
                ARS()
                Ann_HiRad = False
            annun_bus26.write_pin(5,0)

        temp = Radiation.HiRadTrip(RxPowerPlusDelay, StartupRange, InterRange, PowerRange)
        if (temp == True):
            if (Permissive == False):
                ReactorTrip = True
                print ('Rx Trip - Hi Containment Radiation Level')
                if (Ann_HiRadTrip == False):
                    AS()
                    Ann_HiRadTrip = True
                annun_bus26.write_pin(8, 1) # rx trip


        if (GenBreaker == True):
            MWH = MWH + GeneratorLoad / 100

# update screen with latest values/status       
        Display_Data.DisplayData('D',sim_win,run_time, RxPowerPlusDelay, BankA, BankB, BankC, BankD, StartUpRate,
                                 SdAfp_Flow, Mfp1_Flow, Mfp2_Flow, Afp1_Flow, Afp2_Flow, Loop1_Flow, Loop2_Flow,
                                 PriPorv_Display, SecPorv_Display, Rhr_Flow, Si_Flow, Charging_Flow, LetDown_Flow,
                                 Boron_Flow, Steam_Dump_Flow, Circ_Flow, Block_Valves_Display, TurbineSpeed_Display,
                                 GeneratorVoltage, PrimaryTemperature, SecondaryTemperature, Thot, Tcold, PrzrLevel,
                                 PrimaryPressure, GeneratorLoad, SgLevel1, SgLevel2, MWH, SecondaryPressure,
                                 ProcedureViolations)

######################################################################################################################
# EVENTS
######################################################################################################################

        if (RxPowerTotal >= EventRandomPower):
# loss of offsite power
            if (Operation == 'LossPower'):
                EventTimer = EventTimer + 1
                if (EventTimer > EventRandomTimer):
                    Operation = 'Normal'
                    OffSitePower = False
                    StartupTrans = False
                    AuxTrans = False

# rcp trip - rcp #1
            if (Operation == 'RcpTrip'):
                EventTimer = EventTimer + 1
                if (EventTimer > EventRandomTimer):
                    Operation = 'Normal'
                    Rcp1 = False                
                    Rcp1Thermal = 0.0        
                    Rcp1_Demand = 0.0

# mfp trip - mfp #2
            if (Operation == 'MfpTrip'):
                EventTimer = EventTimer + 1
                if (EventTimer > EventRandomTimer):
                    Operation = 'Normal'
                    Mfp2 = False

# turbine trip
            if (Operation == 'TurbineTrip'):
                EventTimer = EventTimer + 1
                if (EventTimer > EventRandomTimer):
                    Operation = 'Normal'
                    TurbineStatus = False
                    GenBreaker = False
                    GeneratorLoad = 0.0
                    MWH = 0.0

# circ water trip
            if (Operation == 'CircWaterTrip'):
                EventTimer = EventTimer + 1
                if (EventTimer > EventRandomTimer):
                    Operation = 'Normal'
                    CircWater = False
                    CircWater_Demand = 0

# primary porv
            if (Operation == 'PriPorvOpen'):
                EventTimer = EventTimer + 1
                if (EventTimer > EventRandomTimer):
                    Operation = 'Normal'
                    PriPorv = False
                    PriPorv_Demand = 0.0

# secondary porv
            if (Operation == 'SecPorvOpen'):
                EventTimer = EventTimer + 1
                if (EventTimer > EventRandomTimer):
                    Operation = 'Normal'
                    SecPorv = False
#                    SecPorv_Demand = 0.0  # need to support ramp up/down

                    
                   
############################################
#end skipper
############################################

        
######################################################################################################################
# CALCULATIONS - START
######################################################################################################################


    if (ReactorTrip == True):
        BankA = 0
        BankB = 0
        BankC = 0
        BankD = 0
        

    TotalFlow = ((float(Loop1_Flow) + float(Loop2_Flow)) / 2.0) 

    RxPowerTotal = RxPowerPlusDelay

    # Energy Primary
    #   507 on pump heat
    #   1114 @ 6% - delayed neutron value
    # so 800 will drag down temp.
    
    PrimaryThermal = RxPowerTotal + Rcp1Thermal + Rcp2Thermal

    EnergyPrimary = (PrimaryThermal * TotalFlow) - (Rhr_Flow * 8)
    EnergySecondary = GeneratorLoad * 100 + Steam_Dump_Flow * 75
    
    if (SecPorv == True):
        EnergySecondary = EnergySecondary + 10 * 100 # porv vents to atmosphere so circ water does not mater
            
  # rcs vol = 135
  # przr vol = 51
    
    V2 = RCSVolume+PrzrLevel*51/100

    PrimaryMass = PrimaryMass + Si_Temp/1000


    FlowStartUpCounter = FlowStartUpCounter + 1
    if (FlowStartUpCounter > 10): #20
        FlowStartUpCounter = 0
        if (FlowStartUp<120):
            FlowStartUp = FlowStartUp+xIncrement1+xIncrement2
    
    PrimaryTemperature = 3.75 * FlowStartUp+100 + ((100 - TotalFlow) * 50 / 100) * RxPowerTotal / 100 + (EnergyPrimary-EnergySecondary) / 95
    DeltaT = EnergySecondary / 10000.0 * 63.0
    Thot = DeltaT / 2 + PrimaryTemperature
    Tcold = PrimaryTemperature - DeltaT

    PrimaryPressure = 17.08 * FlowStartUp + 200 + ((100-TotalFlow) * 200 / 100) * RxPowerTotal / 100 + (EnergyPrimary - EnergySecondary) / 100
    PrimaryPressure = PrimaryPressure + ((160 * (PrimaryMass +LetDownCharging) / 100) / V2) * 1000 - 1000
    PrimaryPressure = PrimaryPressure - PriPorv_Temp

    PrimaryPressure = PrimaryPressure + (((PrimaryTemperature/555)-1) * 600)

    PrimaryPressure = PrimaryPressure + PrimaryPressure * (((-0.2*PrzrLevel)+10)/100)

    if (PrimaryPressure < 200):
        PrimaryPressure = 200
        
    #PrzrLevel = PrzrLevel + HeaterSpray
    if (PrzrLevel > 100):
        PrzrLevel = 100
    if (PrzrLevel < 10):
        PrzrLevel = 10
        
    
    SecondaryTemperature = (TotalFlow * PrimaryTemperature/100) - 25
    if (SecondaryTemperature<100):
        SecondaryTemperature = 100

    SecondaryPressure = SecondaryTemperature / 525 * 1000
    SecondaryPressure = SecondaryPressure + (EnergyPrimary - EnergySecondary + 500)/10
    if (SecPorv == True):
        SecondaryPressure = SecondaryPressure - 100
    if (SecondaryPressure < 200):
        SecondaryPressure = 200

    
    FwFlow = (Mfp1_Flow * 60 / 100) + (Mfp2_Flow * 60 / 100) + (Afp1_Flow * 5 / 100) + (Afp2_Flow * 5 / 100) + (SdAfp_Flow * 5 / 100)

    SgLevel = SgLevel + ((FwFlow * 100)-EnergySecondary)/10000
    SgLevel1 = SgLevel
    SgLevel2 = SgLevel
    




    if (SgLevel>90):
        ManTurbTrip = True
        TurbineStatus = False
        GenBreaker = False
        GeneratorLoad = 0.0        


######################################################################################################################
# PA() = False
######################################################################################################################


    if (PA() == False):
# RCP1
        Rcp1 = False
        Rcp1Thermal = 0.0
        Rcp1_Demand = 0.0
        xIncrement1 = 0.0
        Ann_RcpTrip = False
# RCP2
        Rcp2 = False
        Rcp2Thermal = 0.0
        Rcp2_Demand = 0.0
        xIncrement2 = 0.0
        Ann_RcpTrip = False
# FWP1
        Mfp1 = False
        Mfp1_Demand = 0
        Mfp1_Temp = 0
        Ann_FeedwaterStatus = False
# FWP2
        Mfp2 = False
        Mfp2_Demand = 0
        Mfp2_Temp = 0
        Ann_FeedwaterStatus = False
# AFP1
        Afp1 = False
        Afp1_Demand = 0
        Afp1_Temp = 0
        Ann_AuxFeedStatus = False
# AFP2
        Afp2 = False
        Afp2_Demand = 0
        Afp2_Temp = 0
        Ann_AuxFeedStatus = False
# RHR
        RhrPump = False
        Rhr_Demand = 10
        Rhr_Temp = 0
# SI
        Sip = False
        Si_Demand = 0
        Si_Temp = 0
        Ann_Sip = False
# CIRC
        CircWater = False
        CircWater_Demand = 0
        CircWater_Temp = 0
        Ann_CircWater = False
# Turbine trip / Gen / trip
        TurbineStatus = False
        GenBreaker = False
        GeneratorLoad = 0.0
        GenSync = False        
        MWH = 0.0
        TurbineSpeed_Demand = 0
        TurbineSpeed_Temp = 0
        Ann_TurbOverUnderSpeed = False
        Ann_TurbStatus = False
# Turbine Turning Gear off
        TurbTurnGear = False
# Steam Dump = False
        SteamDump = False       
        SteamDump_Demand = 0
        SteamDump_Temp = 0
        Ann_SteamDump = False



######################################################################################################################
# HALT SIM
######################################################################################################################

    if ( Permissive == False):
        if (PrimaryPressure > 2600):
            Halt.HaltSim(sim_win, 'Primary Pressure High:' + str(PrimaryPressure))
        if (PrzrLevel < 11):
            Halt.HaltSim(sim_win, 'Pressurizer Level Low:' + str(PrzrLevel))
        if (PrzrLevel > 99):
            Halt.HaltSim(sim_win, 'Pressurizer Level High:' + str(PrzrLevel))
        if (SgLevel > 99):
            Halt.HaltSim(sim_win, 'SG Level High:' + str(SgLevel))    
        if (SgLevel < 10):
            Halt.HaltSim(sim_win, 'SG Level Low:' + str(SgLevel))        
        if (PrimaryTemperature > 700):
            Halt.HaltSim(sim_win, 'Primary Temperature High:' + str(PrimaryTemperature))
        if (SecondaryPressure > 1500):
            Halt.HaltSim(sim_win, 'Secondary Temperature High:' + str(SecondaryTemperature))


######################################################################################################################
# PROCEDURE ERRORS  
######################################################################################################################

# Startup / Aux Transformers
    if ((GeneratorLoad > 5) and (OneTime_Transformer == True)):
        OneTime_Transformer = False
        if (StartupTrans == True):
            print ('Procedure Violation: Above 5% Generator Load, Switch to Aux Transformer')
            ProcedureViolations = ProcedureViolations + 1

# Feedwater Source
    if ((GeneratorLoad > 10) and (OneTime_FeedSource == True)):
        OneTime_FeedSource = False
        if ((Mfp1 == False) or (Mfp2 == False)):
            print ('Procedure Violation: Above 10% Generator Load, Switch to Main Feed Pumps')
            ProcedureViolations = ProcedureViolations + 1

# SG Level
    if ((RxPowerTotal > 0.1) and (OneTime_SgLevel == True)):
        OneTime_SgLevel = False
        if ((SgLevel < 50) or (SgLevel1 < 50) or (SgLevel < 50)):
            print ('Procedure Violation: Steam Generator Level(s) Must Be At Least 50% On Startup')
            ProcedureViolations = ProcedureViolations + 1
            
# Permissive
    if ((RxPowerTotal > 0.1) and (OneTime_Permissive == True)):
        OneTime_Permissive = False
        if (Permissive == True):
            print ('Procedure Violation: Permissives Must Be Set False When > 0.1% Rx Power')
            ProcedureViolations = ProcedureViolations +1

# Accumulator
    if ((RxPowerTotal > 0.1) and (OneTime_AccumulatorUnblock == True)):
        OneTime_AccumulatorUnblock = False
        if (BlockValves == True):
            print ('Procedure Violation: Accumulator Block Valve Must Be Open When > 0.1% Rx Power')
            ProcedureViolations = ProcedureViolations +1
            

            
######################################################################################################################
# EXIT SIMULATION
######################################################################################################################

# annunciators off
for i in range(1,17):
    annun_bus26.write_pin(i, 0)
    annun_bus27.write_pin(i, 0)    
    status_lights_bus24.write_pin(i,0)
    status_lights_bus25.write_pin(i,0)



print ('-------------')
print ('Simulation Exit')
print ('FlowStartUp', FlowStartUp)
print ('TotalFlow', TotalFlow)
print ('RxPower', RxPowerTotal)
print ('EP',EnergyPrimary)
print ('ES', EnergySecondary)
print ('Mass', PrimaryMass)
print ('LetdownCharging', LetDownCharging)
print ('V2', V2)
print ('Przr Level', PrzrLevel)
print ('Generator Load', GeneratorLoad)
print ('Steam Dump', SteamDump_Temp)
print ('Circ water', Circ_Flow)
print ('Total FW Flow', FwFlow)


print ('-------------')


# exit simulation
sim_win.close()



















        
        
