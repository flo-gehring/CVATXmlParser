import csv

f = open("BA-01.txt")
r = open("BA-001.txt", "w")


rep = csv.reader(f)


"""      names=['FrameId', 'Id', 'X', 'Y', 'Width', 'Height', 'Confidence', 'ClassId', 'Visibility', 'unused'], 
"""

for line in rep:
    if(len(line) > 0):
        
        r.write("\t".join(line[0:6] + ['1', '1', line[6], '0']) + "\n")
        
                       
    
