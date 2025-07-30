import os

class Descricao_Valor:
	def __init__(self, nome, valor, nome_arquivo):
		self.nome = nome
		self.valor = valor
		self.nome_arquivo = nome_arquivo


	def adicionando_itens(self):
		# Função para criar arquivo se não existir e adiciona itens sempre ao final do arquivo.
		itens = f"{self.nome};{self.valor}"
		with open(self.nome_arquivo, "a", encoding="utf-8") as arquivo:
			arquivo.write(f"{itens}\n")


	def itens_lista(self):
		# lendo e guardando todos o conteúdos do arquivo em uma lista
		if os.path.exists(self.nome_arquivo):# Verifica o arquivo para não dar erro.
			with open(self.nome_arquivo, "r", encoding="utf-8") as arquivo:
				lista = []
				for item in arquivo:
					item = item.strip().split(";")
					lista.append(item)
			return lista


	def soma_valor(self):
		# Somando os valores na lista:
		soma = 0
		for itens in self.itens_lista():
			soma += float(itens[1])
		return soma


