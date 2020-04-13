import tkinter as tk

fonte = {
        'G':('Arial 13 bold'),
        'M':('Arial 11')
}

class Sobre(tk.Tk):
    """Essa classe cria uma janela com informações sobre o criado do Refri Calc Soft e qual as itenções do software"""
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, 'Sobre esse programa')
        tk.Tk.iconbitmap(self, default='Snow_Flake.ico')
        tk.Tk.geometry(self, '500x300')

        titulo = tk.Label(self, text='Refri Calc Soft', font=fonte['G'])
        titulo.pack(side=tk.TOP, fill=tk.X)
        texto = tk.Message(self)
        texto.pack(fill=tk.BOTH)
        textinho = ["\tEsse programa tem a intenção de servir como uma ferramenta no aprendizado de refrigeração, ",
                    "tanto para cursos técnicos quanto para superiores. Ele foi elaborado como um projeto de aula e ",
                    "de forma alguma se intitula como um programa profissional ou se responsabiliza pelos resultados obtidos.",
                    "\n\tCaso surja alguma dúvida na utilização ou seja verificado algum erro tanto no cálculo quanto em ",
                    "alguma das funções, peço que entrem em contato comigo pelo meu e-mail: pedro.moresco93@outlook.com",
                    " utilizando o assunto 'Refri Calc Soft Contato' e forneçam o maior número de informações possíveis ",
                    "para que eu possa efetivamente ajudar.",
                    "\nEsse programa está sob a licença MIT.",
                    "\nv1.1 Dez 2018"]
        textui = ''.join(textinho)
        texto.config(text=textui, font=fonte['M'])
        texto.update()

def main():
    janela = Sobre()
    janela.mainloop()

if __name__ == '__main__':
    main()