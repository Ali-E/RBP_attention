import sys
# !conda install --yes --prefix {sys.prefix} urllib3
import timeit
import numpy as np
import requests as req
import json
import os
import pandas as pd


first_line = True
stubs = []
accession_list = []
target_list = []
rep_num_list = []
assembly_list = []
cell_name_list = []
strand_list = []
filename = sys.argv[1]
# with open(filename, encoding="utf-8") as f: 
with open(filename) as f: 
    for l in f: 
        print(l)
        if first_line: 
            first_line = False
            continue
        l = l.strip() 
        fn = os.path.basename(l)
        stub = fn.split(".")[0]
        stubs.append( stub )
        url = 'https://www.encodeproject.org/files/'+stub+'/?format=json'
        # print(url)
        resp = req.get(url)
        meta = json.loads(resp.text)
        print(meta.keys())
        accession = meta["accession"]# ['rbns_protein_concentration']
        print(accession)
        accession_list.append(accession)
        target = meta["target"]["label"]# ['rbns_protein_concentration']
        print(target)
        target_list.append(target)
        rep_num = meta["biological_replicates"]
        print(rep_num)
        rep_num_list.append(str(rep_num)[1:-1])
        assembly = meta["assembly"]
        print(assembly)
        assembly_list.append(assembly)
        cell_name = meta['biosample_ontology']['term_name']
        print(cell_name)
        cell_name_list.append(cell_name)
        strand_name = meta['output_type'].split()[0]
        print(strand_name)
        strand_list.append(strand_name)



dict_info = {'stub': stubs , 'accession': accession_list, 'target': target_list, 'rep_num': rep_num_list, 'cell_name': cell_name_list, 'assembly': assembly_list, 'strand': strand_list}

df = pd.DataFrame(dict_info) 
df.to_csv('bigwig_files_metadata_sample.csv', index=False)
