import pandas as pd
import os
import json
from owlready2 import *
import types


instance_data = 'obsidian_folder.json'

def create_instance(label):
    inst = onto.search_one(label = label)
    if not inst:
        cl = onto.search_one(label = inst_data_inverse[label])
        if cl:
            inst = cl()
            inst.label = label
    return inst


df_cl = pd.read_csv('classes.csv')
df_contributions = pd.read_csv(os.path.join('data_subset/', 'paper_instance_occurrence_matrix.csv'))
df_rules = pd.read_csv(os.path.join('data_subset/', 'rules_cross_type.csv'))

with open(os.path.join('data_subset/', instance_data)) as file:
    inst_data = json.load(file)

inst_data_inverse = {}
for key, value in inst_data.items():
    for item in value:
        inst_data_inverse[item] = key

onto = get_ontology('http://tib.eu/slr')

with onto:

    # Classes
    for ind, row in df_cl.iterrows():
        cl = types.new_class(row['URI'], (Thing,))
        cl.label = row['Label']
        re = types.new_class(f'has{row["Label"].title().replace(" ", "")}', (ObjectProperty,))
        re.label = f'has {row["Label"]}'

    # Rules
    for ind, row in df_rules.iterrows():
        subj_inst = create_instance(row['antecedents'])
        obj_inst = create_instance(row['consequents'])
        if subj_inst and obj_inst:
            obj_cl = obj_inst.is_a[0]
            rel_label = f'has {str(obj_cl.label[0])}'
            rel = onto.search_one(label = rel_label)
            if rel:
                rel[subj_inst].append(obj_inst)        

onto.save('onto_only_rules.owl')
onto.destroy()
        
    
