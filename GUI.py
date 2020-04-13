import tkinter as tk 
import tkinter.ttk as ttk 
import json
from tkinter import filedialog
import os
from tkinter import messagebox
import time
import Objetos_Simulacao as OBS
import xlsxwriter
from Ajuda import Janela_Ajuda
from Sobre import Sobre

fontes = {
    'G':('Arial', 13),
    'P':('Arial', 7),
    'M': ('Consolas', 10),
    'MM': ('Consolas', 11)
}

cidades = {}
with open('Cidades.json', 'r') as f:
    cidades = json.load(f)

paredes = {}
with open('coef_paredes.json', 'r') as f:
    paredes = json.load(f)

alimentos = {}
with open('Alimentos.json', 'r') as f:
    alimentos = json.load(f)

materiais = {}
with open('coef_k_materiais.json', 'r') as f:
    materiais = json.load(f)

def validacao_input(inp):
    if isinstance(inp, str):
        try:
            conv = float(inp.replace(',','.'))
            return conv
        except:
            return False
    elif isinstance(inp, int) or isinstance(inp, float):
        return inp
    else:
        return False

class Janela_Criacao(tk.Tk):
    var = {}
    linhas = {
        'cidade':('Cidade', 'Lista', '', '',cidades),
        'produto':('Produto', 'Lista', '', '', alimentos),
        'densidade':('Densidade','Input','kg/m3',0),
        'camara_larg_sul':('Largura da camara(lado Sul)','Input', 'm',0),
        'camara_comp_leste':('Comprimento da camara(lado Leste)','Input','m',0),
        'camara_altura':('Altura da camara','Input','m',0),
        'vel_vento_externo':('Velocidade do vento externo', 'Input', 'm/s', 0),
        'vel_vento_interno':('Velocidade do vento interno','Input','m/s',0),
        'isolamento':('Isolamento das paredes','Lista','','', materiais),
        'piso_material':('Configuração piso','Listbox','',''),
        'piso_espessura':('Espessura do piso','passar','m',0),
        'piso_temperatura':('Temperatura do piso','Input','ºC',0),
        'cor_parede':('Cor das paredes','Lista','','', paredes),
        'vol_util':('Volume útil da camara','Input','%',0),
        'temp_prod_incial':('Temperatura inicial do produto','Input','ºC',0),
        'tempo_analise':('Período de tempo em análise','Input',' horas',0),
        'pot_iluminacao':('Potência da iluminação','Input','W/m2',0),
        'pot_miscelanea':('Potência adicional de origem variada','Input','W',0),
        'n_pessoas':('Número de pessoas transitando na camara','Input','',0),
        'h_porta':('Altura da passagem/porta','Input','m',0),
        'l_porta':('Largura da passagem/porta','Input','m',0),
        'n_passagens_porta':('Número de passagens pela porta','Input','',0),
        'tempo_porta_aberta':('Tempo de porta aberta','Input',' segundos',0),
        'fator_Df':('Fator decimal de fluxo de porta','Input','',0),
        'efetividade_protecao_porta':('Efetividade do dispositivo de proteção da porta','Input','',0),
        'cargas_variadas':('Cargas variadas','Input','W',0),
        'coef_seguranca':('Coeficiente de segurança','Input','%',0)
    }
    valores = dict(zip(linhas.keys(),
                 [0 for i in range(len(linhas))]))

    def salvar(self):
        '''Salva os dados da simulação no arquivo'''
        # Validação dos dados
        dados = {}
        for key in self.linhas.keys():
            # Testa se o valor foi preenchido
            if self.linhas[key][1] == 'Input':
                valor = validacao_input(self.var[key].get())
                print(self.var[key].get())
                if isinstance(valor, bool):
                    messagebox.showwarning('Valor inválido','O valor do campo {} não pode ser convertido. Favor verificar'.format(self.linhas[key][0]))
                    break
                else:
                    dados[key] = valor
            elif self.linhas[key][1] == 'Listbox' or self.linhas[key][1] == 'passar':
                if len(self.var[key]) == 0:
                    messagebox.showwarning('Valor inválido','o valor do campo {} não pode ser convertido. Favor verficar'.format(self.linhas[key][0]))
                    break
                else:
                    dados[key] = self.var[key]
            elif self.linhas[key][1] == 'Lista':
                dados[key] = self.var[key].get()
        else:
            # Salva os dados num arquivo JSON
            simulacao_ctr = {'simulacao_ctr':{'dados': dados}}
            print(simulacao_ctr)

            file = filedialog.asksaveasfile(mode='w', defaultextension='.json')
            if file is not None:
                json.dump(simulacao_ctr, file)
                file.close()  
                self.destroy()      
    
    def adicionar_valor(self):
        def preencher_lista():
            if len(self.var['piso_material']) != 0:
                for i in range(len(self.var['piso_material'])):
                    string_lista = ' '.join([str(self.var['piso_material'][i]), str(self.var['piso_espessura'][i])])
                    l1.insert(tk.END, string_lista)

        def add_valor():
            def fechar_janela():
                if (espessura_e.get() == '' or 
                    material_v.get() == ''):
                    messagebox.showwarning('Valores vazios','Favor preencher todos os valores antes de fechar a janela.')
                else:
                    valor_ = validacao_input(espessura_e.get())
                    if valor_ == False:
                        messagebox.showwarning('Valor da espessura','Valor da espessura inválido, favor utilizar somente números')
                    else:
                        self.var['piso_material'].append(material_v.get())
                        self.var['piso_espessura'].append(valor_)
                        string_lista = ' '.join([material_v.get(), espessura_e.get()])
                        l1.insert(tk.END, string_lista)
                        a_janela.destroy()

            a_janela = tk.Tk()
            a_janela.iconbitmap('Snow_Flake.ico')
            tk.Tk.wm_title(a_janela, 'Adicionar piso')
            lb1 = ttk.Label(a_janela, text='Material', width=25)
            lb1.grid(row=0, column=0, padx=1, pady=1, ipadx=1, ipady=1)
            lb2 = ttk.Label(a_janela, text='Espessura')
            lb2.grid(row=0, column=1, padx=1, pady=1, ipadx=1, ipady=1)
            material_v = tk.StringVar()
            material_v.set(0)
            first = list(materiais.keys())[0]
            materiais_lista = ttk.OptionMenu(a_janela, material_v, first, *materiais.keys())
            materiais_lista.grid(row=1, column=0)
            materiais_lista.config(width=23)
            espessura_e = ttk.Entry(a_janela, width=13)
            espessura_e.grid(row=1, column=1)
            b4 = ttk.Button(master=a_janela, text='Adicionar', command=fechar_janela)
            b4.grid(row=2, column=0, columnspan=2, padx=3, pady=3, ipadx=3, ipady=3)
            a_janela.mainloop()

        def del_valor():
            self.var['piso_material'].pop(l1.curselection()[0])
            self.var['piso_espessura'].pop(l1.curselection()[0])
            l1.delete(l1.curselection()[0])
        
        janela = tk.Tk()
        tk.Tk.wm_title(janela, 'Configuração do piso')
        janela.iconbitmap('Snow_Flake.ico')
        rw = 0
        label1 = ttk.Label(janela, text='Material')
        label1.grid(row=rw, column=0, padx=1, pady=1, ipadx=1, ipady=1)
        label2 = ttk.Label(janela, text='Espessura')
        label2.grid(row=rw, column = 1, padx=1, pady=1, ipadx=1, ipady=1)
        rw += 1

        l1 = tk.Listbox(janela, width=70, height=9)
        l1.grid(row=rw, column=0, columnspan=2, padx=3, pady=3, ipadx=3, ipady=3)
        rw +=1
        preencher_lista()

        b1 = ttk.Button(master=janela, text='Adicionar', command=add_valor)
        b1.grid(row=rw, column=0, padx=3, pady=3, ipadx=3, ipady=3)
        b2 = ttk.Button(master=janela, text='Excluir', command=del_valor)
        b2.grid(row=rw, column=1, padx=3, pady=3, ipadx=3, ipady=3)
        rw +=1

        b3 = ttk.Button(master=janela, text='Ok', command=janela.destroy, width=13)
        b3.grid(row=rw, column=0, columnspan=2, padx=3, pady=3, ipadx=3, ipady=3)

        janela.mainloop()

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, 'Criação de simulação')
        tk.Tk.iconbitmap(self, default='Snow_Flake.ico')
        # tk.Tk.geometry(self, '500x350')

        row, col = 0, 0
        # self.var = {}
        # self.var['piso_material'] = []
        # self.var['piso_espessura'] = []

        cabecario_variavel = ttk.Label(self, text='Variável', width=13)
        cabecario_variavel.grid(row=row, column=col, padx=1, pady=1, ipadx=1, ipady=1)
        cabecario_valor = ttk.Label(self, text='Valor', width=13)
        cabecario_valor.grid(row=row, column=col+1, padx=1, pady=1, ipadx=1, ipady=1)
        cabecario_unidade = ttk.Label(self, text='Unidade', width=13)
        cabecario_unidade.grid(row=row, column=col+2, padx=1, pady=1, ipadx=1, ipady=1)
        row+=1

        sep_ = ttk.Separator(self, orient='horizontal')
        sep_.grid(row=row, column=0, columnspan=3, padx=1, pady=1, ipadx=1, ipady=1)
        row+=1

        for key in self.linhas.keys():
            l1 = ttk.Label(self, text = self.linhas[key][0])
            l1.grid(row=row, column=col, padx=1, pady=1, ipadx=1, ipady=1)

            l2 = ttk.Label(self, text=self.linhas[key][2])
            l2.grid(row=row, column=col+2, padx=1, pady=1, ipadx=1, ipady=1)

            if self.linhas[key][1] == 'Input':
                self.var[key] = ttk.Entry(self, width=15)
                self.var[key].grid(row=row, column=col+1, padx=1, pady=1, ipadx=1, ipady=1)

                row += 1
        
            elif self.linhas[key][1] == 'Lista':
                self.var[key] = tk.StringVar(self)
                self.var[key].set(0)
                first = list(self.linhas[key][4].keys())[0]
                lista = ttk.OptionMenu(self, self.var[key],first, *self.linhas[key][4].keys())
                lista.grid(row=row, column=col+1, padx=1, pady=1, ipadx=1, ipady=1)
                lista.config(width=23)

                row += 1

            elif self.linhas[key][1] == 'Listbox':
                b1 = ttk.Button(master=self, text='Adicione valor', command=self.adicionar_valor)        
                b1.grid(row=row, column=col+1, padx=1, pady=1, ipadx=1, ipady=1)

                row+=1

            elif self.linhas[key][1] == 'passar':
                continue

        self.var['piso_material'] = []
        self.var['piso_espessura'] = []

        bOk = ttk.Button(self, text='Salvar', width=23,
                        command=lambda: self.salvar())
        bOk.grid(row=row, column=col+1, padx=1, pady=1, ipadx=1, ipady=1)

        bC = ttk.Button(self, text='Cancel', width=23,
                        command=lambda: self.destroy())
        bC.grid(row=row, column=col, padx=1, pady=1, ipadx=1, ipady=1)


class Janela_Edicao(Janela_Criacao):
    def __init__(self, simulacao):
        try:
            with open(simulacao, 'r') as f:
                self.arquivo = json.load(f)
            self.dados = self.arquivo['simulacao_ctr']['dados']
            super().__init__()
            tk.Tk.wm_title(self, 'Edição de simulação')
            for key in Janela_Criacao.linhas.keys():
                if Janela_Criacao.linhas[key][1] == 'Input':
                    Janela_Criacao.var[key].insert(0, self.dados[key])
                if Janela_Criacao.linhas[key][1] == 'Lista':
                    Janela_Criacao.var[key].set(self.dados[key])
            Janela_Criacao.var['piso_material'] = self.dados['piso_material']
            Janela_Criacao.var['piso_espessura'] = self.dados['piso_espessura']
        except:
            messagebox.showwarning('Favor selecionar','Favor selecionar um arquivo válido do diretório')


class Janela_Edicao_Propriedades(tk.Tk):
    lista_itens = {}

    def Pesquisar_Valor(self):
        self.diretorio.delete(0, tk.END)
        self.valor_pesquisar.get()
        for valor in self.lista_itens.keys():
            if str(self.valor_pesquisar.get()).lower() in valor.lower():
                self.diretorio.insert(0, valor)
        self.caixa_text.config(text='')
        self.caixa_text.update()

    def Limpar_Pesquisa(self):
        self.Atualizar_Lista()
        self.valor_pesquisar.delete(0, tk.END)
        self.caixa_text.config(text='')
        self.caixa_text.update()

    def Criar_Novo(self):
        messagebox.showwarning('Função não disponível', 'Função ainda não implementada')

    def Editar_Valor(self):
        # tk.Tk.__init__(self)
        # tk.Tk.wm_title(self, 'Editar Valor')
        # tk.Tk.iconbitmap(self, default='Snow_Flake.ico')
        # tk.Tk.geometry(self, '250x250')
        messagebox.showwarning('Função não disponível', 'Função ainda não implementada')

    def Exibir_Prop(self, event):
        try:
            selecao = self.diretorio.curselection()[0]
            item = self.diretorio.get(selecao)
            if isinstance(self.lista_itens[item], dict):
                texto = item+'\n'
                for i, j in self.lista_itens[item].items():
                    texto += ''.join(['[',str(i), ': ', str(j), '] '])
            else:
                prefixo = (self.prefixo if self.prefixo != None else '')
                texto = ''.join([item, '\n', prefixo, str(self.lista_itens[item])])
                if self.sufixo != None:
                    texto += self.sufixo
            self.caixa_text.config(text=texto, justify=tk.LEFT, font=fontes['M'])
            self.caixa_text.update()
        except:
            self.caixa_text.config(text='')
            self.caixa_text.update()

    def Atualizar_Lista(self):
        with open(self.arquivo, 'r') as f:
            self.lista_itens = json.load(f)
        self.diretorio.delete(0, tk.END)
        for i, j in self.lista_itens.items():
            self.diretorio.insert(0, i)

    def __init__(self, itens, arquivo,prefix=None, suffix=None):
        self.arquivo = arquivo
        self.prefixo = prefix
        self.sufixo = suffix
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, 'Lista de {}'.format(itens))
        tk.Tk.iconbitmap(self, default='Snow_Flake.ico')
        # tk.Tk.geometry(self, '500x380')

        # Campo de pesquisa
        frame_pesquisa = ttk.Frame(self)
        frame_pesquisa.pack(side=tk.TOP, fill=tk.X)
        self.valor_pesquisar = ttk.Entry(frame_pesquisa, width=40)
        self.valor_pesquisar.pack(side=tk.LEFT,padx=1, pady=1, ipadx=1, ipady=1)
        self.valor_pesquisar.bind('<Return>', lambda x:self.Pesquisar_Valor())
        botao_pesquisar = ttk.Button(frame_pesquisa, text='Pesquisar', command=lambda: self.Pesquisar_Valor())
        botao_pesquisar.pack(side=tk.LEFT,padx=1, pady=1, ipadx=1, ipady=1)
        limpar_pesquisa = ttk.Button(frame_pesquisa, text='Limpar', command=lambda: self.Limpar_Pesquisa())
        limpar_pesquisa.pack(side=tk.LEFT,padx=1, pady=1, ipadx=1, ipady=1)
        limpar_pesquisa.bind('<Escape>', lambda x:self.Limpar_Pesquisa())

        # Frame diretorio
        frame_diretorio = ttk.Frame(self)
        frame_diretorio.pack(side=tk.TOP, fill=tk.X)
        self.diretorio = tk.Listbox(frame_diretorio, width=70, height=15)
        self.diretorio.pack(side=tk.LEFT, padx=1, pady=1, ipadx=1, ipady=1)
        self.diretorio.bind('<Button-1>', self.Exibir_Prop)
        self.Atualizar_Lista()

        self.Barra_Rolagem = tk.Scrollbar(frame_diretorio)
        self.Barra_Rolagem.pack(side=tk.LEFT, fill=tk.Y)
        self.Barra_Rolagem.config(command=self.diretorio.yview)

        self.sep_1 = ttk.Separator(self, orient='horizontal')
        self.sep_1.pack(side=tk.TOP, fill=tk.X, padx=1, pady=1, ipadx=1, ipady=1)

        # self.caixa_text = tk.Label(self, text='')
        self.caixa_text = tk.Message(self,text='', width=420)
        self.caixa_text.pack(side=tk.TOP, fill=tk.X, padx=1, anchor='nw', pady=1, ipadx=1, ipady=1)
        # self.caixa_text.config(height=5, borderwidth=1, relief="solid", wraplength=430)

        botao_novo = ttk.Button(self, text='Novo',
                                command= lambda: self.Criar_Novo())
        botao_novo.pack(side=tk.RIGHT, anchor='se',padx=1, pady=1, ipadx=1, ipady=1)
        botao_editar = ttk.Button(self, text='Editar',
                                 command=lambda: self.Editar_Valor())
        botao_editar.pack(side=tk.RIGHT, anchor='se',padx=1, pady=1, ipadx=1, ipady=1)
        botao_cancelar = ttk.Button(self, text='Cancelar',
                                    command=lambda: self.destroy())
        botao_cancelar.pack(side=tk.RIGHT, anchor='se',padx=1, pady=1, ipadx=1, ipady=1)


class Janela_Principal(tk.Tk):

    home_path = os.getcwd()

    def Calcular(self):
        try:
            selecao = self.diretorio.curselection()[0]
            _arquivo = os.path.join(self.home_path,self.diretorio.get(selecao))
            with open(_arquivo, 'r') as f:
                dd = json.load(f)
            preencher = OBS.Simul()
            preencher.Preencher(dd)
            if preencher != False:
                resultados_ = preencher.Exportar()
                dd['simulacao_ctr']['resultados'] = resultados_
                with open(_arquivo, 'w') as f:
                    json.dump(dd, f)
            else:
                return messagebox.showwarning('Arquivo incorreto','Favor selecionar um arquivo com o conjunto correto de dados.')
        except:
            messagebox.showwarning('Selecionar arquivo','Favor selecionar um arquivo do diretório antes de calcular os resultados.')

    def enviar_edicao(self):
        try:
            selecao = self.diretorio.curselection()[0]
            arquivo = os.path.join(self.home_path, self.diretorio.get(selecao))
            Janela_Edicao(arquivo)
        except:
            messagebox.showwarning('Seleção','Favor selecionar um arquivo.')

    def Exportar_Excel(self):
        try:
            selecao = self.diretorio.curselection()[0]
            arquivo = os.path.join(self.home_path, self.diretorio.get(selecao))
        
            file = filedialog.asksaveasfile(mode='wb', defaultextension='.xlsx')
            if file is not None:
                # Importacao provisoria
                linhas = Janela_Criacao.linhas
                # Abre os resultados
                with open(arquivo,'r') as f:
                    data = json.load(f)
                # Separa em dados e resultados
                dados = data['simulacao_ctr']['dados']
                resultados = data['simulacao_ctr']['resultados']
                # Cria a planilha
                workbook = xlsxwriter.Workbook(file)
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
        except:
            messagebox.showwarning('Seleção inválida','Favor selecionar um arquivo para exportar\n que possua os resultados')

    def print_to_console(self, event):
        widget = event.widget
        try:
            if len(widget.curselection()) != 0:
                selection = widget.curselection()
                value = widget.get(selection[0])
                arq_ = os.path.join(self.home_path, value)
                with open(arq_, 'r') as f:
                    valores = json.load(f)
                data = valores.get('simulacao_ctr', None)
                if data != None:
                    _dados = data['dados']
                    texto_dados = ''
                    for key in Janela_Criacao.linhas.keys():
                        texto_dados += ''.join([Janela_Criacao.linhas[key][0],': ', str(_dados[key]), Janela_Criacao.linhas[key][2],'\n'])
                    self.text_dados.config(text=texto_dados, justify=tk.LEFT, font=fontes['M'])
                    self.text_dados.update()
                    _resultados = data.get('resultados', None)
                    if _resultados != None:
                        texto_resultados = ''
                        for key in _resultados.keys():
                            texto_resultados += ''.join([key, ': ', str(round(_resultados[key][0],2)), _resultados[key][1], '\n'])
                        self.text_resultados.config(text=texto_resultados, justify=tk.LEFT, font=fontes['M'])
                        self.text_resultados.update()
                    else:
                        self.text_resultados.config(text='')
                        self.text_resultados.update()
                    # TODO implementar para preencher os valores dos resultados
                else:
                    self.text_dados.config(text='')
                    self.text_resultados.config(text='')
                    self.text_dados.update()
                    self.text_resultados.update()
        except:
            pass

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, 'Refri Calc Soft')
        tk.Tk.iconbitmap(self, default='Snow_Flake.ico')
        #TODO pensar em um nome melhor
        tk.Tk.geometry(self, '1000x700') # widthXheight

        container = tk.Frame(self)
        container.pack(side = 'top', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # Cria Frames para os botoes
        frame_botao = ttk.Frame(container)
        frame_botao.pack(side=tk.TOP, fill=tk.X)

        botao_rodar = ttk.Button(frame_botao, text='Calcular',
                                command=lambda: self.Calcular())
        botao_rodar.pack(side=tk.LEFT, padx=2, pady=2, ipady=2, ipadx=2)
        botao_salvar = ttk.Button(frame_botao, text='Criar', 
                                    command=lambda: Janela_Criacao())
        botao_salvar.pack(side=tk.LEFT, padx=2, pady=2, ipady=2, ipadx=2)
        botao_editar = ttk.Button(frame_botao, text='Editar',
                                    command=lambda: self.enviar_edicao())
        botao_editar.pack(side=tk.LEFT, padx=2, pady=2, ipady=2, ipadx=2)
        botao_atualizar = ttk.Button(frame_botao, text='Atualizar',
                                    command=lambda: self.preencher_lista_dir(self.home_path))
        botao_atualizar.pack(side=tk.LEFT, padx=2, pady=2, ipadx=2, ipady=2)

        # Separadores
        sep1 = ttk.Separator(container, orient= 'horizontal')
        sep1.pack(side=tk.TOP, fill=tk.X, padx=3, pady=3, ipadx=3, ipady=3)

        frame_dir = tk.Frame(container)
        frame_dir.pack(side=tk.LEFT)
        self.diretorio = tk.Listbox(frame_dir, width=90, height=40)
        self.diretorio.pack(padx=3,pady=3, ipadx=3, ipady=3)
        self.diretorio.bind('<Button-1>', self.print_to_console)

        # Separador 
        separador = ttk.Separator(container, orient='vertical')
        separador.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2, ipadx=2, ipady=2)

        # Cria o construtor
        tabControl = ttk.Notebook(container, width=500, height=700)
        tabControl.pack(side=tk.RIGHT, fill='both', padx=2, pady=2, ipadx=2, ipady=2)

        # Cria as abas
        self.tab_dados = ttk.Frame(tabControl)
        tabControl.add(self.tab_dados, text='Dados da simulação')
        self.tab_resultados = ttk.Frame(tabControl)
        tabControl.add(self.tab_resultados, text='Resultados')

        # Preencher a lista do diretório
        self.preencher_lista_dir(self.home_path)

        self.text_dados = tk.Label(self.tab_dados, text='')
        self.text_resultados = tk.Label(self.tab_resultados, text='')
        self.text_dados.pack(anchor='nw', padx=2, pady=2,ipadx=2, ipady=2)
        self.text_resultados.pack(anchor='nw', padx=2, pady=2,ipadx=2, ipady=2)

        # Menus
        menubar = tk.Menu(container)

        # Menu de arquivos
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menu_arquivo.add_command(label='Editar', command=lambda: self.enviar_edicao())
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label='Trocar diretorio', command=lambda: self.preencher_lista_dir(filedialog.askdirectory()))
        menu_arquivo.add_command(label='Sair', command=lambda: self.destroy())
        menubar.add_cascade(label='Arquivo', menu=menu_arquivo)

        # Menu editar
        menu_editar = tk.Menu(menubar, tearoff=0)
        menu_editar.add_command(label='Exportar planilha', command=lambda: self.Exportar_Excel())
        menubar.add_cascade(label='Editar', menu=menu_editar)

        # Menu opções
        menu_opcoes = tk.Menu(menubar, tearoff=0)
        menu_opcoes.add_command(label='Lista materiais', command=lambda: Janela_Edicao_Propriedades('Materiais isolantes','coef_k_materiais.json',prefix='Cond. térmica k: ',suffix='W/mk'))
        menu_opcoes.add_command(label='Lista alimentos', command=lambda: Janela_Edicao_Propriedades('Alimentos', 'Alimentos.json'))
        menu_opcoes.add_command(label='Lista frutas', command=lambda: Janela_Edicao_Propriedades('Frutas', 'Calor_resp.json'))
        menu_opcoes.add_command(label='Lista cidades', command=lambda: Janela_Edicao_Propriedades('Cidades','Cidades.json'))
        menubar.add_cascade(label='Listas', menu=menu_opcoes)

        # Menu ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menu_ajuda.add_command(label='Ajuda', command=lambda: Janela_Ajuda())
        menu_ajuda.add_separator()
        menu_ajuda.add_command(label='Sobre', command=lambda: Sobre())
        menubar.add_cascade(label='Ajuda', menu=menu_ajuda)

        # Acrescenta os menus a janela
        tk.Tk.config(self, menu=menubar)

        log_line = tk.Frame(self)
        log_line.pack(side = 'bottom', fill='x')        
        sep4 = ttk.Separator(log_line, orient='horizontal')
        sep4.pack(fill='x')

    def Janela_aviso(self, texto=None):
        if texto is None:
            texto = 'Essa função ainda não foi implementada'
        w = tk.Tk()
        w.wm_title('AVISO!!!')
        w.geometry('250x250')
        t = ttk.Label(w, text=texto)
        t.pack(fill=tk.BOTH, pady=10)
        w.mainloop()

    def preencher_lista_dir(self, dir_path):
        if dir_path == '':
            pass
        else:
            try:
                self.diretorio.delete(0, tk.END)
                for arq in os.listdir(dir_path):
                    if os.path.splitext(arq)[1] =='.json':
                        self.diretorio.insert(tk.END, arq)
                self.home_path = dir_path
                print(dir_path)
            except:
                messagebox.showerror('Não foi possível trocar o diretório','Não foi possível efetuar a troca de diretório, por favor tente novamente.')

def main():
    # main = Janela_Criacao()
    main = Janela_Principal()
    main.mainloop()

if __name__ == '__main__':
    main()