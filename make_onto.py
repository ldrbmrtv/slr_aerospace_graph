import pandas as pd
import os
import json
from owlready2 import *
import types


df_cl = pd.read_csv('classes.csv')

with open(os.path.join('data_subset/', 'instance_types_dicts.json')) as file:
    inst_data = json.load(file)

df_data = pd.read_csv(os.path.join('data_subset/', 'paper_instance_occurrence_matrix.csv'))

onto = get_ontology('http://tib.eu/slr')

with onto:

    # Classes
    for ind, row in df_cl.iterrows():
        cl = types.new_class(row['URI'], (Thing,))
        cl.label = row['Label']

    for key, value in inst_data.items():
        cl = onto.search_one(label = key)
        if cl:
            for item in value:
                inst = cl()
                inst.label = item

    Research = types.new_class('Research', (Thing,))
    mentions = types.new_class('mentions', (ObjectProperty,))
    for ind, row in df_data.iterrows():
        res_inst = Research()
        res_inst.label = row[0]
        for col in df_data.columns:
            if row[col]:
                inst = onto.search_one(label = col)
                if inst:
                    res_inst.mentions.append(inst)
                    

onto.save('onto.owl')
onto.destroy()
        
    
