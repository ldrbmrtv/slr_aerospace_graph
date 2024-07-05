import pandas as pd
import os
import json
from owlready2 import *
import types


df_cl = pd.read_csv('classes.csv')
df_contributions = pd.read_csv(os.path.join('data_subset/', 'paper_instance_occurrence_matrix.csv'))
df_rules = pd.read_csv(os.path.join('data_subset/', 'rules_cross_type.csv'))

with open(os.path.join('data_subset/', 'instance_types_dicts.json')) as file:
    inst_data = json.load(file)

onto = get_ontology('http://tib.eu/slr')

with onto:

    # Classes
    for ind, row in df_cl.iterrows():
        cl = types.new_class(row['URI'], (Thing,))
        cl.label = row['Label']
        re = types.new_class(f'has{row["Label"].title().replace(" ", "")}', (ObjectProperty,))
        re.label = f'has {row["Label"]}'

    # Instances
    for key, value in inst_data.items():
        cl = onto.search_one(label = key)
        if cl:
            for item in value:
                inst = cl()
                inst.label = item

    # Statements
    Contribution = types.new_class('Contribution', (Thing,))
    mentions = types.new_class('mentions', (ObjectProperty,))
    mentions.label = 'mentions'
    for ind, row in df_contributions.iterrows():
        contrib_inst = Contribution()
        contrib_inst.label = row[0]
        for col in df_contributions.columns:
            if row[col]:
                inst = onto.search_one(label = col)
                if inst:
                    contrib_inst.mentions.append(inst)

    # Rules
    for ind, row in df_rules.iterrows():
        subj_inst = onto.search_one(label = row['antecedents'])
        obj_inst = onto.search_one(label = row['consequents'])
        if subj_inst and obj_inst:
            obj_cl = obj_inst.is_a[0]
            rel_label = f'has {str(obj_cl.label[0])}'
            rel = onto.search_one(label = rel_label)
            if rel:
                rel[subj_inst].append(obj_inst)        

onto.save('onto.owl')
onto.destroy()
        
    
