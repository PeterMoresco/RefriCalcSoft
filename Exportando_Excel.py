import json
import os
import xlsxwriter
import GUI
# Importacao provisoria
linhas = GUI.Janela_Criacao.linhas

# Abre os resultados
with open('Validacao_Caso_Repolho.json','r') as f:
    data = json.load(f)
# Separa em dados e resultados
dados = data['simulacao_ctr']['dados']
resultados = data['simulacao_ctr']['resultados']
# Cria a planilha
workbook = xlsxwriter.Workbook('Teste_Exportacao_1.xlsx')
w_dados = workbook.add_worksheet(name='Dados')
w_resultados = workbook.add_worksheet(name='Resultados')
# Cria o formato dos cabecarios
formato = workbook.add_format({'bold':True})
# Inicia a contagem de celulas e colunas
d_r, r_r = 0, 0
# Cria os cabecarios
for plan in [w_dados, w_resultados]:
    plan.write(d_r, 0, 'Item', formato)
    plan.write(d_r, 1, 'Valor', formato)
    plan.write(d_r, 2, 'Unidade', formato)
d_r, r_r = 1, 1
# Itera através dos itens
for keys, values in linhas.items():
    w_dados.write(d_r, 0, values[0])
    if isinstance(dados[keys], list):
        lista = ', '.join([str(x) for x in dados[keys]])
        w_dados.write(d_r, 1, lista)
    else:
        w_dados.write(d_r, 1, dados[keys])
    w_dados.write(d_r, 2, values[2])
    d_r += 1
for keys, values in resultados.items():
    w_resultados.write(r_r, 0, keys)
    w_resultados.write(r_r, 1, values[0])
    w_resultados.write(r_r, 2, values[1])
    r_r += 1
# Ajusta a largura das colunas
w_dados.set_column(0, 0, 45)
w_resultados.set_column(0, 0, 30)
w_dados.set_column(1, 1, 13)
w_resultados.set_column(1, 1, 35)
w_dados.set_column(2, 2, 10)
w_resultados.set_column(2, 2, 8)
workbook.close()
