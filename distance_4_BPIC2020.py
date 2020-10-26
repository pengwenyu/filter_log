
import numpy as np
from scipy.cluster.vq import vq,kmeans,whiten
event=['Declaration SUBMITTED by EMPLOYEE', 'Declaration FINAL_APPROVED by SUPERVISOR', 'Request Payment',
       'Payment Handled', 'Declaration APPROVED by PRE_APPROVER',
       'Declaration REJECTED by PRE_APPROVER', 'Declaration REJECTED by EMPLOYEE',
       'Declaration REJECTED by SUPERVISOR', 'Declaration APPROVED by ADMINISTRATION', 'Declaration APPROVED by BUDGET OWNER',
        'Declaration REJECTED by ADMINISTRATION',
        'Declaration FOR_APPROVAL by ADMINISTRATION']
#read log file
fp=open('./log/BPI 2020/DomesticDeclarations.xes')
lines = fp.readlines()

idx=[]

for i in range(len(lines)):
    if'<trace>' in lines[i]:
        idx.append(i)
        #print("trace start line ",i)
    if '</trace>' in lines[i]:
        idx.append(i)
        #print("trace end line ", i)
print(len(idx))
vector_space = []
for i in range(len(idx)):
    if i== len(idx)-1:
        break
    start = idx[i]
    end = idx[i+1]
    j = start
    array = np.zeros(14)
    for j in range(start,end):
        for k in range(len(event)):
            if event[k] in lines[j]:
                array[k]=array[k]+1
    if (np.all(array==0))==0:
        #print(array)
        vector_space.append(array)
    i=i+2
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