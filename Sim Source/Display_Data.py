from zellegraphics import *
from array import *
from random import randrange, uniform

def DisplayData(Switcher,win, run_time, RxPower,
                BankA,BankB,BankC,BankD, StartUpRate,
                SdAfp_Flow, Mfp1_Flow, Mfp2_Flow, Afp1_Flow, Afp2_Flow,
                Loop1_Flow, Loop2_Flow, PriPorv_Display, SecPorv_Display,
                Rhr_Flow, Si_Flow, Charging_Flow, LetDown_Flow, Boron_Flow,
                Steam_Dump_Flow, Circ_Flow, Block_Valves_Display, TurbineSpeed_Display,
                GeneratorVoltage, PrimaryTemperature, SecondaryTemperature, Thot, Tcold,
                PrzrLevel, PrimaryPressure, GeneratorLoad, SgLevel1, SgLevel2, MWH, SecondaryPressure,
                ProcedureViolations):


    global message1,message2,message3,message4,message5,message6,message7,message8,message9,message10
    global message11,message12,message13,message14,message15,message16,message17,message18,message19,message20
    global message21,message22,message23,message24,message25,message26,message27,message28,message29,message30
    global message31, message32, message33, message34, message35, message36, message37, message38
    global xLine

    global DisplayPower

    RxPowerE = '{:.2e}'.format(RxPower)

    if (StartUpRate == 0):
        StartUpRateE = 0
    else:
        StartUpRateE = '{:.2e}'.format(StartUpRate)



# display current data
    if Switcher=='D':

        
        message1.undraw()
        temp=str(SdAfp_Flow) + "%"
        message1 = Text(Point(985,475), temp) #sdafp
        message1.setTextColor('red')
        message1.setStyle('bold')
        message1.setSize(8)
        message1.draw(win)

        message2.undraw()
        temp=str(Afp2_Flow) + "%"
        message2 = Text(Point(985,525), temp) #mdafp 2
        message2.setTextColor('red')
        message2.setStyle('bold')
        message2.setSize(8)
        message2.draw(win)

        message3.undraw()
        temp=str(Afp1_Flow) + "%"
        message3 = Text(Point(985,580), temp) #mdafp 1 995
        message3.setTextColor('red')
        message3.setStyle('bold')
        message3.setSize(8)
        message3.draw(win)

        message4.undraw()
        temp=str(Mfp2_Flow) + "%"
        message4 = Text(Point(985,640), temp) #fp 2
        message4.setTextColor('red')
        message4.setStyle('bold')
        message4.setSize(8)
        message4.draw(win)

        message5.undraw()
        temp=str(Mfp1_Flow) + "%"
        message5 = Text(Point(985,700), temp) #fp 1
        message5.setTextColor('red')
        message5.setStyle('bold')
        message5.setSize(8)
        message5.draw(win)


        message6.undraw()
        temp = str(int(GeneratorLoad * 950 / 100)) + ' MW'
        message6 = Text(Point(960,330), temp) #generator power
        message6.setTextColor('red')
        message6.setStyle('bold')
        message6.setSize(8)
        message6.draw(win)


        message7.undraw()
        temp=str(int(GeneratorVoltage)) + ' KV'
        message7 = Text(Point(960,245), temp) #generator voltage
        message7.setTextColor('red')
        message7.setStyle('bold')
        message7.setSize(8)
        message7.draw(win)

        message8.undraw()
        temp=str(int(20*TurbineSpeed_Display)) + ' rpm'
        message8 = Text(Point(885,300), temp) #turbine speed
        message8.setTextColor('red')
        message8.setStyle('bold')
        message8.setSize(8)
        message8.draw(win)


        message9.undraw()
        temp=str(Circ_Flow) + "%"
        message9 = Text(Point(1040,45), temp) #circ water
        message9.setTextColor('red')
        message9.setStyle('bold')
        message9.setSize(8)
        message9.draw(win)


        message10.undraw()
        temp=str(Steam_Dump_Flow) + "%"
        message10 = Text(Point(620,250), temp) #steam dump
        message10.setTextColor('red')
        message10.setStyle('bold')
        message10.setSize(8)
        message10.draw(win)

        message11.undraw()
        temp=str(Boron_Flow) + "%"
        message11 = Text(Point(490,235), temp) #boron
        message11.setTextColor('red')
        message11.setStyle('bold')
        message11.setSize(8)
        message11.draw(win)

        message12.undraw()
        temp=str(Si_Flow) + "%"
        message12 = Text(Point(378,265), temp) #si
        message12.setTextColor('red')
        message12.setStyle('bold')
        message12.setSize(8)
        message12.draw(win)

        message13.undraw()
        temp=str(LetDown_Flow) + "%"
        message13 = Text(Point(290,250), temp) #letdown
        message13.setTextColor('red')
        message13.setStyle('bold')
        message13.setSize(8)
        message13.draw(win)

        message14.undraw()
        temp=str(Charging_Flow) + "%"
        message14 = Text(Point(130,250), temp) #charging
        message14.setTextColor('red')
        message14.setStyle('bold')
        message14.setSize(8)
        message14.draw(win)

        message15.undraw()
        temp=int(BankA)
        message15 = Text(Point(115,105), temp) #cr bank a
        message15.setTextColor('red')
        message15.setStyle('bold')
        message15.setSize(8)
        message15.draw(win)

        message16.undraw()
        temp=int(BankB)
        message16 = Text(Point(245,105), temp) #cr bank b
        message16.setTextColor('red')
        message16.setStyle('bold')
        message16.setSize(8)
        message16.draw(win)

        message17.undraw()
        temp=int(BankC)
        message17 = Text(Point(390,105), temp) #cr bank c
        message17.setTextColor('red')
        message17.setStyle('bold')
        message17.setSize(8)
        message17.draw(win)

        message18.undraw()
        temp=int(BankD)
        message18 = Text(Point(510,105), temp) #cr bank d
        message18.setTextColor('red')
        message18.setStyle('bold')
        message18.setSize(8)
        message18.draw(win)

        message19.undraw()
        temp = str(int(SgLevel1)) + ' %'
        message19 = Text(Point(35,665), temp) #sg 1 level
        message19.setTextColor('red')
        message19.setStyle('bold')
        message19.setSize(8)
        message19.draw(win)

        message20.undraw()
        temp = str(int(SgLevel2)) + ' %'
        message20 = Text(Point(505,665), temp) #sg 2 level
        message20.setTextColor('red')
        message20.setStyle('bold')
        message20.setSize(8)
        message20.draw(win)

        message21.undraw()
        temp = str(round(PrzrLevel,1)) + "%"
        message21 = Text(Point(406,682), temp) #przr level
        message21.setTextColor('red')
        message21.setStyle('bold')
        message21.setSize(8)
        message21.draw(win)

        message22.undraw()
        message22 = Text(Point(1335,825), run_time) #rx uptime
        message22.setTextColor('red')
        message22.setStyle('bold')
        message22.setSize(8)
        message22.draw(win)

        message23.undraw()
        temp = round(MWH,1)
        message23 = Text(Point(1330,735), temp) #MWH
        message23.setTextColor('red')
        message23.setStyle('bold')
        message23.setSize(8)
        message23.draw(win)

        message24.undraw()
        message24 = Text(Point(1330,655), ProcedureViolations) #procedure violations
        message24.setTextColor('red')
        message24.setStyle('bold')
        message24.setSize(8)
        message24.draw(win)

        message25.undraw()
        temp = str(int(PrimaryPressure)) + ' psig'
        message25 = Text(Point(295,615), temp) #rx pressure
        message25.setTextColor('white')
        message25.setStyle('bold')
        message25.setSize(8)
        message25.draw(win)

        message26.undraw()
        temp = str(int(PrimaryTemperature)) + ' Degf'
        message26 = Text(Point(295,630), temp) #rx temp
        message26.setTextColor('white')
        message26.setStyle('bold')
        message26.setSize(8)
        message26.draw(win)

        message27.undraw()
        temp = str(int(SecondaryTemperature)) + ' Degf'
        message27 = Text(Point(205,800), temp) #sec temp
        message27.setTextColor('red')
        message27.setStyle('bold')
        message27.setSize(8)
        message27.draw(win)

        message28.undraw()
        temp = str(int(SecondaryPressure)) + ' psig'
        message28 = Text(Point(340,800), temp) #sec pressure
        message28.setTextColor('red')
        message28.setStyle('bold')
        message28.setSize(8)
        message28.draw(win)

        message29.undraw()
        message29 = Text(Point(215,500), Loop1_Flow) #pri flow sg1
        message29.setTextColor('red')
        message29.setStyle('bold')
        message29.setSize(8)
        message29.draw(win)

        message30.undraw()
        temp=str(Rhr_Flow) + "%"
        message30 = Text(Point(545,425), temp) #rhr
        message30.setTextColor('red')
        message30.setStyle('bold')
        message30.setSize(8)
        message30.draw(win)

        message31.undraw()
        message31 = Text(Point(325,35), StartUpRateE) #startup rate
        message31.setTextColor('red')
        message31.setStyle('bold')
        message31.setSize(8)
        message31.draw(win) 
 
        message32.undraw()
        message32 = Text(Point(370,500), Loop2_Flow) #pri flow sg2
        message32.setTextColor('red')
        message32.setStyle('bold')
        message32.setSize(8)
        message32.draw(win)

        message33.undraw()
        temp=str(float(RxPowerE)) + "%"
        message33 = Text(Point(295,515), temp) #rx power %
        message33.setTextColor('white')
        message33.setStyle('bold')
        message33.setSize(8)
        message33.draw(win)

        message34.undraw()
        message34 = Text(Point(492,822), SecPorv_Display) #sec porv
        message34.setTextColor('red')
        message34.setStyle('bold')
        message34.setSize(8)
        message34.draw(win)

        message35.undraw()
        message35 = Text(Point(510,710), PriPorv_Display) #pri porv old 695,525
        message35.setTextColor('red')
        message35.setStyle('bold')
        message35.setSize(8)
        message35.draw(win)

        message36.undraw()
        message36 = Text(Point(460,535), Block_Valves_Display) #accumulator
        message36.setTextColor('red')
        message36.setStyle('bold')
        message36.setSize(8)
        message36.draw(win)

        message37.undraw()
        temp = int(Thot)
        message37 = Text(Point(215,455), temp) #Thot
        message37.setTextColor('red')
        message37.setStyle('bold')
        message37.setSize(8)
        message37.draw(win)

        message38.undraw()
        temp = int(Tcold)
        message38 = Text(Point(375,420), temp) #Tcold
        message38.setTextColor('red')
        message38.setStyle('bold')
        message38.setSize(8)
        message38.draw(win)




        xLine.undraw() # rx power line
        NewY = 0
        for i in range(1,826):
            if (RxPower > DisplayPower[i]):
                NewY = i*270/825
                
        #NewY = (BankA+BankB+BankC+BankD) * 270 / 912
        xLine=Line(Point(1312,325+NewY), Point(1326,325+NewY))
        xLine.setOutline('red')
        xLine.draw(win)        
        

# init screen display vars
    if Switcher=='I':




        DisplayPower = array('d',[0])
        for i in range(1,826):
            DisplayPower.append(0)

        BankA = 0.0
        BankB = 0.0
        BankC = 0.0
        BankD = 0.0

        for i in range(1,826):
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
            step1 = BankA/228
            step2 = step1*125
            part1 = step2*0.000009

            step1 = BankB/228
            step2 = step1*125
            part2 = step2*0.00009

            step1 = BankC/228
            step2 = step1*125
            part3 = step2*0.0009

            step1 = BankD/228
            step2 = step1*125
            part4 = step2*0.999 - 0.000844

            DisplayPower[i] = part1+part2+part3+part4



        print ("Display Power array init completed")    





        message1 = Text(Point(985,475), '####%') #sdafp
        message1.setTextColor('red')
        message1.setStyle('bold')
        message1.setSize(8)
        message1.draw(win)

        message2 = Text(Point(985,525), '####%') #mdafp 2
        message2.setTextColor('red')
        message2.setStyle('bold')
        message2.setSize(8)
        message2.draw(win)

        message3 = Text(Point(985,580), '####%') #mdafp 1 995
        message3.setTextColor('red')
        message3.setStyle('bold')
        message3.setSize(8)
        message3.draw(win)

        message4 = Text(Point(985,640), '####%') #fp 2
        message4.setTextColor('red')
        message4.setStyle('bold')
        message4.setSize(8)
        message4.draw(win)

        message5 = Text(Point(985,700), '####%') #fp 1
        message5.setTextColor('red')
        message5.setStyle('bold')
        message5.setSize(8)
        message5.draw(win)


        message6 = Text(Point(960,330), '#### Mw') #generator power
        message6.setTextColor('red')
        message6.setStyle('bold')
        message6.setSize(8)
        message6.draw(win)


        message7 = Text(Point(960,245), '#### kv') #generator voltage
        message7.setTextColor('red')
        message7.setStyle('bold')
        message7.setSize(8)
        message7.draw(win)

        message8 = Text(Point(885,300), '#### rpm') #turbine speed
        message8.setTextColor('red')
        message8.setStyle('bold')
        message8.setSize(8)
        message8.draw(win)


        message9 = Text(Point(1040,45), '####%') #circ water
        message9.setTextColor('red')
        message9.setStyle('bold')
        message9.setSize(8)
        message9.draw(win)


        message10 = Text(Point(620,250), '####%') #steam dump
        message10.setTextColor('red')
        message10.setStyle('bold')
        message10.setSize(8)
        message10.draw(win)

        message11 = Text(Point(490,235), '####%') #boron
        message11.setTextColor('red')
        message11.setStyle('bold')
        message11.setSize(8)
        message11.draw(win)

        message12 = Text(Point(378,265), '####%') #si
        message12.setTextColor('red')
        message12.setStyle('bold')
        message12.setSize(8)
        message12.draw(win)

        message13 = Text(Point(290,250), '####%') #letdown
        message13.setTextColor('red')
        message13.setStyle('bold')
        message13.setSize(8)
        message13.draw(win)

        message14 = Text(Point(130,250), '####%') #charging
        message14.setTextColor('red')
        message14.setStyle('bold')
        message14.setSize(8)
        message14.draw(win)

        message15 = Text(Point(115,105), '####') #cr bank a
        message15.setTextColor('red')
        message15.setStyle('bold')
        message15.setSize(8)
        message15.draw(win)

        message16 = Text(Point(245,105), '####') #cr bank b
        message16.setTextColor('red')
        message16.setStyle('bold')
        message16.setSize(8)
        message16.draw(win)

        message17 = Text(Point(390,105), '####') #cr bank c
        message17.setTextColor('red')
        message17.setStyle('bold')
        message17.setSize(8)
        message17.draw(win)

        message18 = Text(Point(510,105), '####') #cr bank d
        message18.setTextColor('red')
        message18.setStyle('bold')
        message18.setSize(8)
        message18.draw(win)

        label1 = Text(Point(35,680),'Level')  # level text sg 1 35,695
        label1.setTextColor('red')
        label1.setStyle('bold')
        label1.setSize(8)
        label1.draw(win)

        message19 = Text(Point(35,665), '####%') #sg 1 level  35,680
        message19.setTextColor('red')
        message19.setStyle('bold')
        message19.setSize(8)
        message19.draw(win)

        label1 = Text(Point(505,680),'Level')  # level text sg 2   505,695
        label1.setTextColor('red')
        label1.setStyle('bold')
        label1.setSize(8)
        label1.draw(win)

        message20 = Text(Point(505,665), '####%') #sg 2 level   505,680
        message20.setTextColor('red')
        message20.setStyle('bold')
        message20.setSize(8)
        message20.draw(win)

        label1 = Text(Point(406,697),'Level')  # level text przr  406,682
        label1.setTextColor('red')
        label1.setStyle('bold')
        label1.setSize(8)
        label1.draw(win)

        message21 = Text(Point(406,682), '####%') #przr level  406,667
        message21.setTextColor('red')
        message21.setStyle('bold')
        message21.setSize(8)
        message21.draw(win)

        message22 = Text(Point(1335,825), 'xxxx') #reactor critical time
        message22.setTextColor('red')
        message22.setStyle('bold')
        message22.setSize(8)
        message22.draw(win)

        message23 = Text(Point(1330,735), '####') #MWH
        message23.setTextColor('red')
        message23.setStyle('bold')
        message23.setSize(8)
        message23.draw(win)

        message24 = Text(Point(1330,655), '####') #procedure violations
        message24.setTextColor('red')
        message24.setStyle('bold')
        message24.setSize(8)
        message24.draw(win)

        message25 = Text(Point(295,615), '#### psig') #rx pressure
        message25.setTextColor('white')
        message25.setStyle('bold')
        message25.setSize(8)
        message25.draw(win)

        message26 = Text(Point(295,630), '#### DegF') #rx temp
        message26.setTextColor('white')
        message26.setStyle('bold')
        message26.setSize(8)
        message26.draw(win)

        message27 = Text(Point(205,800), '#### Degf') #sec temp
        message27.setTextColor('red')
        message27.setStyle('bold')
        message27.setSize(8)
        message27.draw(win)

        message28 = Text(Point(340,800), '#### psig') #sec pressure
        message28.setTextColor('red')
        message28.setStyle('bold')
        message28.setSize(8)
        message28.draw(win)

        label1 = Text(Point(215,515),'Flow')  # flow text sg1
        label1.setTextColor('red')
        label1.setStyle('bold')
        label1.setSize(8)
        label1.draw(win)

        message29 = Text(Point(215,500), '####%') #pri flow sg1
        message29.setTextColor('red')
        message29.setStyle('bold')
        message29.setSize(8)
        message29.draw(win)

        message30 = Text(Point(545,425), '####%') #rhr
        message30.setTextColor('red')
        message30.setStyle('bold')
        message30.setSize(8)
        message30.draw(win)

        message31 = Text(Point(325,35), '####%') #startup rate
        message31.setTextColor('red')
        message31.setStyle('bold')
        message31.setSize(8)
        message31.draw(win) 
 
        label1 = Text(Point(370,515),'Flow')  # flow text sg2
        label1.setTextColor('red')
        label1.setStyle('bold')
        label1.setSize(8)
        label1.draw(win)

        message32 = Text(Point(370,500), '####%') #pri flow sg2
        message32.setTextColor('red')
        message32.setStyle('bold')
        message32.setSize(8)
        message32.draw(win)

        message33 = Text(Point(295,515), '####%') #rx power %
        message33.setTextColor('white')
        message33.setStyle('bold')
        message33.setSize(8)
        message33.draw(win)

        message34 = Text(Point(492,822), 'CLOSED') #sec porv
        message34.setTextColor('red')
        message34.setStyle('bold')
        message34.setSize(8)
        message34.draw(win)

        message35 = Text(Point(510,710), 'CLOSED') #pri porv old 695, 525
        message35.setTextColor('red')
        message35.setStyle('bold')
        message35.setSize(8)
        message35.draw(win)

        message36 = Text(Point(460,535), 'CLOSED') #accumulator
        message36.setTextColor('red')
        message36.setStyle('bold')
        message36.setSize(8)
        message36.draw(win)

        tempmess = Text(Point(215,465), 'Thot') #Thot label
        tempmess.setTextColor('red')
        tempmess.setStyle('bold')
        tempmess.setSize(8)
        tempmess.draw(win)
        
        message37 = Text(Point(215,455), '####') #Thot
        message37.setTextColor('red')
        message37.setStyle('bold')
        message37.setSize(8)
        message37.draw(win)

        tempmess = Text(Point(375,430), 'Tcold') #Tcold label
        tempmess.setTextColor('red')
        tempmess.setStyle('bold')
        tempmess.setSize(8)
        tempmess.draw(win)
        
        message38 = Text(Point(375,420), '') #Tcold
        message38.setTextColor('red')
        message38.setStyle('bold')
        message38.setSize(8)
        message38.draw(win)



        xLine=Line(Point(1315,325), Point(1325,325))
        xLine.draw(win)
