"""
Algoritmo para calculo de carga termica de refrigeração
Iniciado: 21.03.2018 - 19:12
Autor: peter.moresco
Algoritmo integrante do Projeto CC-TRAC - Calculo de Carga Térmica de Refrigeração
Auxiliado por Computador para a aula de projeto integrador III
Lembretes: 
- Descobrir como usar a equação h
- Incluir as unidades na hora de perguntar pelo input
"""
import pandas as pd

#Entrada
cidade = #criar repositorio
material_estoque =
altura_camara =  #verificar se não precisa dizer tamanhos da parede
l_parede_norte = 
l_parede_oeste =
l_parede_sul = 
l_parede_leste =  
isolamento = 
piso = 
contrapiso = 
t_solo =  #verificar se não é tabelado
parede_sol = 
cor_parede_ext = #importar de arquivo
#1 - Carga de transmissão através das superfícies
#Diferencial de temperatura
#te - temperatura externa da cidade com dia de verão em 0.4% temp de bulbo seco
#ti - temperatura interna
#AS - acréscimo devido ao sol
AT = (te - ti) + AS
#O h pode ser calculado, só deve-se saber como e o que considerar
#u - velocidade do vento
h = 8.7 +3.8 * u
#Se o isolamento não for poliuretano, deve-se corrigir pela equação, com x 
#espessura corrigida e xT a espessura corrigida, k a condutividade
x = xT * (k / 0.025)
#Esta lista/array precisa conter o coeficiente k e a epessura L dos materiais
#de forma L / k ; Os materiais devem ser oriundos de um dicionário
mat_forro = []
#Coeficiente global de transferência
#hi - coef transf convecção interno; he - coef transf convecção externo
U = 1 / ((1 / hi) + sum(mat_forro) + (1 / he)) 
#Calor sensível através de paredes e pisos em regime estacionário
# U - coeficiente de transf global; A - área; AT - diferença de temperatura do
#ar externo e espaço refrigerado
QTR = U * A * AT
#2 - Carga calorífica do produto contido na câmara
#3 - Carga de infiltração do ar na câmara
#4 - Carga interna provenientes de pessoas, eletrônicos e motores
#5 - Carga devida ao equipamento de refrigeração