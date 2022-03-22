import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(suppress=True)
from scipy.cluster.vq import vq,kmeans,whiten
from pm4py.objects.log.importer.xes import importer as xes_importer
import os
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.evaluation.replay_fitness import evaluator as replay_fitness
import datetime
import random
from datetime import timedelta  
import time
fp=open('generate.xes')
lines = fp.readlines()
fp1=open('smaller.xes')
origin_lines = fp1.readlines()
fp2=open('smaller.xes')
lines2 = fp2.readlines()
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
event = ["Send Fine","Insert Fine Notification","Add penalty","Payment","Insert Date Appeal to Prefecture",
        "Send Appeal to Prefecture","Receive Result Appeal from Prefecture","Notify Result Appeal to Offender", "Appeal to Judge", "Send for Credit Collection",]
dependency=["Create Fine-Payment","Send Fine-Insert Fine Notification",
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
idx=[]
idx_event =[]
for i in range(len(lines2)):
    if'<trace>' in lines2[i]:
        idx.append(i)
        #print("trace start line ",i)
    if '</trace>' in lines2[i]:
        idx.append(i)
        #print("trace end line ", i)
    if'<event>' in lines2[i]:
        idx_event.append(i)
    if'</event>' in lines2[i]:
        idx_event.append(i)
log233=[]
head='<log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7">'+'\n'
tail= '</log>'
trace_head = '<trace>\n'
trace_tail = '</trace>\n'
#log233.append(head)
ts = datetime.datetime(2001, 1, 1)
#ts = ts+ timedelta(days=100) 
tend = datetime.datetime(2007, 12, 31)
nums = [210,210,220,220,210,220,210]#[0,0,0,0,0,0,0]#######################[210,210,220,220,210,220,210]
nums0 = nums[0]
for k in range(nums0):
    eve = np.random.choice(event,1)[0]
    log233.append(trace_head)
    dt = random.random()*(tend-ts) +ts
    eve_len = np.random.choice(range(10,100),1)[0]
    for i in range(eve_len):
        for j in range(len(lines)):
            if j == 1:
                if i == 0:
                    line = lines[j][:37]+"Send Fine"+'"/>\n'
                else:
                    line = lines[j][:37]+eve+'"/>\n'
                log233.append(line)
            elif j == 4:
                line = lines[j][:37]+str(dt)[:-1]+'"/>\n'
                log233.append(line)
            else:
                log233.append(lines[j])
        #print(np.random.choice(range(2,20),1)[0],int(np.random.choice(range(2,20),1)[0]))
        dt += timedelta(days=(int(np.random.choice(range(1,60),1)[0]))) 
        log233.append('\n')
    log233.append(trace_tail)
idxs = list(range(0,len(idx)-1,2))

nums1 = nums[1]
traces = np.random.choice(idxs,nums1)
for k in range(nums1):# Exclude head
    trace = traces[k]
    start = idx[trace]
    end = idx[trace+1]
    ignore = 1
    for i in range(start,end):
        if not ignore:
            log233.append(lines2[i])
            #print(lines2[i])
        if '</event>' in lines2[i] and ignore:
           log233.append('<trace>\n') 
           ignore = 0
    log233.append(trace_tail)

nums2 = nums[2]
traces = np.random.choice(idxs,nums2)
for k in range(nums2):  
    trace = traces[k]
    start = idx[trace]
    end = idx[trace+1]
    ignore = 0
    event_num = 0
    for i in range(start,end):
        if '<event>' in lines2[i]:
            event_num += 1
    even = 0
    for i in range(start,end):
        if not ignore:
            log233.append(lines2[i])
        if '</event>' in lines2[i] and not ignore:
            even += 1
            if even==event_num-1:
                #log233.append('<trace>\n') 
                ignore = 1
    log233.append(trace_tail)

nums3 = nums[3]
traces = np.random.choice(idxs,nums3)
for k in range(nums3):  
    trace = traces[k]
    start = idx[trace]
    end = idx[trace+1]
    ignore = 0
    event_num = 0
    for i in range(start,end):
        if '<event>' in lines2[i]:
            event_num += 1
    Event = np.random.choice(range(event_num),1)[0]
    even = 0
    for i in range(start,end):
        if '<event>' in lines2[i]:
            if not ignore and even==Event:
                    ignore = 1
            if ignore and even==Event+1:
                ignore = 0
            even += 1
        if not ignore:
            log233.append(lines2[i])
    log233.append(trace_tail)

nums4 = nums[4]
traces = np.random.choice(idxs,nums4)
for k in range(nums4): #Change name 
    trace = traces[k]
    start = idx[trace]
    end = idx[trace+1]
    locate = 0
    event_num = 0
    for i in range(start,end):
        if '<event>' in lines2[i]:
            event_num += 1
    Event = np.random.choice(range(event_num),2,replace=False)[0]
    even = 0
    for i in range(start,end):
        if '<event>' in lines2[i]:
            if not locate and even==Event:
                locate = 1
            if locate and even==Event+1:
                locate = 0
            even += 1
        if locate and '<string key="concept:name" value="' in lines2[i]:
            name = np.random.choice(event,1)[0]
            newline = lines2[i][:37]+str(name)+'"/>\n'
            #print(newline)
            log233.append(newline)
        else:
            log233.append(lines2[i])
    log233.append(trace_tail)

nums5 = nums[5]
traces = np.random.choice(idxs,nums5) 
for k in range(nums5): #exchange name
    trace = traces[k]
    start = idx[trace]
    end = idx[trace+1]
    locate = 0
    event_num = 0
    events = []
    for i in range(start,end):
        if '<event>' in lines2[i]:
            event_num += 1
        if '<string key="concept:name" value="' in lines2[i]:
            events.append(lines2[i][37:-4])
    events=events[1:]
    if  event_num==1:
        break
    e1,e2 = np.random.choice(range(event_num),2,replace=False)
    even = 0
    for i in range(start,end):
        if '<event>' in lines2[i]:
            if not locate and (even==e1 or even==e2):
                locate = 1
            if locate and (even==e1+1 or even==e2+1):
                locate = 0
            even += 1
        if locate and '<string key="concept:name" value="' in lines2[i]:
            name = lines2[i][37:-4]
            if name == events[e1]:
                newline = lines2[i][:37]+str(events[e2])+'"/>\n'
            elif name == events[e2]:
                newline = lines2[i][:37]+str(events[e1])+'"/>\n'
            #print(newline)
            log233.append(newline)
        else:
            log233.append(lines2[i])
    log233.append(trace_tail)

nums6 = nums[6]
traces = np.random.choice(idxs,nums6)
for k in range(nums6): 
    trace = traces[k]
    #print("TA",trace)
    start = idx[trace]
    end = idx[trace+1]
    locate = 0
    event_num = 0
    e_lens = []
    e_len = 0
    for i in range(start,end):
        if '<event>' in lines2[i]:
            event_num += 1
            e_len = 1
        elif e_len>0:
            e_len += 1
        if '</event>' in lines2[i]:
            e_lens += [e_len]
    #print(e_lens)
    Event = np.random.choice(range(event_num),1)[0]
    even = 0
    #end += e_lens[Event]
    rep_event = []
    e_flag = 0
    for i in range(start,end):
        line2 = lines2[i]
        if '<event>' in line2:
            real_len = 0
            e_flag = 1
            if not locate and even==Event:
                locate = 1
            if locate and even==Event+1:
                locate = 0
            even += 1
        if locate:
            rep_event.append(line2)
        log233.append(line2)
        #print(len(rep_event), e_lens[Event])
        if len(rep_event) == e_lens[Event]:
            for item in rep_event:
                log233.append(item)
                #print(item)
            rep_event = []
    log233.append(trace_tail)

log233.append(tail)
with open('repeat.xes','w') as file:
    for i in range(len(origin_lines)-1):
        file.write(origin_lines[i])
       
    for i in range(len(log233)):
        file.write(log233[i])
    file.close()
