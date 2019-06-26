from zellegraphics import *
from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
from ABE_ADCPi import ADCPi

def InitCond(sim_win, adc1, adc2, switch_bus21):

    DispImage = Image(Point(750,450), 'InitScreen.gif')
    DispImage.draw(sim_win)
    z=0

    lv1 = False
    lv2 = False
    lv3 = False
    lv4 = False
    lv5 = False
    lv6 = False
    lv7 = False
    lv7 = False
    lv8 = False
    lv9 = False
    lv10 = False
    lv11 = False
    lv12 = False
    lv13 = False
    lv14 = False
    lv15 = False
    lsw1 = False
    lsw2 = False

    v1 = 99 # boron
    v2 = 0 # turbine coarse
    v3 = 0 # turbine fine
    v4 = 0 # generator load
    v5 = 0 # generator voltage
    v6 = 10 # rhr
    v7 = 0 # si
    v8 = 50 # letdown
    v9 = 50 # charging
    v10 = 0 # steam dump
    v11 = 0 # sdafp
    v12 = 0 # afp 1
    v13 = 0 # afp 2
    v14 = 0 # mfp 1
    v15 = 0 # mfp 2

    message1 = Text(Point(250,665), '')
    message1.setTextColor('red')
    message1.setStyle('bold')
    message1.setSize(8)
    message1.draw(sim_win)

    message2 = Text(Point(240,635), '')
    message2.setTextColor('red')
    message2.setStyle('bold')
    message2.setSize(8)
    message2.draw(sim_win)

    message3 = Text(Point(225,605), '')
    message3.setTextColor('red')
    message3.setStyle('bold')
    message3.setSize(8)
    message3.draw(sim_win)

    message4 = Text(Point(225,605), '')
    message4.setTextColor('red')
    message4.setStyle('bold')
    message4.setSize(8)
    message4.draw(sim_win)

    message5 = Text(Point(225,605), '')
    message5.setTextColor('red')
    message5.setStyle('bold')
    message5.setSize(8)
    message5.draw(sim_win)

    message6 = Text(Point(225,605), '')
    message6.setTextColor('red')
    message6.setStyle('bold')
    message6.setSize(8)
    message6.draw(sim_win)

    message7 = Text(Point(225,605), '')
    message7.setTextColor('red')
    message7.setStyle('bold')
    message7.setSize(8)
    message7.draw(sim_win)

    message8 = Text(Point(225,605), '')
    message8.setTextColor('red')
    message8.setStyle('bold')
    message8.setSize(8)
    message8.draw(sim_win)

    message9 = Text(Point(225,605), '')
    message9.setTextColor('red')
    message9.setStyle('bold')
    message9.setSize(8)
    message9.draw(sim_win)

    message10 = Text(Point(225,605), '')
    message10.setTextColor('red')
    message10.setStyle('bold')
    message10.setSize(8)
    message10.draw(sim_win)

    message11 = Text(Point(225,605), '')
    message11.setTextColor('red')
    message11.setStyle('bold')
    message11.setSize(8)
    message11.draw(sim_win)

    message12 = Text(Point(225,605), '')
    message12.setTextColor('red')
    message12.setStyle('bold')
    message12.setSize(8)
    message12.draw(sim_win)

    message13 = Text(Point(225,605), '')
    message13.setTextColor('red')
    message13.setStyle('bold')
    message13.setSize(8)
    message13.draw(sim_win)

    message14 = Text(Point(225,605), '')
    message14.setTextColor('red')
    message14.setStyle('bold')
    message14.setSize(8)
    message14.draw(sim_win)

    message15 = Text(Point(225,605), '')
    message15.setTextColor('red')
    message15.setStyle('bold')
    message15.setSize(8)
    message15.draw(sim_win)

    message16 = Text(Point(225,605), '')
    message16.setTextColor('red')
    message16.setStyle('bold')
    message16.setSize(8)
    message16.draw(sim_win)







    AdjVol=4.87
                               
    while z==0:
        time.sleep(0.50)
        if (lv1 == True and lv2 == True and lv3 == True and lv4 == True and lv5 == True and lv6 == True and
             lv7 == True and lv8 == True and lv9 == True and lv10 == True and lv11 == True and lv12 == True
            and lv13 == True and lv14 == True and lv15 == True and lsw1 == True and lsw2 == True):
            z = 1

        # boron
        v = int(round(adc2.read_voltage(6)/AdjVol*100,0))     
        c = 'green'
        if (v < v1 or v > v1):
            c = 'red'
            lv1 = False
        else:
            c='green'
            lv1 = True
        message1.undraw()
        temp=str(v)
        message1 = Text(Point(250,660), temp)
        message1.setTextColor(c)
        message1.setStyle('bold')
        message1.setSize(8)
        message1.draw(sim_win)

        # turbine coarse
        v = int(round(adc2.read_voltage(1)/AdjVol*100,0))     
        c = 'green'
        if (v < v2 or v > v2):
            c = 'red'
            lv2 = False
        else:
            c='green'
            lv2 = True
        message2.undraw()
        temp=str(v)
        message2 = Text(Point(240,630), temp)
        message2.setTextColor(c)
        message2.setStyle('bold')
        message2.setSize(8)
        message2.draw(sim_win)

        # turbine fine
        v = int(round(adc2.read_voltage(5)/AdjVol*100,0))     
        c = 'green'
        if (v < v3 or v > v3):
            c = 'red'
            lv3 = False
        else:
            c='green'
            lv3 = True
        message3.undraw()
        temp=str(v)
        message3 = Text(Point(225,600), temp)
        message3.setTextColor(c)
        message3.setStyle('bold')
        message3.setSize(8)
        message3.draw(sim_win)

        # generator load
        v = int(round(adc2.read_voltage(7)/AdjVol*100,0))     
        c = 'green'
        if (v < v4 or v > v4):
            c = 'red'
            lv4 = False
        else:
            c='green'
            lv4 = True
        message4.undraw()
        temp=str(v)
        message4 = Text(Point(245,570), temp)
        message4.setTextColor(c)
        message4.setStyle('bold')
        message4.setSize(8)
        message4.draw(sim_win)

        # generator voltage
        v = int(round(adc2.read_voltage(4)/AdjVol*100,0))     
        c = 'green'
        if (v < v5 or v > v5):
            c = 'red'
            lv5 = False
        else:
            c='green'
            lv5 = True
        message5.undraw()
        temp=str(v)
        message5 = Text(Point(260,540), temp)
        message5.setTextColor(c)
        message5.setStyle('bold')
        message5.setSize(8)
        message5.draw(sim_win)

        # rhr
        v = int(round(adc2.read_voltage(2)/AdjVol*100,0))     
        c = 'green'
        if (v < v6 or v > v6):
            c = 'red'
            lv6 = False
        else:
            c='green'
            lv6 = True
        message6.undraw()
        temp=str(v)
        message6 = Text(Point(180,510), temp)
        message6.setTextColor(c)
        message6.setStyle('bold')
        message6.setSize(8)
        message6.draw(sim_win)

        # si
        v = int(round(adc2.read_voltage(3)/AdjVol*100,0))     
        c = 'green'
        if (v < v7 or v > v7):
            c = 'red'
            lv7 = False
        else:
            c='green'
            lv7 = True
        message7.undraw()
        temp=str(v)
        message7 = Text(Point(240,480), temp)
        message7.setTextColor(c)
        message7.setStyle('bold')
        message7.setSize(8)
        message7.draw(sim_win)

        # charging
        v = int(round(adc1.read_voltage(5)/AdjVol*100,0))     
        c = 'green'
        if (v < v8 or v > v8):
            c = 'red'
            lv8 = False
        else:
            c='green'
            lv8 = True
        message8.undraw()
        temp=str(v)
        message8 = Text(Point(205,450), temp)
        message8.setTextColor(c)
        message8.setStyle('bold')
        message8.setSize(8)
        message8.draw(sim_win)

        # letdown
        v = int(round(adc1.read_voltage(2)/AdjVol*100,0))     
        c = 'green'
        if (v < v9 or v > v9):
            c = 'red'
            lv9 = False
        else:
            c='green'
            lv9 = True
        message9.undraw()
        temp=str(v)
        message9 = Text(Point(205,420), temp)
        message9.setTextColor(c)
        message9.setStyle('bold')
        message9.setSize(8)
        message9.draw(sim_win)

        # steam dump
        v = int(round(adc1.read_voltage(6)/AdjVol*100,0))     
        c = 'green'
        if (v < v10 or v > v10):
            c = 'red'
            lv10 = False
        else:
            c='green'
            lv10 = True
        message10.undraw()
        temp=str(v)
        message10 = Text(Point(225,390), temp)
        message10.setTextColor(c)
        message10.setStyle('bold')
        message10.setSize(8)
        message10.draw(sim_win)

        # sdafp
        v = int(round(adc1.read_voltage(7)/AdjVol*100,0))     
        c = 'green'
        if (v < v11 or v > v11):
            c = 'red'
            lv11 = False
        else:
            c='green'
            lv11 = True
        message11.undraw()
        temp=str(v)
        message11 = Text(Point(225,360), temp)
        message11.setTextColor(c)
        message11.setStyle('bold')
        message11.setSize(8)
        message11.draw(sim_win)

        # afp 1
        v = int(round(adc1.read_voltage(8)/AdjVol*100,0))     
        c = 'green'
        if (v < v12 or v > v12):
            c = 'red'
            lv12 = False
        else:
            c='green'
            lv12 = True
        message12.undraw()
        temp=str(v)
        message12 = Text(Point(215,330), temp)
        message12.setTextColor(c)
        message12.setStyle('bold')
        message12.setSize(8)
        message12.draw(sim_win)

        # afp 2
        v = int(round(adc1.read_voltage(3)/AdjVol*100,0))     
        c = 'green'
        if (v < v13 or v > v13):
            c = 'red'
            lv13 = False
        else:
            c='green'
            lv13 = True
        message13.undraw()
        temp=str(v)
        message13 = Text(Point(215,300), temp)
        message13.setTextColor(c)
        message13.setStyle('bold')
        message13.setSize(8)
        message13.draw(sim_win)

        # mfp 1
        v = int(round(adc1.read_voltage(4)/AdjVol*100,0))     
        c = 'green'
        if (v < v14 or v > v14):
            c = 'red'
            lv14 = False
        else:
            c='green'
            lv14 = True
        message14.undraw()
        temp=str(v)
        message14 = Text(Point(185,270), temp)
        message14.setTextColor(c)
        message14.setStyle('bold')
        message14.setSize(8)
        message14.draw(sim_win)

        # mfp 2
        v = int(round(adc1.read_voltage(1)/AdjVol*100,0))     
        c = 'green'
        if (v < v15 or v > v15):
            c = 'red'
            lv15 = False
        else:
            c='green'
            lv15 = True
        message15.undraw()
        temp=str(v)
        message15 = Text(Point(185,240), temp)
        message15.setTextColor(c)
        message15.setStyle('bold')
        message15.setSize(8)
        message15.draw(sim_win)

        # control rods
        temp = 'Center'
        lsw1 = True
        lsw2 = True
        c = 'green'
        if (switch_bus21.read_pin(12) == 0):
            temp = 'Rods In'
            c = 'red'
            lsw1 = False
        if (switch_bus21.read_pin(14) == 0):
            temp = 'Rods Out'
            c = 'red'
            lsw2 = False                
        message16.undraw()
        message16 = Text(Point(265,180), temp)                
        message16.setTextColor(c)
        message16.setStyle('bold')
        message16.setSize(8)
        message16.draw(sim_win)





