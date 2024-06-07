from owlready2 import *
import pandas as pd
import types


df_cl = pd.read_csv('classes.csv')
df_re = pd.read_csv('relations.csv')
df_re = df_re.set_index('Domain\Range')
df = pd.read_csv('data.csv')

onto = get_ontology('http://tib.eu/slr')

with onto:

    # Classes
    for ind, row in df_cl.iterrows():
        cl = types.new_class(row['URI'], (Thing,))
        cl.label = row['Label']

    # Relations
    for ind, row in df_re.iterrows():
        for col in df_re.columns:
            if ind == col:
                continue
            if pd.isna(row[col]):
                continue
            for re in row[col].split(','):
                re = re.strip()
                re_cl = types.new_class(re, (ObjectProperty,))
                re_cl.label = re
                domain_cl = onto.search_one(label = ind)
                range_cl = onto.search_one(label = col)
                re_cl.domain = domain_cl
                re_cl.range = range_cl

                for data_ind, data_row in df.iterrows():
                    sub_label = data_row[ind]
                    if pd.isna(sub_label):
                        #sub_label = f'{data_ind}_{ind}'
                        continue
                    obj_label = data_row[col]
                    if pd.isna(obj_label):
                        #obj_label = f'{data_ind}_{col}'
                        continue

                    sub = onto.search_one(label = sub_label)
                    if not sub:
                        sub = domain_cl()
                    sub.label = sub_label

                    obj = onto.search_one(label = obj_label)
                    if not obj:
                        obj = range_cl()
                    obj.label = obj_label
                    re_cl[sub].append(obj)
                    

onto.save('onto.owl')
onto.destroy()
        
    
