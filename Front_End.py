import tkinter as tk

fontes = {
    'grande':('Consolas', 13),
    'pequena':('Consolas', 10)
}

class Main_App(tk.Tk):
    """Classe container para criacao das outras janelas"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'RefriCalcSoft')
        #TODO repensar esse nome horrível
        tk.Tk.geometry(self, '1000x700') #larguraXaltura

        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        for F in (Janela_inicial, Janela_Criacao):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.mostrar_janela(Janela_Criacao)

    def mostrar_janela(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Janela_inicial(tk.Frame):
    """Janela inicial que irá exibir as simulações já criadas daquele 
    repositório"""
    def __init__(self, parent, controller):
        #o parametro controller passa o próprio objeto para posteriormente
        #atribuir as funções a ele
        tk.Frame.__init__(self, parent)


class Janela_Criacao(tk.Frame):
    """Janela aonde são criadas as simulações"""
    linhas = {
        'cidade':('Cidade', 'Lista', '', ''),
        'produto':('Produto', 'Lista', '', ''),
        'camara_larg_sul':('Largura da camara(lado Sul)','Input', 'm',0),
        'camara_comp_leste':('Comprimento da camara(lado Leste)','Input','m',0),
        'camara_altura':('Altura da camara','Input','m',0),
        'vel_vento_interno':('Velocidade do vento interno','Input','m/s',0),
        'isolamento':('Isolamento das paredes','Lista','',''),
        'piso_material':('Material do piso','Lista','',''),
        'piso_espessura':('Espessura do piso','Input','m',0),
        'piso_temperatura':('Temperatura do piso','Input','ºC',0),
        'cor_parede':('Cor das paredes','Lista','',''),
        'vol_util':('Volume útil da camara','Input','%',0),
        'temp_prod_incial':('Temperatura inicial do produto','Input','ºC',0),
        'tempo_analise':('Período de tempo em análise','Input','horas',0),
        'pot_iluminacao':('Potência da iluminação','Input','W/m2',0),
        'pot_miscelanea':('Potência adicional de origem variada','Input','W',0),
        'n_pessoas':('Número de pessoas transitando na camara','Input','',0),
        'h_porta':('Altura da passagem/porta','Input','m',0),
        'l_porta':('Largura da passagem/porta','Input','m',0),
        'n_passagens_porta':('Número de passagens pela porta','Input','',0),
        'tempo_porta_aberta':('Tempo de porta aberta','Input','segundos',0),
        'fator_Df':('Fator decimal de fluxo de porta','Input','',0),
        'efetividade_protecao_porta':('Efetividade do dispositivo de proteção da porta','Input','',0),
        'cargas_variadas':('Cargas variadas','Input','W',0),
        'coef_seguranca':('Coeficiente de segurança','Input','',1)
    }
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        for i in self.linhas.values():
            a = tk.ttk.Label(self, text=i[0])
            a.pack(side=tk.TOP)
            b = tk.ttk.Entry(self)
            b.pack(side=tk.LEFT)
            c = tk.ttk.Label()
        

main = Main_App()

main.mainloop()