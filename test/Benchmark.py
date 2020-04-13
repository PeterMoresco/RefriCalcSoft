import Objetos_Simulacao as obs

#Variáveis
simul1 = obs.Simul('Benchmark')
simul1.cidade = 'Porto Alegre, RS'
simul1.produto = 'Bacon, congelado'
simul1.camara_larg_sul = 20
simul1.camara_comp_leste = 20
simul1.camara_altura = 8.5
simul1.vel_vento_externo = 6
simul1.vel_vento_interno = 0.6
simul1.isolamento = 'Poliisocianureto'
simul1.piso_material = ['Concreto', 'Concreto']
simul1.piso_espessura = [0.06, 0.2]
simul1.piso_temperatura = 15
simul1.cor_parede = 'Media'
simul1.vol_util = 0.7
simul1.temp_prod_incial = 20
simul1.tempo_analise = 4
simul1.h_porta = 2
simul1.l_porta = 0.9

#Cálculos
# simul1.Exportar()
print(simul1.Qest())