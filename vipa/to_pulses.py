#! /usr/bin/python3


with open("samples") as f:
    
    last_level = None
    start_time = None
    for i, line in enumerate(f):
        
        if line.startswith('#'):
            continue
        
        fields = line.split()
        real = float(fields[0])
        imag = float(fields[1])
        
        power = real*real + imag*imag
        
        if power > 15: level = 1
        else:      level = 0
        
        if last_level is None:
            last_level = level
            
        elif last_level != level:
            
            if level == 1:
                start_time = i
            else:
                duration = i - start_time
                print(start_time, duration)
                
            last_level = level
            
            
