import numpy as np
np.set_printoptions(suppress=True)
from scipy.cluster.vq import vq,kmeans,whiten
import datetime
event = ['NEW', 'FIN', 'RELEASE', 'CODE OK', 'BILLED', 'DELETE', 'REOPEN', 'CHANGE DIAGN', 'STORNO',
 'REJECT', 'CODE NOK', 'SET STATUS', 'MANUAL', 'JOIN-PAT', 'CODE ERROR', 'EMPTY']
dependency=['NEW-FIN','NEW-CHANGE DIAGN','NEW-DELETE','FIN-RELEASE','FIN-REOPEN','REOPEN-FIN','CHANGE DIAGN-FIN',
            'RELEASE-CODE NOK','RELEASE-CODE OK','RELEASE-SET STATUS','RELEASE-CODE ERROR','REJECT-RELEASE',
            'SET STATUS-RELEASE','CODE ERROR-RELEASE','CODE OK-BILLED','CODE OK-SET STATUS','CODE OK-REOPEN',
            'CODE NOK-CODE OK','MANUAL-CODE OK','SET STATUS-CODE OK','BILLED-MANUAL','BILLED-STORNO',
            'CODE NOK-BILLED','MANUAL-BILLED','STORNO-BILLED','REJECT-BILLED','MANUAL-CODE NOK','CODE NOK-MANUAL',
            'STORNO-REJECT','CODE NOK-EMPTY','CODE NOK-SET STATUS','CODE NOK-REOPEN',
            'REOPEN-CHANGE DIAGN','REOPEN-DELETE','CHANGE DIAGN-DELETE',
]
#read log file
fp=open('./Hospital Billing/Hospital Billing.xes')
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

import random
from scipy.spatial import distance
from scipy import sparse
from numpy import mat
from sklearn.metrics.pairwise import pairwise_distances

def canopy(X, T1, T2, distance_metric='euclidean', filemap=None):
    canopies = dict()
    X1_dist = pairwise_distances(X, metric=distance_metric)
    canopy_points = set(range(X.shape[0]))
    while canopy_points:
        point = canopy_points.pop()
        i = len(canopies)
        canopies[i] = {"c": point, "points": list(np.where(X1_dist[point] < T2)[0])}
        canopy_points = canopy_points.difference(set(np.where(X1_dist[point] < T1)[0]))
    if filemap:
        for canopy_id in canopies.keys():
            canopy = canopies.pop(canopy_id)
            canopy2 = {"c": filemap[canopy['c']], "points": list()}
            for point in canopy['points']:
                canopy2["points"].append(filemap[point])
            canopies[canopy_id] = canopy2
    return canopies

distnace_metrix=[]
resultList=random.sample(range(0,100000),50)

for i in range(0,50):
    for j in range(0,100000):
        vec1 = vector_space[resultList[i]]
        vec2 = vector_space[j]
        dist = distance.euclidean(vec1,vec2)
        distnace_metrix.append(dist)
distnace_metrix.sort()

l= len(distnace_metrix)
print(l)
T1 =distnace_metrix[int(l*0.25)]
T2 =distnace_metrix[int(l*0.75)]
print(T1)
print(T2)
new_space=[]
resultList=random.sample(range(0,100000),20000)
for i in range(0,len(resultList)):
    new_space.append(vector_space[resultList[i]])
X= np.array(new_space)
#print(X)
X = sparse.csr_matrix(X)
#print(X)
# 300 500
start = datetime.datetime.now()
c=canopy(X,T1,T2,distance_metric='euclidean', filemap=None)
end = datetime.datetime.now()
canopy_time=end-start
print ('running time is',end-start)
print('Length of canopy is ',len(c))


start = datetime.datetime.now()
centroids,_=kmeans(vector_space,7)
result,_=vq(vector_space,centroids)
end = datetime.datetime.now()
print ('k-means package running time is',end-start)

start = datetime.datetime.now()
from kmeans import kmeans
dataSet = mat(new_space)
k = 6
centroids, clusterAssment = kmeans(dataSet, k)
end = datetime.datetime.now()
print ('k-means running time is',end-start)

centroids=[]
space=[]
for i in range(0,len(c)):
    #print(c[i])
    centroids.append(c[i]['c'])
    s=c[i]['points']
    for j in range(0,len(s)):
        space.append(s[j])
#print(centroids)
#print(space)
start = datetime.datetime.now()
result,_=vq(space,centroids)
end = datetime.datetime.now()
canopy_time=canopy_time+end-start
print ('canopy running time is',canopy_time)

log1=[]
log2=[]
log3=[]
log4=[]
log5=[]
log6=[]
head='<log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7">'+'\n'
tail= '</log>'

log1.append(head)
log2.append(head)
log3.append(head)
log4.append(head)
log5.append(head)
log6.append(head)

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
#write to file

log1.append(tail)
log2.append(tail)
log3.append(tail)
log4.append(tail)
log5.append(tail)
log6.append(tail)

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
