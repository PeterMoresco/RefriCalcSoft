import json
import os 

for dicionario in ['Alimentos.json','Calor_resp.json','coef_k_materiais.json']:
    nome_novo = os.path.splitext(dicionario)[0]
    nome_novo = nome_novo+'_Sorted.json'
    with open(dicionario,'r') as f:
         data = json.load(f)

    data_sorted = {k : data[k] for k in sorted(data.keys())}

    with open(nome_novo, 'w') as f:
        json.dump(data_sorted, f)