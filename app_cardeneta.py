import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classe_anotacao import Descricao_Valor
import os


class App_Contas:

	def __init__(self, tela):
		self.arquivo_ganho = "Ganhos.txt"
		self.arquivo_gasto = "Gastos.txt"

		if not os.path.exists(self.arquivo_ganho):
			with open(self.arquivo_ganho, "w", encoding="utf-8") as txt:
				pass

		if not os.path.exists(self.arquivo_gasto):
			with open(self.arquivo_gasto, "w", encoding="utf-8") as txt_2:
				pass

		self.tela = tela # variável para criar a tela.
		self.tela.title("Cardeneta Financeira")# nomeia o abeçalho da janela
		self.tela.geometry("720x540")# Especifica o tamanho da janela.
		self.tela.configure()# se for necessário modificar algum detalhe da interface, por exemplo cor de fundo ou de letra.

		# Estilo de interface utilizando ttk
		interface_moderna = ttk.Style()# chama para personalizar aparência visual dos widgets
		interface_moderna.theme_use("clam")# Ativa um dos temas do ttk, esse é um dos temas mais utilizados
		interface_moderna.configure("TLabel", font=("Roboto", 14))# serve para alterar escrita, botões ou campos de entrada, personalisando cores, letras
		interface_moderna.configure("TEntry", padding=5)# padding especifica a largura do quadrado da entrada de texto.
		interface_moderna.configure("TButton", font=("Roboto", 12), padding=5)# Adiciona os botões as configurações da interface Stile

		# Utilizando Frame para centralizar os widgets na janela
		centralizando_app = tk.Frame(self.tela)
		centralizando_app.pack(pady=15)# Posisiona o frame dentro da janela e pady adiciona pixel de espaçamento vertical, para não ficar colado com outros widgets


		# Nome do Programa:
		ttk.Label(centralizando_app, text="Cardeneta Financeira").grid(row=0, column=1, pady=10)

		# Entrada de dados para receber nomes:
		ttk.Label(centralizando_app, text="Conta:").grid(row=1, column=0, pady=5) # texto para especificar caixa de texto
		self.nome_conta = ttk.Entry(centralizando_app, width=30)#criação da caixa de texto para receber dados de entrada
		self.nome_conta.grid(row=1, column=1, sticky="w", pady=5, padx=5)# especificando linha e coluna e espaçamento entre os widgets.

		# Entrada de dados para receber valores:
		ttk.Label(centralizando_app, text="Valor: R$").grid(row=2, column=0, pady=5)# row - linha, column - coluna, 
		self.valor_conta = ttk.Entry(centralizando_app, width=15) # width - largura
		self.valor_conta.grid(row=2, column=1, padx=5, sticky="w")

		# Criando um frame para o botão:
		botao_frame = tk.Frame(self.tela)
		botao_frame.pack(pady=5)

		# Botão para marcar ganhos
		ttk.Button(botao_frame, text="Adicionar Ganhos", command=lambda:self.incluindo_dados(self.arquivo_ganho, self.saldo_ganho)).grid(row=0, column=0, padx=5)
		ttk.Button(botao_frame, text="Adicionar Gastos", command=lambda:self.incluindo_dados(self.arquivo_gasto, self.saldo_gasto)).grid(row=0, column=2, padx=5)
		ttk.Button(botao_frame, text="Mostrar Lista Ganhos", command=lambda:self.mostrar_dados(self.arquivo_ganho)).grid(row=0, column=1, padx=5)
		ttk.Button(botao_frame, text="Mostrar Lista Gastos", command=lambda:self.mostrar_dados(self.arquivo_gasto)).grid(row=0, column=4, padx=5)

		# Caixa de texto para mostrar listas:
		self.caixa_texto = tk.Text(self.tela, height=10, font=("Roboto", 12))
		self.caixa_texto.pack(pady=10, padx=10, fill="both", expand=True)# fill-preencher

		self.saldo_ganho = ttk.Label(self.tela, text="Saldo Ganho: R$ 0.00", font=("Roboto", 12, "bold"))
		self.saldo_ganho.pack(side="left", padx=25)

		self.saldo_gasto = ttk.Label(self.tela, text="Saldo Gasto: R$ 0.00", font=("Roboto", 12, "bold"))
		self.saldo_gasto.pack(side="left", pady=10)

		self.saldo_liquido = ttk.Label(self.tela, text=f"Saldo Liquido: R$ 0.00", font=("Roboto", 12, "bold"))
		self.saldo_liquido.pack(side="left", padx=25)

		if os.path.exists(self.arquivo_ganho):# verificando se arquivo existe para ler valor
			self.saldo_total(self.arquivo_ganho, self.saldo_ganho)# mostra o saldo no app.

		if os.path.exists(self.arquivo_gasto):
			self.saldo_total(self.arquivo_gasto, self.saldo_gasto)

		if os.path.exists(self.arquivo_ganho) or os.path.exists(self.arquivo_gasto):
			self.soma_valores()

# Adicionando dados de entrada entre app e arquivo
	def incluindo_dados(self, arquivo, saldo):
		nome = self.nome_conta.get()
		try:
			valor = self.valor_conta.get()# é necessário ser chamado dentro da função para ler dados armazenados na memória.
			# se não for chamado aqui dentro os dados irão constar vazios.

			itens = Descricao_Valor(nome, float(valor), arquivo)# chamando classe para ler ou criar o arquivo.
			itens.adicionando_itens()# adicionando itens no arquivo

			self.nome_conta.delete(0, tk.END)# apagando string adicionados na caixa de entrada de dados após clicar o botão.
			self.valor_conta.delete(0, tk.END)

			self.caixa_texto.delete(1.0, tk.END)# apaga strings na caixa de texto a cada item adicionado.
			self.caixa_texto.insert(tk.END, f"{nome:.<50}R$ {float(valor):.2f}\n")# Imprime cada valor adicionado na caixa de texto

			if os.path.exists(self.arquivo_ganho) or os.path.exists(self.arquivo_gasto):# verificando se arquivo existe para ler valor
				self.saldo_total(arquivo, saldo)# atualiza o saldo a cada alteração do valor
				self.soma_valores()
		except ValueError:
			messagebox.showerror("Erro, Digite um valor válido!")
			return

	# Função para atualizar saldo no app.
	def saldo_total(self, arquivo, saldo):
		# Essa função foi criada para atualizar e ao abrir o aplicativo visualizar a soma dos valores
		#nome = self.nome_conta.get()
		#valor = self.valor_conta.get()
		itens = Descricao_Valor("", 0, arquivo)
		itens.itens_lista() # função que faz a leitura do arquivo e guarda tudo em uma lista
		saldo_lista = itens.soma_valor()# função que soma os valores que estão na lista
		if arquivo == self.arquivo_ganho:
			saldo.config(text=f"Saldo Ganhos: R$ {saldo_lista:.2f}")# atualização do saldo no app
		elif arquivo == self.arquivo_gasto:
			saldo.config(text=f"Saldo Gastos: R$ {saldo_lista:.2f}")
		return saldo_lista # retorno necessário para calcular valores de ganhos e de gastos na função soma_valores.


	def soma_valores(self):
		# soma de valores para mostrar o valor liquido que existe
		ganho = self.saldo_total(self.arquivo_ganho, self.saldo_ganho)
		gasto = self.saldo_total(self.arquivo_gasto, self.saldo_gasto)
		valor_liquido = ganho - gasto
		self.saldo_liquido.config(text=f"Saldo Liquido: R$ {valor_liquido:.2f}")
		


	def mostrar_dados(self, arquivo):
		# função para mostrar lista de contas.
		self.caixa_texto.delete(1.0, tk.END)
		itens = Descricao_Valor("", 0, arquivo)
		lista = itens.itens_lista()
		for nome, valor in lista:
			valor = float(valor)
			self.caixa_texto.insert(tk.END, f"{nome:.<50}R$ {valor:.2f}\n")


tela = tk.Tk()# Criando a janela principal
app = App_Contas(tela)# classe que a interface está construido
tela.mainloop()# .mainloop é necessário para manter o aplicativo aberto
