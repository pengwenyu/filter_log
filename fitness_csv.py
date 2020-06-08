from pm4py.objects.log.importer.xes import importer as xes_importer
import os
import datetime
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
log_csv = pd.read_csv('./log/BPI2016_Complaints.csv', sep=',')
log = log_converter.apply(log_csv)

from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
heu_net = heuristics_miner.apply_heu(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
gviz = hn_visualizer.apply(heu_net)
#hn_visualizer.view(gviz)

from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
net, im, fm = heuristics_miner.apply(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})

print("alignment start")
starttime = datetime.datetime.now()
print(starttime)
from pm4py.algo.conformance.alignments import algorithm as alignments
alignments = alignments.apply_log(log, net, im, fm)
endtime = datetime.datetime.now()
print(endtime)
print("alignments success")
from pm4py.evaluation.replay_fitness import evaluator as replay_fitness
log_fitness = replay_fitness.evaluate(alignments, variant=replay_fitness.Variants.ALIGNMENT_BASED)

print(log_fitness)
print("system end")
final_time = endtime-starttime
print(final_time.seconds)