# Lista encadeada simples para histórico
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Historico:
    def __init__(self):
        self.head = None

    def adicionar(self, acao):
        novo = Node(acao)
        novo.next = self.head
        self.head = novo

    def mostrar(self):
        atual = self.head
        while atual:
            print(f"- {atual.data}")
            atual = atual.next

# Estrutura principal
class BibliotecaCLI:
    def __init__(self):
        self.livros = {}  
        self.usuarios = {}  
        self.categorias = set()
        self.fila_espera = {}  
        self.pilha_emprestimos = []
        self.historico = Historico()
        self.proximo_id_livro = 1
        self.proximo_id_usuario = 1


    #Adicionar Novo Livro
    # def adicionar_livro(self, titulo, autor, categorias, exemplares):
       
    #Cadastrar Novo Usuario
    # def cadastrar_usuario(self, nome, email, telefone, cpf):

    #Emprestar Livro a um Usuario Existente
    # def emprestar_livro(self, id_usuario, id_livro):
       
    #Devolver Livro A Biblioteca
    # def devolver_livro(self, id_usuario, id_livro):

    #Adicionar Livro a Fila de Espera
    #def adicionar_fila_espera(self, id_usuario, id_livro):

    #Exibir Livros Disponíveis
    # def mostrar_livros(self):

    #Exibir Usuarios Cadastrados
    # def mostrar_usuarios(self):
       
    #Exibir Histórico De Ações
    # def mostrar_historico(self):

    #Listar Empréstimos Atuais
    # def listar_emprestimos_atuais(self):

    #Listar Filas de Espera
    # def listar_filas_de_espera(self):



#Menus

#Submenu Livros
def submenu_livros(biblioteca):
    while True:
        print("\n--- Gerenciar Livros ---")
        print("1. Adicionar livro")
        print("2. Mostrar livros")
        print("0. Voltar")

#Submenu Usuarios
def submenu_usuarios(biblioteca):
    while True:
        print("\n--- Gerenciar Usuários ---")
        print("1. Cadastrar usuário")
        print("2. Mostrar usuários")
        print("0. Voltar")

#Submenu Emprestimos
def submenu_emprestimos(biblioteca):
    while True:
        print("\n--- Empréstimos ---")
        print("1. Emprestar livro")
        print("2. Devolver livro")
        print("3. Adicionar à fila de espera")
        print("0. Voltar")

#Submenu Relatorios
def submenu_relatorios(biblioteca):
    while True:
        print("\n--- Relatórios e Histórico ---")
        print("1. Listar empréstimos atuais")
        print("2. Mostrar filas de espera")
        print("3. Mostrar histórico de ações")
        print("0. Voltar")

#Menu Principal
def menu():
    biblioteca = BibliotecaCLI()
    while True:
        print("\n===== Biblioteca CLI =====")
        print("1. Gerenciar livros")
        print("2. Gerenciar usuários")
        print("3. Empréstimos")
        print("4. Relatórios e histórico")
        print("0. Sair")
        op = input("Escolha: ")
        if op == "1":
            submenu_livros(biblioteca)
        elif op == "2":
            submenu_usuarios(biblioteca)
        elif op == "3":
            submenu_emprestimos(biblioteca)
        elif op == "4":
            submenu_relatorios(biblioteca)
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
