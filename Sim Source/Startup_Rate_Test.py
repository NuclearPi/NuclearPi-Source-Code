BankA=0
BankB=0
BankC=0
BankD=0
LastRxPower = 0


for i in range(1,2000):
    ControlRodsOut=True
    
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
                                
    BankA=float(BankA)
    BankB=float(BankB)
    BankC=float(BankC)
    BankD=float(BankD)

    RxPower=(BankA/228)*125*0.000009 + (BankB/228)*125*0.00009 + (BankC/228)*125*0.0009 + (BankD/228)*125*0.999 - 0.000844


    if (LastRxPower!=0):
        StartUpRate=(RxPower-LastRxPower)/LastRxPower
    else:
        StartUpRate=0
                
    if (StartUpRate>0.5):
        print ('Hi Startup Rate" ', int(BankA), int(BankB), int(BankC), int(BankD), StartUpRate)

    LastRxPower=RxPower

