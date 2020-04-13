import pandas as pd
import os

# Calculo de carga térmica de refrigeração

####### Varíaveis de entrada #######

cidade = 'Porto Alegre, RS'

produto = 'Bacon, congelado'

temp_inicial = 20

tempo_analise = 4 #horas

dim_larg_sul = 20  # m

dim_comp_leste = 20  # m

dim_alt = 8.5  # m

cor_parede = 'Media'

v_vento_ext = 6  # m/s

v_vento_int = 0.6  # m/s

isolamento = 'Poliisocianureto'

m_piso = ['Concreto', 'Concreto']

e_piso = [0.06, 0.20]  # cm

t_solo = 15  # C

# parede_ensol = ['N', 'O']

q_iluminacao = 10 #W/m2

n_pessoas = 16

h_porta = 2 #m

l_porta = 0.9 #m

P_porta, T_porta, T_porta_min = 30, 25, 750

# variáveis que saíram de listas no futuro
cpr = 3.49
cpc = 2.14
hc = 233
densidade_produto = 145 #kg/m3
tc = -2.2
pr = 1.39 #densidade do ar refrigerado
pi = 1.11 #densidade do ar de infiltração
entalpia_infiltracao = 94
entalpia_refrigerado = -19

### DICT/TABS ###
cur_dir = os.getcwd()
path = os.path.join(cur_dir, 'Tabelas_Dados_Termicos.xls')
cidades = pd.read_excel(path, 'Cidades')
cidades.set_index('Cidade', inplace = True)

alimentos = pd.read_excel(path, 'Alimentos')
alimentos.set_index('Produto', inplace = True)

t_prod_estoc = alimentos.loc[produto]['T Estoc']
temp_ext = cidades.loc[cidade]['tbs']
prod_ur = alimentos.loc[produto]['UR']

m_isolantes = ['Poliuretano em placa', 'Poliisocianureto', 'Poliestireno extrudado', 'Poliestireno expandido',
               'Cortica', 'Fibra de vidro', 'Concreto']

cond_termica_k = [0.025, 0.027, 0.035, 0.037, 0.043, 0.044, 2]

coef_k_materiais = dict(zip(m_isolantes, cond_termica_k))

temp_estoc = [-40, -26, -9, 4]

esp_isol = [0.125, 0.100, 0.075, 0.050]

paredes_cor = ['Escura', 'Media', 'Clara']

paredes_valores = [[5, 3, 5, 11], [4, 3, 4, 9], [3, 2, 3, 5]]

coef_paredes = dict(zip(paredes_cor, paredes_valores))

########### FUNC ##########

def esp_min(t):
    """ Define a espessura mínima para o isolamento em mm"""
    if t < temp_estoc[0]:
        return esp_isol[0]
    elif t > temp_estoc[-1]:
        return esp_isol[-1]
    else:
        for i in range(1, len(temp_estoc)):
            if t < temp_estoc[i]:
                return esp_isol[i - 1]
#(m_piso, e_piso,
# coef_k_materiais[isolamento], esp_isolamento, coef_calor_conv_int)
def coef_transf_piso(d_mat_piso, d_e_piso, d_mat_isol, d_e_isol, d_hi):
    """Calcula o coeficiente de transferencia do piso"""
    U_piso = 0
    for i, j in zip(d_e_piso, d_mat_piso):
        U_piso += i / coef_k_materiais[j]
    U_piso += d_e_isol / d_mat_isol
    U_piso += 1 / d_hi
    return U_piso

##### CALC #####
### 1 - Carga de transmissão

coef_calor_conv_ext = 8.7 + 3.8 * v_vento_ext #W/m2k

coef_calor_conv_int = 8.7 + 3.8 * v_vento_int #W/m2k

esp_isolamento = esp_min(t_prod_estoc)

U_paredes = 1 / coef_calor_conv_int
U_paredes += esp_isolamento / coef_k_materiais[isolamento]
U_paredes += 1 / coef_calor_conv_ext

delta_temperatura = temp_ext - t_prod_estoc

Q_Sul = U_paredes * dim_larg_sul * dim_alt * delta_temperatura
Q_Norte = U_paredes * dim_larg_sul * dim_alt * (delta_temperatura + coef_paredes[cor_parede][1])
Q_Oeste = U_paredes * dim_comp_leste * dim_alt * (delta_temperatura + coef_paredes[cor_parede][2])
#Verifica se a parede leste se repete
Q_Forro = U_paredes * dim_comp_leste * dim_larg_sul * (delta_temperatura + coef_paredes[cor_parede][3])
U_Piso = coef_transf_piso(m_piso, e_piso, coef_k_materiais[isolamento], esp_isolamento, coef_calor_conv_int)
Q_Piso = U_Piso * dim_comp_leste * dim_larg_sul * (delta_temperatura)

### 2 - Carga do produto

# Considerando desconto de 30% no volume para circulação de máquinas e pessoal
volume_camara = dim_larg_sul * dim_comp_leste * dim_alt #m3
volume_util_cam = 0.7 * volume_camara

massa_produto = densidade_produto * volume_util_cam #kg

Q2 = massa_produto * cpr * (temp_inicial - tc) #kJ
Q3 = massa_produto * hc #kJ
Q4 = massa_produto * cpc * (tc - t_prod_estoc)
Q_Total = (Q2 + Q3 + Q4) / (3600 * tempo_analise)
### 3 - Carga interna

Q_Iluminacao = dim_comp_leste * dim_larg_sul * q_iluminacao

Q_Pessoas = n_pessoas * (272 - 6 * t_prod_estoc)
### 4 - Carga de infiltração

Fm = (2 / (1+ (pr / pi)**(1 / 3))) ** 1.5
u_est = 0.442 * Fm * ((pr - pi) * 9.81 * h_porta / pr) ** 0.5
Q_Sen_Lat = h_porta * l_porta * 0.5 * (entalpia_infiltracao - entalpia_refrigerado) * pr * u_est
Dt = (P_porta * T_porta + 60 * T_porta_min) / (3600 * tempo_analise)
Q_Infiltracao = Q_Sen_Lat * Dt * 1000

### Resultado

Carga_Termica_Refrigeracao = Q_Sul + Q_Norte + Q_Oeste + Q_Piso + Q_Forro
Carga_Termica_Refrigeracao += Q_Total
Carga_Termica_Refrigeracao += Q_Iluminacao + Q_Pessoas
Carga_Termica_Refrigeracao += Q_Infiltracao

################### DEBUG ##############################

# print(coef_k_materiais[isolamento], 'W/mk')

# print('coef transmissao externo {0:.2f} W/m2k'.format(coef_calor_conv_ext))

# print('coef transmissao interno {0:.2f} W/m2k'.format(coef_calor_conv_int))

# print('A espessura mínima para a temp de -20C é', esp_min(t_prod_estoc), 'm')

# print('Coeficiente global de transferência de calor U para paredes, pisos e forros, {0:.2f} W/m2k'.format(U_paredes))

# print('Parede sul {0:.2f} W'.format(Q_Sul))

# print('Parede norte {0:.2f} W'.format(Q_Norte))

# print('Parede oeste/leste {0:.2f} W'.format(Q_Oeste))

# print('Forro {0:.2f}W'.format(Q_Forro))

# print('Piso {0:.2f}W'.format(Q_Piso))

# print('Volume total da camâra {0:.2f}m3'.format(volume_camara))
#
# print('Massa de produto na camara {0:.2f}kg'.format(massa_produto))

# print('Calor removido para resfriar o produto até o ponto inicial de congelamento é {0:.2f}kJ'.format(Q2))

# print('Calor removido para congelar o produto é {0:.2f}kJ'.format(Q3))

# print('Calor removido para resfriar o produto até o temperatura de estocagem é {0:.2f}kJ'.format(Q4))

# print('Potência total para resfriar o produto é {0:.2f}kJ'.format(Q_Total))

#print('A potência dispersada pela iluminação é {0:.2f}W'.format(Q_Iluminacao))

#print('A potência dispersada por pessoas é {0:.2f}W'.format(Q_Pessoas))

print('O calor sensível latente é de {0:.2f}kW'.format(Q_Sen_Lat))

#print('O ganho de calor proporcionado pela porta é de {0:.2f}W'.format(Q_infiltracao))

# print('A carga térmica de refrigeração para as condições fornecidas é de {0:.2f}W'.format(Carga_Termica_Refrigeracao))
# print(cidades.loc[cidade]['tbs'])
