#! /usr/bin/python3


tick0 = None
with open('zz') as f_in:
    with open('z', 'w') as f_out:
    
        for line in f_in:
            
            fields = line.split()
            tick = int(fields[0])
            level = int(fields[1])
            
            if tick0 is None:
                tick0 = tick
                
            time = (tick - tick0)
            
            print(time, 1-level, file=f_out)
            print(time, level, file=f_out)
        
        
        
        
