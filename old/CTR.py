# -*- coding: utf-8 -*-
"""

"""

#Calculo de carga térmica de refrigeração

####### 1 - Carga de transmissão

temp_ext = 33.1 #C(Porto Alegre)

prod_te = -20 #C(Chuleta)

prod_ur = 0.9 #%(Chuleta)

dim_larg = 20 #m

dim_comp = 20 #m

dim_alt = 8.5 #m

v_vento_ext = 6 #m/s

v_vento_int = 0.6 #m/s

isolamento = 'Poliisocianureto' #Chave para dicionário?

m_piso = 'concreto' #Chave para dicionário?

e_piso = 6 #cm

m_isolantes = ['Poliuretano em placa', 'Poliisocianureto', 'Poliestireno extrudado', 'Poliestireno expandido', 'Cortica', 'Fibra de vidro', 'Concreto']

cond_termica_k = [0.025, 0.027, 0.035, 0.037, 0.043, 0.044, 2]

coef_k_materiais = dict(zip(m_isolantes, cond_termica_k))

print(cond_termica_k[m_isolantes.index(isolamento)])

print(coef_k_materiais[isolamento])