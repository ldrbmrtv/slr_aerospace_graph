from owlready2 import *
import pandas as pd
import types


df_cl = pd.read_csv('classes.csv')
#df_re = pd.read_csv('relations.csv')
#df_re = df_re.set_index('Domain\Range')
df = pd.read_csv('data.csv')

onto = get_ontology('http://tib.eu/slr')

with onto:

    # Classes
    for ind, row in df_cl.iterrows():
        cl = types.new_class(row['URI'], (Thing,))
        cl.label = row['Label']
        re_label = f'has_{row["Label"].replace(" ", "_")}'
        cl = types.new_class(re_label, (ObjectProperty,))
        cl.label = re_label

    research = types.new_class('Research', (Thing,))
    has_source = types.new_class('has_source', (DataProperty,))
    # Relations
    #for ind, row in df_re.iterrows():
    #    for col in df_re.columns:
    #        if ind == col:
    #            continue
    #        if pd.isna(row[col]):
    #            continue
    #        for re in row[col].split(','):
    #            re = re.strip()
    #            re_cl = types.new_class(re, (ObjectProperty,))
    #            re_cl.label = re
    #            domain_cl = onto.search_one(label = ind)
    #            range_cl = onto.search_one(label = col)
    #            re_cl.domain = domain_cl
    #            re_cl.range = range_cl
    #
    #            for data_ind, data_row in df.iterrows():
    #                sub_label = data_row[ind]
    #                if pd.isna(sub_label):
    #                    #sub_label = f'{data_ind}_{ind}'
    #                    continue
    #                obj_label = data_row[col]
    #                if pd.isna(obj_label):
    #                    #obj_label = f'{data_ind}_{col}'
    #                    continue

    #                sub = onto.search_one(label = sub_label)
    #                if not sub:
    #                    sub = domain_cl()
    #                sub.label = sub_label

    #                obj = onto.search_one(label = obj_label)
    #                if not obj:
    #                    obj = range_cl()
    #                obj.label = obj_label
    #                re_cl[sub].append(obj)
    for ind, row in df.iterrows():
        res_inst = research()
        for col in df.columns:
            if pd.isna(row[col]):
                continue
            cl = onto.search_one(label = col)
            if not cl:
                continue
            inst = cl()
            inst.label = row[col]
            re_cl = onto.search_one(label = f'has_{col.replace(" ", "_")}')
            re_cl[res_inst].append(inst)
        has_source[res_inst].append(row['source'])


onto.save('onto.owl')
onto.destroy()
        
    
