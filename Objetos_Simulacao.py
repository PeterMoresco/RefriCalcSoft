import os
import json


class Simul:
    def __init__(self):
        self.cidade = None
        self.produto = None
        self.densidade = None
        self.camara_larg_sul = None
        self.camara_comp_leste = None
        self.camara_altura = None
        self.vel_vento_externo = None
        self.vel_vento_interno = None
        self.isolamento = None
        self.piso_material = []
        self.piso_espessura = []
        self.piso_temperatura = None
        self.cor_parede = None
        self.vol_util = None
        self.temp_prod_incial = None
        self.tempo_analise = None
        self.pot_iluminacao = 0
        self.pot_miscelanea = 0
        self.n_pessoas = 0
        self.h_porta = None
        self.l_porta = None
        self.n_passagens_porta = None
        self.tempo_porta_aberta = None
        self.fator_Df = None
        self.efetividade_protecao_porta = None
        self.cargas_variadas = 0
        self.coef_seguranca = None

    cur_dir = os.getcwd()
    caminho = os.path.join(cur_dir, 'Tabelas_Dados_Termicos.xls')

    # Dados intermediarios
    hi = 0
    hr = 0
    pr = 0 
    pi = 0

    # coef_paredes = {'Escura': [5, 3, 5, 11],
    #                 'Media': [4, 3, 4, 9],
    #                 'Clara': [3, 2, 3, 5]}
    with open('coef_paredes.json', 'r') as f:
        coef_paredes = json.load(f)

    with open('coef_k_materiais.json','r') as f:
        coef_k_materiais = json.load(f)

    def dados_produto(self, coluna):
        # alimentos = pd.read_excel(self.caminho, 'Alimentos')
        # alimentos.set_index('Produto', inplace = True)
        # return alimentos.loc[self.produto][coluna]
        with open('alimentos.json','r') as f:
            alimentos = json.load(f)
        return alimentos[self.produto][coluna]

    def calor_resp(self):
        # alimentos = pd.read_excel(self.caminho, 'Calor_resp')
        # alimentos.set_index('Produto', inplace = True)
        # return alimentos.loc[self.produto]['Cr, mW/kg']
        with open('Calor_resp.json','r') as f:
            calor_r = json.load(f)
        return calor_r[self.produto]['Cr, mW/kg']

    def temp_externa(self, coluna):
        """Retorna a temperatura externa de bulbo seco para a
        cidade desejada em graus Celsius"""
        # cidades = pd.read_excel(self.caminho, 'Cidades')
        # cidades.set_index('Cidade', inplace = True)
        # return cidades.loc[self.cidade][coluna]
        with open('Cidades.json','r') as f:
            _cidades = json.load(f)
        return _cidades[self.cidade][coluna]

    def coef_hi(self):
        """Coeficiente de transferência de calor por convecção
        interno W/m2k"""
        return 8.7 + 3.8 * self.vel_vento_interno

    def coef_he(self):
        """Coeficiente de transferência de calor por convecção
        externo W/m2k"""
        return 8.7 + 3.8 * self.vel_vento_externo

    def esp_min(self):
        """ Define a espessura mínima para o isolamento em m"""
        t = self.dados_produto('T Estoc')
        temp_estoc = [-40, -26, -9, 4]
        esp_isol = [0.125, 0.100, 0.075, 0.050]
        if t < temp_estoc[0]:
            return esp_isol[0]
        elif t > temp_estoc[-1]:
            return esp_isol[-1]
        else:
            for i in range(1, len(temp_estoc)):
                if t < temp_estoc[i]:
                    return esp_isol[i - 1]

    def U_paredes(self):
        """Calcula o coeficiente de transferência global de calor
        para as paredes W/m2k"""
        u_paredes = 1 / self.coef_hi()
        u_paredes += self.esp_min() / self.coef_k_materiais[self.isolamento]
        u_paredes += 1 / self.coef_he()
        return u_paredes

    def U_piso(self):
        """Calcula o coeficiente de transferência global de calor
        para o piso W/m2k"""
        U_piso = 0
        for i, j in zip(self.piso_espessura, self.piso_material):
            U_piso += i/self.coef_k_materiais[j]
        U_piso += self.esp_min() / self.coef_k_materiais[self.isolamento]
        U_piso += 1 / self.coef_hi()
        return U_piso

    def delta_temp(self):
        """Calcula a diferença de temperatura entre a de estocagem
        e a externa"""
        t = self.temp_externa('tbs') - self.dados_produto('T Estoc')
        return t

    def Q_sul(self):
        """Calcula o ganho de calor sensível para a parede do lado
        sul"""
        Q_sul = self.U_paredes() * self.camara_larg_sul
        Q_sul *= self.camara_altura * self.delta_temp()
        return Q_sul

    def Q_norte(self):
        """Calcula o ganho de calor sensível para a parede do lado
        norte"""
        Q_norte = self.U_paredes() * self.camara_larg_sul
        Q_norte *= self.camara_altura
        Q_norte *= (self.delta_temp() + self.coef_paredes[
            self.cor_parede][1])
        return Q_norte

    def Q_oeste(self):
        """Calcula o ganho de calor sensível para a parede do lado
        oeste"""
        Q_oeste = self.U_paredes() * self.camara_comp_leste
        Q_oeste *= self.camara_altura
        Q_oeste *= (self.delta_temp() + self.coef_paredes[
            self.cor_parede][2])
        return Q_oeste

    def Q_forro(self):
        """Calcula o ganho de calor sesível para o forro"""
        Q_forro = self.U_paredes() * self.camara_comp_leste
        Q_forro *= self.camara_larg_sul
        Q_forro *= (self.delta_temp() + self.coef_paredes[
            self.cor_parede][3])
        return Q_forro

    def Q_piso(self):
        """Calcula o ganho de calor sensível para o piso"""
        #todo incluir unidades para os cálculos Q
        Q_piso = self.U_piso() * self.camara_comp_leste
        Q_piso *= self.camara_larg_sul
        Q_piso *= (self.piso_temperatura - self.dados_produto('T Estoc'))
        return Q_piso
    
    #2 - Carga de produto
    def massa_produto(self):
        """Calcula a massa de produto com base no tamanho
        da camara e da densidade do produto kg"""
        vol_camara = self.camara_larg_sul * self.camara_comp_leste
        vol_camara *= self.camara_altura * self.vol_util/100
        return vol_camara * self.densidade
        #TODO ajustar tabela de dados dos alimentos incluindo a densidade

    def Q1(self):
        """Calor kJ removido para resfriar o produto desde a temperatura
        inicial até outra acima do congelamento, para produtos resfriados"""
        Q1 = self.massa_produto() * self.dados_produto('Cal_esp_resf')
        Q1 *= (self.temp_prod_incial - self.dados_produto('T Estoc'))
        return Q1

    def Q2(self):
        """Calor kJ removido para resfriar o produto desde a temperatura
        inicial até a temperatura incial de congelamento do produto"""
        Q2 = self.massa_produto() * self.dados_produto('Cal_esp_resf')
        Q2 *= (self.temp_prod_incial - self.dados_produto('Temp Cong'))
        return Q2
        #TODO verificar se a temperatura inicial do produto não é menor que a de congelamento

    def Q3(self):
        """Calor kJ removido para congelar o produto"""
        Q3 = self.massa_produto() * self.dados_produto('Calor_congela')
        return Q3

    def Q4(self):
        """Calor kJ removido para resfriar o produto desde a temperatura
        inicial de congelamento do produto até a temperatura final 
        de estocagem do produto congelado"""
        Q4 = self.massa_produto() * self.dados_produto('Cal_esp_cong')
        Q4 *= (self.dados_produto('Temp Cong') - self.dados_produto('T Estoc'))
        return Q4

    def Q5(self):
        """Calor kJ removido para resfriar pallets, caixas, containers e
        outros materiais de contenção de alimentos"""
        return 0
        #TODO implementar essa função Q5

    def Q6(self):
        """Potência kW térmica para resfriar o produto desde a temperatura
        incial até a temperatura final"""
        if self.dados_produto('T Estoc') < self.dados_produto('Temp Cong'):
            Q6 = self.Q2() + self.Q3()
            Q6 += self.Q4() + self.Q5()
            Q6 /= (3600 * self.tempo_analise)
            return Q6
        else:
            Q6 = self.Q1() + self.Q5()
            Q6 /= (3600 * self.tempo_analise)
            return Q6
    #TODO preencher as unidades dos itens

    def Q7(self):
        """Potência térmica na respiração de frutas e vegetais"""
        try:
            Q7 = self.massa_produto() * self.calor_resp()/1000
            return Q7
        except:
            return 0

    def Carga_Produto(self):
        """Potência total de refrigeração devida ao produto"""
        Qpr = 1000*self.Q6() + self.Q7()
        return Qpr
        
    #3 - Carga interna
    def Iluminacao(self):
       """Calcula W a carga térmica devida a iluminação""" 
       q_iluminacao = self.camara_comp_leste * self.camara_larg_sul
       q_iluminacao *= self.pot_iluminacao
       return q_iluminacao

    def Q_pessoas(self):
        """Estimativa da perda de calor causada pelas pessoa W"""
        Qpes = self.n_pessoas * (272 - 6 * self.dados_produto('T Estoc'))
        return Qpes

    #4 - Carga de infiltração
    def Qest(self):
        """Carga de refrigeração sensível e latente para fluxo de ar
        estabelecido kW"""
        import psychrochart.equations as pce
        area_p = self.h_porta * self.l_porta
        tbs = self.temp_externa('tbs')
        tbu = self.temp_externa('tbu')
        h_externo = pce.humidity_ratio_from_temps(tbs, tbu)
        w_externo = pce.water_vapor_pressure(h_externo)
        hi = pce.enthalpy_moist_air(tbs, w_externo)
        t_estoc = self.dados_produto('T Estoc')
        u_estoc = self.dados_produto('UR')
        t_bu_refri = pce.wet_bulb_temperature_empiric(t_estoc, u_estoc)
        h_refri = pce.humidity_ratio_from_temps(t_estoc, t_bu_refri)
        w_refri = pce.water_vapor_pressure(h_refri)
        hr = pce.enthalpy_moist_air(t_estoc, w_refri)
        pi = 1/pce.specific_volume(tbs, w_externo)
        pr = 1/pce.specific_volume(t_estoc, w_refri)
        Fm = (2/(1+(pr/pi)**(1/3)))**1.5
        Uest = 0.442 * Fm * ((pr - pi)*9.81*self.h_porta/pr)**0.5
        Qest = 0.5 * area_p * (hi - hr) * pr * Uest
        return Qest

    def Dt(self):
        """Fator temporal decimal de abertura de porta"""
        Dt = (self.n_passagens_porta * self.tempo_porta_aberta*(1+60))
        #TODO confirmar alteração com o professor
        Dt /= (3600 * self.tempo_analise)
        return Dt

    def Carga_Infiltracao(self):
        """O ganho de calor pelas portas devido as trocas de ar(infiltração) kW"""
        Qinf = self.Qest() * self.Dt() * self.fator_Df * (1-self.efetividade_protecao_porta)
        return Qinf
        #TODO verificar se a unidade desse item não sofre alteração

    #Carga térmica de refrigeração
    def Carga_Termica_Total(self):
        """Calcula a carga térmica de refrigeração total"""
        #1 - Carga de transmissão
        CT = 2*self.Q_sul() + self.Q_norte() + self.Q_oeste()
        CT += self.Q_forro() + self.Q_piso()
        #2 - Carga produto
        CT += self.Carga_Produto()
        #3 - Carga interna
        CT += self.Iluminacao() + self.Q_pessoas()
        #4 - Carga de infiltração
        CT += (self.Carga_Infiltracao()*1000)
        #5 - Cargas variadas
        CT += self.cargas_variadas
        #Coeficiente de segurança
        CT *= (1+(self.coef_seguranca/100))
        return CT

    #Funcionalidades        
    def Preencher(self, dicionario):
        """Preenche os valores dos atributos do objeto de acordo com o
        dicionário repassado"""
        try:
            valida = dicionario.get('simulacao_ctr', None)
            if valida != None:
                dados = valida['dados']
                for key in self.__dict__.keys():
                    setattr(self, key, dados[key])
            else:
                return False
        except:
            return
        # for key in dicionario.keys():
        #     if key in self.__dict__.keys():
        #         setattr(self, key, dicionario[key])

    def Exportar(self):
        """Exporta alguns resultados selecionados para um arquivo de 
            texto
        """
        resultados = {
            'Coef. transf. conv. interno':(self.coef_hi(), 'W/m2k'),
            'Coef. transf. conv. externo':(self.coef_he(), 'W/m2k'),
            'Espessura mín. isolamento':(self.esp_min(), 'm'),
            'Coef. transf. global paredes':(self.U_paredes(), 'W/m2k'),
            'Coef. transf. global piso':(self.U_piso(), 'W/m2k'),
            'Calor sensível parede Sul':(self.Q_sul(), 'W'),
            'Calor sensível parede Norte':(self.Q_norte(), 'W'),
            'Calor sensível parede Oeste':(self.Q_oeste(), 'W'),
            'Calor sensível parede Leste':(self.Q_sul(), 'W'),
            'Calor sensível forro':(self.Q_forro(), 'W'),
            'Calor sensível piso':(self.Q_piso(), 'W'),
            'Massa de produto':(self.massa_produto(), 'kg'),
            'Q1':(self.Q1(), 'kJ'),
            'Q2':(self.Q2(), 'kJ'),
            'Q3':(self.Q3(), 'kJ'),
            'Q4':(self.Q4(), 'kJ'),
            'Q6':(self.Q6(), 'kW'),
            'Q7':(self.Q7(), 'W'),
            'Carga do produto':(self.Carga_Produto(), 'W'),
            'Carga iluminação':(self.Iluminacao(), 'W'),
            'Carga de pessoas':(self.Q_pessoas(), 'W'),
            'Qest':(self.Qest(), 'kW'),
            'Fator de abertura de porta':(self.Dt(), ''),
            'Carga Infiltração':(self.Carga_Infiltracao(), 'kW'),
            'Carga térmica total':(self.Carga_Termica_Total(), 'W')
        }
        return resultados

if __name__ == '__main__':
    with open('Validacao_Caso_Repolho_1.json','r') as f:
        data = json.load(f)
    
    simulacao = Simul()
    simulacao.Preencher(data)
    resultados = simulacao.Exportar()
    print(resultados)
    data['simulacao_ctr']['resultados'] = resultados
    print(data)
    # with open('Teste_Validacao_Calculo.json','w') as f:
    #     json.dump(data, f)