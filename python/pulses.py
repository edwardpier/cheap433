#! /usr/bin/python3


tick0 = None
with open('zz') as f_in:
    with open('zpulse', 'w') as f_out:
    
    
        start = None
        last_start = None
        for line in f_in:
            
            fields = line.split()
            tick = int(fields[0])
            level = int(fields[1])
            
            if tick0 is None:
                tick0 = tick

            if level == 1:
                # start of a pulse
                last_start = start
                start = tick
            elif not      start is None and \
                 not last_start is None:
                # end of a pulse
                duration = tick - start
                interval = start - last_start
                
                time = (start-tick0)/1e6
                print(time, interval, duration, file=f_out)
                

            

        
        
        
        
