import pandas as pd
import os
import json
from owlready2 import *
import types


df_cl = pd.read_csv('classes.csv')
df_contributions = pd.read_csv(os.path.join('data_subset/', 'paper_instance_occurrence_matrix_reviewed.csv'))
df_rules = pd.read_csv(os.path.join('data_subset/', 'rules_cross_type_reviewed.csv'))

with open(os.path.join('data_subset/', 'obsidian_folder.json')) as file:
    inst_data = json.load(file)

#onto_path.append('slr.owl')
onto = get_ontology('slr.owl').load()

with onto:

    # Custom predicates
    #Contribution = types.new_class('Contribution', (Thing,))
    #mentions = types.new_class('mentions', (ObjectProperty,))
    #mentions.label = 'mentions'
    #aliase = types.new_class('aliase', (AnnotationProperty,))
    #aliase.label = 'aliase'
    #wikidata_uri = types.new_class('wikidata_uri', (AnnotationProperty,))
    #wikidata_uri.label = 'wikidata_uri'
    #source = types.new_class('source', (AnnotationProperty,))
    #source.label = 'source'

    # Classes
    #for ind, row in df_cl.iterrows():
    #    cl = types.new_class(row['URI'], (Thing,))
    #    cl.label = row['Label']
    #    re = types.new_class(f'has{row["Label"].title().replace(" ", "")}', (ObjectProperty,))
    #    re.label = f'has {row["Label"]}'
    Contribution = onto['Contribution']

    # Instances
    #for class_key, class_value in inst_data.items():
    #    cl = onto.search_one(label = class_key)
    #    if cl:
    #        for item_key, item_value in class_value.items():
    #            inst = cl()
    #            inst.label = item_value['label']
    #            inst.aliase = item_value['aliases']
    #            inst.wikidata_uri = item_value['wikidata_uri']
    #            inst.source = item_value['source']

    # Statements
    for ind, row in df_contributions.iterrows():
        contrib_inst = onto.search_one(label = row[0])
        if not contrib_inst:
            contrib_inst = Contribution()
            contrib_inst.label = row[0]
            print(f'new contribution: {row[0]}')
        for col in df_contributions.columns:
            if row[col]:
                inst = onto[col]
                if inst:
                    if inst not in contrib_inst.mentions:
                        print(f'new mention: {inst.label[0]}')
                        contrib_inst.mentions.append(inst)

    # Rules
    for ind, row in df_rules.iterrows():
        subj_inst = onto[row['antecedents']]
        if not subj_inst:
            subj_inst = IRIS[f'http://webprotege.stanford.edu/{row["antecedents"]}']
        obj_inst = onto[row['consequents']]
        if not obj_inst:
            obj_inst = IRIS[f'http://webprotege.stanford.edu/{row["consequents"]}']
        if subj_inst:
            if obj_inst:
                obj_cl = obj_inst.is_a[0]
                rel_label = f'has {str(obj_cl.label[0])}'
                rel = onto.search_one(label = rel_label)
                if rel:
                    if obj_inst not in rel[subj_inst]:
                        print(f'new rule: ({subj_inst.label[0]}, {rel.label[0]}, {obj_inst.label[0]})')
                        rel[subj_inst].append(obj_inst)
                else:
                    print(f'rel not found: {rel_label})')
            else:
                print(f'object {row["consequents"]} not found')
        else:
            print(f'subject {row["antecedents"]} not found')
            

onto.save('slr2_reviewed.owl')
onto.destroy()
        
    
