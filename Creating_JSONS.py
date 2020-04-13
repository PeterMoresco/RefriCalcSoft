import json
import pandas as pd 

alimentos_dict = {}
cidades_dict = {}
calor_respiracao = {}
dissi = [('Alimentos', 'Produto'), ('Cidades', 'Cidade'),('Calor_resp','Produto')]
types = []
for id in zip([alimentos_dict, cidades_dict, calor_respiracao],dissi):
    planilha = pd.read_excel('Tabelas_Dados_Termicos.xls', sheet_name=id[1][0])
    for item in range(len(planilha.index)):
        produto = planilha.loc[item]
        id[0][produto[id[1][1]]] = {}
        for col in range(1,len(planilha.columns)):
            colum = planilha.columns
            if isinstance(produto[colum[col]], int) or isinstance(produto[colum[col]], float) or isinstance(produto[colum[col]], str):
                id[0][produto[id[1][1]]][colum[col]] = produto[colum[col]]
            else:
                id[0][produto[id[1][1]]][colum[col]] = float(produto[colum[col]])

    with open((id[1][0]+'.json'), 'w') as output:
        json.dump(id[0], output) 