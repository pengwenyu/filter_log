from itsdangerous import NoneAlgorithm
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
np.set_printoptions(suppress=True)
from scipy.cluster.vq import vq,kmeans,whiten
from pm4py.objects.log.importer.xes import importer as xes_importer
import os
import numpy as np
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.evaluation.replay_fitness import evaluator as replay_fitness
import datetime
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
#read log file
#fp=open('log/Road_Traffic_Fine_Management_Process.xes')
fp=open('repeat.xes')
lines = fp.readlines()

def get_event_name(lines,start,end):
    find_all = lambda data, s: [r for r in range(len(data)) if data[r] == s]
    event_name = None
    for i in range(start,end):
        if "concept:name" in lines[i]:
            r_list = find_all(lines[i], '"')
            event_name = lines[i][r_list[2]+1:r_list[3]]
    if event_name is None:
        for i in range(start,end):
            #print(lines[i])
            pass
    return  event_name

def get_event_time(lines,start,end):
    find_all = lambda data, s: [r for r in range(len(data)) if data[r] == s]
    for i in range(start,end):
        if "time:timestamp" in lines[i]:
            r_list = find_all(lines[i], '"')
            event_time = lines[i][r_list[2]+1:r_list[3]-15]
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

print("IDXXXXXXXX",len(idx),len(idx)/2)
start_event=event[0]
vector_space = []
index_in_event =0

sum_time=0
average_time=19.301498656255745
times = []
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
    for k in range(0,event_in_trace):
        event_start = idx_event[index_in_event]
        event_end = idx_event[index_in_event + 1]
        event_name = get_event_name(lines, event_start, event_end)
        if event_name is None:
            print(i,k,idx[i])
        event_time = get_event_time(lines, event_start, event_end)
        #times += [event_time.days]
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
    #print("DEP",dep)
    vector_space.append(np.hstack((array, dep)))
times = np.array(times)
print("TIME",np.shape(times))
#print(sum_time/17/150370)
vector_space = np.array(vector_space)
vmean = np.mean(vector_space,axis = 0)
vec = vector_space - vmean
vstd = np.std(vec,axis = 0)
vec  /= vstd
#vec = whiten(vector_space)
#vec = (vector_space)
#print('STD',np.std(vec,axis = 0))
#print("MEAN",np.mean(vec,axis = 0))
#cov = np.cov(vec.T)
#svec = vec[:,23]
#his = np.histogram(svec,bins = 50)
#xx = list(range(np.shape(his)[1]))9
#plt.hist(his)
#plt.show()
#ax = sn.heatmap(cov, annot=False, fmt='g')
#plt.show()
#fig,ax = plt.subplots()
#ax.boxplot(vector_space,whis=[5, 95])
#ax.set_xlabel("vector index")
#ax.set_yscale('log')
#plt.show()
np.save('vec.npy',vec)
vec = vec[5000:,:]
#exit(0)

start = datetime.datetime.now()
tot_fit = []
sum_fit = []
for i in range(1):
    centroids,_=kmeans(vec,3)
    #print(centroids)
    result,_=vq(vec,centroids)
    #np.save('result.npy',result)
    print("DONE")
    (unique, counts) = np.unique(result, return_counts=True)
    frequencies = np.asarray((unique, counts)).T
    print("Freq",frequencies)
    freq = np.array(counts)/sum(counts)
    np.save('freq.npy',freq)
    end = datetime.datetime.now()

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
    fits = 0
    for i in range(len(freq)):
        log = xes_importer.apply(os.path.join("log{}.xes".format(i+1)))
        print("log{}.xes".format(i+1))
        heu_net = heuristics_miner.apply_heu(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
        
        #gviz = hn_visualizer.apply(heu_net)
        #hn_visualizer.view(gviz)
        net, im, fm = heuristics_miner.apply(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})

        from pm4py.algo.conformance.alignments import algorithm as alignments
        alignments = alignments.apply_log(log, net, im, fm)
        
        log_fitness = replay_fitness.evaluate(alignments, variant=replay_fitness.Variants.ALIGNMENT_BASED)
        fit = log_fitness['averageFitness']
        fits += fit*freq[i]
    tot_fit += [fits]
    sumfit = sum(tot_fit)/len(tot_fit)
    sum_fit += [sumfit]
    print('Current accuracy',sumfit)
print(sum_fit)