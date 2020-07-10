import numpy as np
import random
COUNT=2000
fp=open('./BPI 2020/cluster 4 time/log4.xes')
lines = fp.readlines()

idx=[]

for i in range(len(lines)):
    if'<trace>' in lines[i]:
        idx.append(i)
    if '</trace>' in lines[i]:
        idx.append(i)
print('the number of trace is',len(idx)/2)
trace_number = int(len(idx)/2)
resultList=[]

resultList=random.sample(range(0,trace_number),COUNT);
resultList =np.sort(resultList)


head='<log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7">'+'\n'
tail= '</log>'

index = 0
new_line=[]
new_line.append(head)
for i in range(0,len(idx)):
    if index==COUNT:
        break
    start = idx[resultList[index]*2]
    end= idx[resultList[index]*2+1]
    for j in range(start,end+1):
        new_line.append(lines[j])

    index=index+1

new_line.append(tail)

new_idx=[]
for i in range(len(new_line)):
    if'<trace>' in new_line[i]:
        new_idx.append(i)
    if '</trace>' in new_line[i]:
        new_idx.append(i)

#print(len(new_idx)/2)
#file=open('./log/2000trace.xes','w')
#for i in range(len(new_line)):
#    file.write(new_line[i]);
#file.close()