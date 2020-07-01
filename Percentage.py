import glob
import os
paths=[]
for root,dirs,files in os.walk('./road_traffic'):
    for file in files:
        path=os.path.join(root,file)
        if path.endswith('.xes'):
            print(path)
            fp = open(path)
            lines = fp.readlines()
            idx = []
            for i in range(len(lines)):
                if '<trace>' in lines[i]:
                    idx.append(i)
                if '</trace>' in lines[i]:
                    idx.append(i)
            print('the number of trace is', len(idx) / 2)