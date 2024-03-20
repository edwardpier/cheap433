#! /usr/bin/python3

with open("samples") as f:
    
    last_power = None
    for i, line in enumerate(f):
        
        if line.startswith('#'):
            continue
        
        fields = line.split()
        real = float(fields[0])
        imag = float(fields[1])
        
        power = real*real + imag*imag
        
        if last_power is None:
            last_power = power
            
        else:
            print((last_power + power)*0.5)
            last_power = None
