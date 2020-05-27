
#path_to_xes_file ='./log/CCC19.xes'
path_to_xes_file ='./log/Sepsis_Cases.xes'

import pandas as pd

from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.util import func

variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply(path_to_xes_file,
                         variant=variant, parameters=parameters)

from pm4py.objects.log.exporter.xes import exporter as xes_exporter
log = func.filter_(lambda t: len(t) < 8, log)
xes_exporter.apply(log, 'test.xes')

from pm4py.algo.filtering.log.variants import variants_filter
variants = variants_filter.get_variants(log)




from pm4py.algo.filtering.log.attributes import attributes_filter
activities = attributes_filter.get_attribute_values(log, "concept:name")
resources = attributes_filter.get_attribute_values(log, "org:resource")

print(activities)

from pm4py.statistics.traces.log import case_statistics
variants_count = case_statistics.get_variant_statistics(log)
variants_count = sorted(variants_count, key=lambda x: x['count'], reverse=True)
print(variants_count)

#from pm4py.objects.log.exporter.xes import exporter as xes_exporter
#xes_exporter.apply(filtered_log_events, 'test.xes')
