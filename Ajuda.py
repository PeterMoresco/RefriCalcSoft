import tkinter as tk 
from tkinter import ttk
import json 

fonte = ('Arial',11)

class Janela_Ajuda(tk.Tk):
    """Essa classe cria uma janela de ajuda para os usuários do RefriCalc Soft"""

    texto_corpo = {
    "Fluxo básico": ["\tBem vindo ao Refri Calc Soft, um software destinado a simulação e dimensionamento de carga térmica de refrigeração.",
        "O fluxo básico de trabalho funciona com os seguintes passos:\n - Configurar o diretório de trabalho \n - Criar a simulação",
        "\n - Atualizar a área de trabalho \n - Calcular os resultados \n - Visualizá-los na aba resultados",
        ""],
    "Diretórios":["\tO programa por padrão inicia no diretório aonde o executável se encontra.",
                " Para mudar o diretório de trabalho, vá no menu 'Arquivo' e selecione 'Trocar diretório', uma janela",
                " irá abrir e você poderá escolher a pasta para trabalhar. Assim que selecionar o diretório, clique em ",
                "'Selecionar pasta' e na janela principal serão mostrados todos os arquivos com extensão JSON na pasta atual."],
    "Criar simulação":["\tPara criar uma nova simulação basta clicar no botão 'Criar' na barra principal, uma janela irá aparecer ",
                "contendo todas os valores à serem preenchidos. Após preencher todos os campos clique em 'Salvar' e selecione a pasta para salvar e nomeie o arquivo.",
                "\n\tCaso algum dos campos não seja preenchido, ou seja preenchido com ",
                "um valor inválido, com texto no lugar de número por exemplo, um aviso será exibido e a simulação só poderá ",
                "ser salva após o problema ser corrigido.",
                "\nNão é se deve preencher a extensão, a mesma já é preenchida automaticamente."],
    "Visualizar dados":["\tApós criar a simulação, clique em 'Atualizar' na barra principal para que a sua simulação seja ",
                "listada na janela principal. Ao clicar na sua simulação os valores dos dados preenchidos irão aparecer na ",
                "aba lateral 'Dados da  simulação', e será possível a conferência do preenchimento apenas clicando nos arquivos",
                " sem a necessidade de abri-los."],
    "Calcular os resultados":["\tApós a simulação aparecer na listagem do diretório, selecione-a e clique em 'Calcular' na barra principal ",
                "feito isso, selecione novamente o arquivo e na aba 'Resultados' será possível a visualização dos resultados da simulação.\n",
                "\tOs resultados ficam salvos no mesmo arquivo dos dados da simulação, portanto você não irá perdê-lo ao fechar o programa."],
    "Editar":["\tA função editar permite que seja possível editar uma simulação já existente sem preencher todos os dados novamente, ",
                "pois eles são recuperados. Para usá-la selecione a simulação para editar e vá no menu 'Arquivo' -> 'Editar' ",
                "ou clique no botão na barra principal. Após efetuar as alterações necessárias, clique em 'Salvar' e selecione a pasta ",
                "e o nome da nova simulação.\n\tComo uma forma de evitar a confusão e incopatibilidade dos dados, ao editar uma simulação ",
                "os resultados não são levados para o novo arquivo, denvendo-se calcula-los novamente."],
    "Exportar planilha":["\tA função 'exportar planilha' exporta uma simulação ja calculada para uma planilha no formato 'xlsx'",
                "de forma a tornar a manipulação dos resultados do Refri Calc Soft fácil e acssível. Para usá-la selecione uma ",
                "simulação no diretório local e vá no menu 'Editar' e clique em 'Exportar planilha', após selecione o local para ",
                "salvá-la e um nome para o arquivo."],
    "Listas":["Todos os valores associados nas listas de seleção são oriundos das listas que devem sempre estar na mesma pasta ",
                "do executável do programa. Elas podem ser verificadas ao acessá-las no menu 'Listas'.\n\t",
                "Ao selecionar qualquer valor, os coeficientes e outros valores utilizados nos cálculos irão aparecer na ",
                "caixa de texto na parte inferior da janela. \n\tOs valores originais dessas listas foram retirados do material ",
                "do capítulo 8 disponível no endereço online http://www.professor.unisinos.br/mhmac/Refrigeracao/"],
    "Q_1": ["Variável de resultado."
            ,"\n\tCalor removido para resfriar um produto desde sua temperatura inicial até uma temperatura menor, acima do ponto de congelamento (para produtos resfriados)."],
	"Q_2": ["Variável de resultado.",
            "\n\tCalor removido para resfriar um produto desde sua temperatura inicial até sua temperatura de congelamento."],
	"Q_3": ["Variável de resultado.",
            "\n\tCalor removido para congelar o produto."],
	"Q_4": ["Variável de resultado.",
            "\n\tCalor removido para resfriar o produto desde uma temperatura de congelamento até a temperatura final abaixo desta."],
    "Qest":["Variável de resultado.",
            "\n\tCarga de refrigeração sensível e latente para fluxo de ar estabelecido."]
        }

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, 'Ajuda Refri Calc Soft')
        tk.Tk.iconbitmap(self, default='Snow_Flake.ico')
        tk.Tk.geometry(self,'700x500')

        self.lista_topicos = tk.Listbox(self, width=30)
        self.lista_topicos.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, ipady=5, ipadx=5)
        self.lista_topicos.bind('<Button-1>', self.Visualizar)

        self.texto_ajuda = tk.Text(self, width=150)
        self.texto_ajuda.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, ipady=5, ipadx=5)

        for key in self.texto_corpo.keys():
            self.lista_topicos.insert(tk.END, key)
        texto_ini = ''.join(self.texto_corpo['Fluxo básico'])
        self.texto_ajuda.insert(tk.END, texto_ini)
        self.texto_ajuda.config(font=fonte, spacing1=2, spacing2=5, spacing3=5)

    def Visualizar(self, event):
        try:
            selecao = self.lista_topicos.curselection()[0]
            item = self.lista_topicos.get(selecao)
            self.texto_ajuda.delete(1.0, tk.END)
            texto = ''.join(self.texto_corpo[item])
            self.texto_ajuda.insert(tk.END, texto)
            self.texto_ajuda.config(font=fonte, spacing1=2, spacing2=5, spacing3=5)
        except:
            pass

def main():
    janela = Janela_Ajuda()
    janela.mainloop()

if __name__ == '__main__':
    main()