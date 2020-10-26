import numpy as np
np.set_printoptions(suppress=True)
from scipy.cluster.vq import vq,kmeans,whiten
import datetime
event=['Declaration SUBMITTED by EMPLOYEE', 'Declaration FINAL_APPROVED by SUPERVISOR', 'Request Payment',
       'Payment Handled', 'Declaration APPROVED by PRE_APPROVER',
       'Declaration REJECTED by PRE_APPROVER', 'Declaration REJECTED by EMPLOYEE',
       'Declaration REJECTED by SUPERVISOR', 'Declaration APPROVED by ADMINISTRATION', 'Declaration APPROVED by BUDGET OWNER',
        'Declaration REJECTED by ADMINISTRATION',
        'Declaration FOR_APPROVAL by ADMINISTRATION']

dependency=['Declaration SUBMITTED by EMPLOYEE-Declaration FINAL_APPROVED by SUPERVISOR', 'Declaration FINAL_APPROVED by SUPERVISOR-Request Payment',
            'Request Payment-Payment Handled','Declaration SUBMITTED by EMPLOYEE-Declaration APPROVED by PRE_APPROVER',
            'Declaration APPROVED by PRE_APPROVER-Declaration FINAL_APPROVED by SUPERVISOR',
            'Declaration SUBMITTED by EMPLOYEE-Declaration REJECTED by PRE_APPROVER',
            'Declaration SUBMITTED by EMPLOYEE-Declaration FOR_APPROVAL by ADMINISTRATION',
            'Declaration FOR_APPROVAL by ADMINISTRATION-Declaration SUBMITTED by EMPLOYEE',
            'Declaration REJECTED by EMPLOYEE-Declaration SUBMITTED by EMPLOYEE',
            'Declaration SUBMITTED by EMPLOYEE-Declaration APPROVED by ADMINISTRATION',
            'Declaration APPROVED by ADMINISTRATION-Declaration FINAL_APPROVED by SUPERVISOR',
            'Declaration APPROVED by ADMINISTRATION-Declaration APPROVED by BUDGET OWNER',
            'Declaration APPROVED by ADMINISTRATION-Declaration REJECTED by SUPERVISOR',
            'Declaration APPROVED by BUDGET OWNER-Declaration FINAL_APPROVED by SUPERVISOR',
            'Declaration REJECTED by SUPERVISOR-Declaration REJECTED by EMPLOYEE',
            'Declaration SUBMITTED by EMPLOYEE-Declaration REJECTED by ADMINISTRATION',
            'Declaration REJECTED by ADMINISTRATION-Declaration REJECTED by EMPLOYEE'
            ]
#read log file
fp=open('./log/BPI 2020/DomesticDeclarations.xes')
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
            event_time = lines[i][r_list[2]+1:r_list[3]-19]
            #print(event_time)
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
        last_event = event_name
        time_dependency=event_time
        index_in_event=index_in_event+2

    vector_space.append(np.hstack((array, dep)))
print("calculate done")
print(len(vector_space))

centroids,_=kmeans(vector_space,5)
result,_=vq(vector_space,centroids)


cluster1=[]
cluster2=[]
cluster3=[]
cluster4=[]
cluster5=[]
cluster6=[]
for i in range(0,len(vector_space)):
    if result[i]==0:
        cluster1.append(vector_space[i])
    if result[i]==1:
        cluster2.append(vector_space[i])
    if result[i]==2:
        cluster3.append(vector_space[i])
    if result[i]==3:
        cluster4.append(vector_space[i])
    if result[i]==4:
        cluster5.append(vector_space[i])
    if result[i]==5:
        cluster6.append(vector_space[i])
print("calculation start")
sum=0
times=0
for i in range(0,len(cluster1)):
    for j in range(i,len(cluster1)):
        dist = np.linalg.norm(cluster1[i] - cluster1[j])
        sum=sum+dist
        times=times+1
print(sum/times)
sum=0
times=0
for i in range(0,len(cluster2)):
    for j in range(i,len(cluster2)):
        dist = np.linalg.norm(cluster2[i] - cluster2[j])
        sum=sum+dist
        times=times+1
print(sum/times)
sum=0
times=0
for i in range(0,len(cluster3)):
    for j in range(i,len(cluster3)):
        dist = np.linalg.norm(cluster3[i] - cluster3[j])
        sum=sum+dist
        times=times+1
print(sum/times)
sum=0
times=0
for i in range(0,len(cluster4)):
    for j in range(i,len(cluster4)):
        dist = np.linalg.norm(cluster4[i] - cluster4[j])
        sum=sum+dist
        times=times+1
print(sum/times)
sum=0
times=0
for i in range(0,len(cluster5)):
    for j in range(i,len(cluster5)):
        dist = np.linalg.norm(cluster5[i] - cluster5[j])
        sum=sum+dist
        times=times+1
print(sum/times)