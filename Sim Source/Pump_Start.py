

Demand = 100

Current = 0

for i in range(1,800):

    Current=float(Current) + float((Demand-Current)/100 ) 
    print (Current, int(round(Current,0)))
