import numpy as np
np.set_printoptions(suppress=True)
from scipy.cluster.vq import vq,kmeans,whiten

import datetime
event = ["Create Fine","Send Fine","Insert Fine Notification","Add penalty","Payment","Insert Date Appeal to Prefecture",
        "Send Appeal to Prefecture","Receive Result Appeal from Prefecture","Notify Result Appeal to Offender", "Appeal to Judge", "Send for Credit Collection",]
dependency=["Create Fine-Send Fine","Create Fine-Payment","Send Fine-Insert Fine Notification",
            "Send Fine-Payment","Insert Fine Notification-Insert Date Appeal to Prefecture",
            "Insert Fine Notification-Add penalty",
            "Insert Fine Notification-Payment","Insert Fine Notification-Appeal to Judge",
            "Insert Date Appeal to Prefecture-Send Appeal to Prefecture",
            "Send Appeal to Prefecture-Receive Result Appeal from Prefecture",
            "Receive Result Appeal from Prefecture-Notify Result Appeal to Offender",
            "Notify Result Appeal to Offender-Appeal to Judge",
            "Notify Result Appeal to Offender-Send for Credit Collection",
            "Notify Result Appeal to Offender-Payment",
            "Payment-Add penalty","Add penalty-Payment","Add penalty-Send for Credit Collection"]
#read log file
fp=open('./road_traffic/Road_Traffic_Fine_Management_Process.xes')
lines = fp.readlines()

def get_event_name(lines,start,end):
    find_all = lambda data, s: [r for r in range(len(data)) if data[r] == s]
    for i in range(start,end):
        if "concept:name" in lines[i]:
            r_list = find_all(lines[i], '"')
            event_name = lines[i][r_list[2]+1:r_list[3]]
    return  event_name

def get_event_time(lines,start,end):
    find_all = lambda data, s: [r for r in range(len(data)) if data[r] == s]
    for i in range(start,end):
        if "time:timestamp" in lines[i]:
            r_list = find_all(lines[i], '"')
            event_time = lines[i][r_list[2]+1:r_list[3]-15]
    event_time=datetime.datetime.strptime(event_time,"%Y-%m-%d")
    return  event_time

idx=[]
idx_event =[]
for i in range(len(lines)):
    if'<trace>' in lines[i]:
        idx.append(i)
        #print("trace start line ",i)
    if '</trace>' in lines[i]:
        idx.append(i)
        #print("trace end line ", i)
    if'<event>' in lines[i]:
        idx_event.append(i)
    if'</event>' in lines[i]:
        idx_event.append(i)

print(len(idx))
print(len(idx_event))
print(len(dependency))

start_event=event[0]
vector_space = []
index_in_event =0

sum_time=0
average_time=19.301498656255745
for i in range(0,len(idx),2):
    if i== len(idx)-1:
        break
    start = idx[i]
    end = idx[i+1]
    j = start
    array = np.zeros(len(event))
    dep=np.zeros(len(dependency))
    time_dependency= datetime.datetime.today()
    last_event=start_event
    event_in_trace =0
    for j in range(start,end):
        if '<event>' in lines[j]:
            event_in_trace=event_in_trace+1
    #print(event_in_trace)
    for k in range(0,event_in_trace):
        event_start = idx_event[index_in_event]
        event_end = idx_event[index_in_event + 1]
        event_name = get_event_name(lines, event_start, event_end)
        event_time = get_event_time(lines, event_start, event_end)
        for m in range(len(event)):
            if event_name==event[m]:
                array[m]=array[m]+1
        if event_name == start_event:
            time_dependency=event_time
        else:
            edge = last_event + '-' + event_name
            for z in range(0, len(dependency)):
                if edge in dependency[z]:
                    final_time=event_time-time_dependency
                    dep[z]= final_time.days
                    sum_time=sum_time+final_time.days
        last_event = event_name
        time_dependency=event_time
        index_in_event=index_in_event+2

    vector_space.append(np.hstack((array, dep)))
print("calculate done")
#print(vector_space)
#print(sum_time/17/150370)

start = datetime.datetime.now()
centroids,_=kmeans(vector_space,5)
#print(centroids)
result,_=vq(vector_space,centroids)
end = datetime.datetime.now()
print ('running time is',end-start)

log1=[]
log2=[]
log3=[]
log4=[]
log5=[]
log6=[]
log7=[]
log8=[]
log9=[]
log10=[]
log11=[]
log12=[]

head='<log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7">'+'\n'
tail= '</log>'

log1.append(head)
log2.append(head)
log3.append(head)
log4.append(head)
log5.append(head)
log6.append(head)
log7.append(head)
log8.append(head)
log9.append(head)
log10.append(head)
log11.append(head)
log12.append(head)
for i in range(len(result)):
    start = idx[2*i]
    end = idx[2*i+1]
    if result[i]==0:
        for j in range(start, end):
            log1.append(lines[j])
        log1.append(lines[j+1])
    if result[i]==1:
        for j in range(start, end):
            log2.append(lines[j])
        log2.append(lines[j + 1])
    if result[i]==2:
        for j in range(start, end):
            log3.append(lines[j])
        log3.append(lines[j+1])
    if result[i]==3:
        for j in range(start, end):
            log4.append(lines[j])
        log4.append(lines[j + 1])
    if result[i]==4:
        for j in range(start, end):
            log5.append(lines[j])
        log5.append(lines[j+1])
    if result[i]==5:
        for j in range(start, end):
            log6.append(lines[j])
        log6.append(lines[j + 1])
    if result[i]==6:
        for j in range(start, end):
            log7.append(lines[j])
        log7.append(lines[j+1])
    if result[i]==7:
        for j in range(start, end):
            log8.append(lines[j])
        log8.append(lines[j + 1])
    if result[i]==8:
        for j in range(start, end):
            log9.append(lines[j])
        log9.append(lines[j+1])
    if result[i]==9:
        for j in range(start, end):
            log10.append(lines[j])
        log10.append(lines[j + 1])
    if result[i]==10:
        for j in range(start, end):
            log11.append(lines[j])
        log11.append(lines[j+1])
    if result[i]==11:
        for j in range(start, end):
            log12.append(lines[j])
        log12.append(lines[j + 1])
#write to file

log1.append(tail)
log2.append(tail)
log3.append(tail)
log4.append(tail)
log5.append(tail)
log6.append(tail)
log7.append(tail)
log8.append(tail)
log9.append(tail)
log10.append(tail)
log11.append(tail)
log12.append(tail)

file=open('log1.xes','w')
for i in range(len(log1)):
    file.write(log1[i]);
file.close()

#write to file
file=open('log2.xes','w')
for i in range(len(log2)):
    file.write(log2[i]);
file.close()

#write to file
file=open('log3.xes','w')
for i in range(len(log3)):
    file.write(log3[i]);
file.close()

#write to file
file=open('log4.xes','w')
for i in range(len(log4)):
    file.write(log4[i]);
file.close()

#write to file
file=open('log5.xes','w')
for i in range(len(log5)):
    file.write(log5[i]);
file.close()

#write to file
file=open('log6.xes','w')
for i in range(len(log6)):
    file.write(log6[i]);
file.close()


file=open('log7.xes','w')
for i in range(len(log7)):
    file.write(log7[i]);
file.close()

#write to file
file=open('log8.xes','w')
for i in range(len(log8)):
    file.write(log8[i]);
file.close()

#write to file
file=open('log9.xes','w')
for i in range(len(log9)):
    file.write(log9[i]);
file.close()

#write to file
file=open('log10.xes','w')
for i in range(len(log10)):
    file.write(log10[i]);
file.close()

#write to file
file=open('log11.xes','w')
for i in range(len(log11)):
    file.write(log11[i]);
file.close()

#write to file
file=open('log12.xes','w')
for i in range(len(log12)):
    file.write(log12[i]);
file.close()
