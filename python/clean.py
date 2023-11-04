
data = []

with open("z") as f:
    
    for line in f:
        
        fields = line.split()
        time = float(fields[0])
        on = int(fields[1])
        
        data.append({'time':time, 'on':on})
            

deleted = {}
for i in range(0, len(data)-2):
    
    if data[i  ]['on'] == data[i+1]['on'] and \
       data[i+1]['on'] == data[i+2]['on']:
           
       deleted[i+1] = 1
       
print(len(data), len(deleted))
       
clean = []
for i, entry in enumerate(data):
    
    if not i in deleted:
        print(entry['time'], entry['on'])
        

    
        

        
        
