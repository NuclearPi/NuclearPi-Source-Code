from zellegraphics import *
import time


def HaltSim(win, reason):
    DispImage = Image(Point(750,450),'sim_out_of_range.gif')
    DispImage.draw(win)    

    print ('Sim Halted: ',reason)
    
    a=0
    while a == 0: 
        time.sleep(2)
        print ('Simulation Halted')

