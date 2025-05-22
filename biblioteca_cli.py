class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
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

class BibliotecaCLI:
    def __init__(self):
        self.livros = {}  
        self.usuarios = {}  
        self.categorias = set()
        self.fila_espera = {}  
        self.pilha_emprestimos = []
        self.historico = LinkedList()
        self.proximo_id_livro = 1
        self.proximo_id_usuario = 1

    #====================Funções Livros====================

    def adicionar_livro(self, titulo, autor, categorias, exemplares):
        id_livro = self.proximo_id_livro
        self.livros[id_livro] = {
            "titulo": titulo,
            "autor": autor,
            "categorias": set(categorias), 
            "exemplares": exemplares
        }
        self.categorias.update(categorias)
        self.proximo_id_livro += 1
        self.fila_espera[id_livro] = []
        self.historico.adicionar(f"Livro adicionado: {titulo} (ID: {id_livro})")
        continuar()

    def mostrar_livros(self):
        print("\nLivros disponíveis:")
        if not self.livros:
            print("Nenhum livro cadastrado.")
        for id_livro, dados in self.livros.items():
            print(f"{id_livro}: {dados['titulo']} ({dados['autor']}) - Categorias: {', '.join(dados['categorias'])}")
        continuar()
    


    #====================Funções Usuarios====================

    def cadastrar_usuario(self, nome, email, telefone, cpf):
        id_usuario = self.proximo_id_usuario
        self.usuarios[id_usuario] = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "cpf": cpf,
            "emprestimos": []
        }
        self.proximo_id_usuario += 1
        self.historico.adicionar(f"Usuário cadastrado: {nome} (ID: {id_usuario})")
        continuar()


    def mostrar_usuarios(self):
        print("\nUsuários cadastrados:")
        if not self.usuarios:
            print("\nNenhum usuário cadastrado.")
        for id_user, info in self.usuarios.items():
            livros = [self.livros[l]["titulo"] for l in info["emprestimos"]]
            print(f"{id_user}: {info['nome']} - Empréstimos: {', '.join(livros) if livros else 'Nenhum'}")
        continuar()


    #====================Funções Emprestimos====================

    def selecionar_usuario(self):
        print("\n--- Usuários Cadastrados ---")
        if not self.usuarios:
            print("Nenhum usuário cadastrado.")
            continuar()
            return None

        for id_user, info in self.usuarios.items():
            print(f"{id_user}: {info['nome']} - Empréstimos: {', '.join([self.livros[lid]['titulo'] for lid in info['emprestimos']]) if info['emprestimos'] else 'Nenhum'}")
        
        while True:
            try:
                uid = int(input("\nSelecione o ID do usuário para o empréstimo: "))
                if uid in self.usuarios:
                    return uid
                else:
                    print("ID de usuário inválido, tente novamente.")
            except ValueError:
                print("Entrada inválida, por favor insira um número válido.")

    def selecionar_livro(self):
        print("\n--- Livros Disponíveis ---")
        if not self.livros:
            print("Nenhum livro disponível.")
            continuar()
            return None

        for id_livro, dados in self.livros.items():
            print(f"{id_livro}: {dados['titulo']} ({dados['autor']}) - Exemplares: {dados['exemplares']}")

        while True:
            try:
                lid = int(input("\nSelecione o ID do livro para empréstimo: "))
                if lid in self.livros and self.livros[lid]["exemplares"] > 0:
                    return lid
                else:
                    print("ID de livro inválido ou sem exemplares disponíveis, tente novamente.")
            except ValueError:
                print("Entrada inválida, por favor insira um número válido.")

    def emprestar_livro(self, id_usuario, id_livro):

        if id_livro in self.usuarios[id_usuario]["emprestimos"]:
            print("Usuário já possui este livro.")
            continuar()
            return

        if self.fila_espera[id_livro] and self.fila_espera[id_livro][0] != id_usuario:
            print("Livro está reservado por outro usuário.")
            continuar()
            return

        self.usuarios[id_usuario]["emprestimos"].append(id_livro)
        self.pilha_emprestimos.append((id_usuario, id_livro))
        self.livros[id_livro]["exemplares"] -= 1  

        if self.fila_espera[id_livro] and self.fila_espera[id_livro][0] == id_usuario:
            self.fila_espera[id_livro].pop(0)

        titulo = self.livros[id_livro]["titulo"]
        nome = self.usuarios[id_usuario]["nome"]
        self.historico.adicionar(f"{nome} emprestou '{titulo}'")
        print(f"Livro '{titulo}' emprestado com sucesso para {nome}.")

    def devolver_livro(self, id_usuario, id_livro):

        if id_livro in self.usuarios[id_usuario]["emprestimos"]:
            self.usuarios[id_usuario]["emprestimos"].remove(id_livro)
            titulo = self.livros[id_livro]["titulo"]
            nome = self.usuarios[id_usuario]["nome"]
            
            if self.fila_espera[id_livro]:
                proximo_usuario = self.fila_espera[id_livro].pop(0)
                self.usuarios[proximo_usuario]["emprestimos"].append(id_livro)
                nome_proximo_usuario = self.usuarios[proximo_usuario]["nome"]
                
                self.historico.adicionar(f"Livro '{titulo}' devolvido por {nome}. Emprestado a {nome_proximo_usuario}.")
                print(f"{nome} devolveu o livro '{titulo}'. O livro foi emprestado a {nome_proximo_usuario}.")
                continuar()
            else:
                self.historico.adicionar(f"{nome} devolveu '{titulo}'")
                print(f"{nome} devolveu o livro '{titulo}'.")
                continuar()
        else:
            print("Empréstimo não encontrado para esse usuário e livro.")
            continuar()

    def adicionar_fila_espera(self, id_usuario, id_livro):

        if id_usuario not in self.fila_espera[id_livro]:
            self.fila_espera[id_livro].append(id_usuario)
            self.historico.adicionar(f"Usuário {id_usuario} entrou na fila para o livro {id_livro}")
            print(f"Usuário adicionado à fila de espera do livro '{self.livros[id_livro]['titulo']}'.")
        else:
            print("Usuário já está na fila de espera deste livro.")



    #====================Funções Emprestimos====================

    def listar_emprestimos_atuais(self):
        print("\n--- Empréstimos Atuais ---")
        encontrou = False
        for uid, dados in self.usuarios.items():
            if dados["emprestimos"]:
                encontrou = True
                nome = dados["nome"]
                livros = [self.livros[lid]["titulo"] for lid in dados["emprestimos"]]
                print(f"{nome} está com: {', '.join(livros)}")
                continuar()
        if not encontrou:
            print("Nenhum empréstimo ativo no momento.")
            continuar()

    def listar_filas_de_espera(self):
        print("\n--- Filas de Espera ---")
        encontrou = False
        for lid, fila in self.fila_espera.items():
            if fila:
                encontrou = True
                titulo = self.livros[lid]["titulo"]
                nomes = [self.usuarios[uid]["nome"] for uid in fila]
                print(f"{titulo}: {', '.join(nomes)}")
                continuar()

        if not encontrou:
            print("Nenhuma fila de espera ativa.")
            continuar()

    def mostrar_historico(self):
        print("\nHistórico de ações:")
        if not self.historico.head:
            print("Nenhuma ação registrada ainda.")
            continuar()
        else:
            self.historico.mostrar()
            continuar()



#====================Menu Principal====================
def menu():
    biblioteca = BibliotecaCLI()
    while True:
        print("\n===== Biblioteca CLI =====")
        print("1. Gerenciar livros")
        print("2. Gerenciar usuários")
        print("3. Empréstimos")
        print("4. Relatórios e histórico")
        print("0. Sair")
        op = input("\nEscolha: ")
        if op == "1":
            submenu_livros(biblioteca)
        elif op == "2":
            submenu_usuarios(biblioteca)
        elif op == "3":
            submenu_emprestimos(biblioteca)
        elif op == "4":
            submenu_relatorios(biblioteca)
        elif op == "0":
            print("\nSaindo...")
            break
        else:
            print("\nOpção inválida.")
            continuar()

#====================Menu Livros====================
def submenu_livros(biblioteca):
    while True:
        print("\n--- Gerenciar Livros ---")
        print("1. Adicionar livro")
        print("2. Mostrar livros")
        print("0. Voltar")
        op = input("\nEscolha: ")
        if op == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            categorias = input("Categorias (separadas por vírgula): ").split(",")
            exemplares = int(input("Quantidade de exemplares: "))
            biblioteca.adicionar_livro(titulo, autor, [c.strip() for c in categorias], exemplares)
        elif op == "2":
            biblioteca.mostrar_livros()
        elif op == "0":
            break
        else:
            print("\nOpção inválida.")
            continuar()


#====================Menu Usuarios====================
def submenu_usuarios(biblioteca):
    while True:
        print("\n--- Gerenciar Usuários ---")
        print("1. Cadastrar usuário")
        print("2. Mostrar usuários")
        print("0. Voltar")
        op = input("\nEscolha: ")
        if op == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            cpf = input("CPF: ")
            biblioteca.cadastrar_usuario(nome, email, telefone, cpf)
        elif op == "2":
            biblioteca.mostrar_usuarios()
        elif op == "0":
            break
        else:
            print("\nOpção inválida.")
            continuar()



#====================Menu Emprestimos====================
def submenu_emprestimos(biblioteca):
    while True:
        print("\n--- Empréstimos ---")
        print("1. Emprestar livro")
        print("2. Devolver livro")
        print("3. Adicionar à fila de espera")
        print("0. Voltar")
        op = input("\nEscolha: ")
        if op == "1":
            uid = biblioteca.selecionar_usuario()
            if uid is not None:
                lid = biblioteca.selecionar_livro()
                if lid is not None:
                    biblioteca.emprestar_livro(uid, lid)
        elif op == "2":
            uid = biblioteca.selecionar_usuario()
            if uid is not None:
                lid = biblioteca.selecionar_livro()
                if lid is not None:
                    biblioteca.devolver_livro(uid, lid)
        elif op == "3":
            uid = biblioteca.selecionar_usuario()
            if uid is not None:
                lid = biblioteca.selecionar_livro()
                if lid is not None:
                    biblioteca.adicionar_fila_espera(uid, lid)
        elif op == "0":
            break
        else:
            print("\nOpção inválida.")
            continuar()


#====================Menu Relatorios====================
def submenu_relatorios(biblioteca):
    while True:
        print("\n--- Relatórios e Histórico ---")
        print("1. Listar empréstimos atuais")
        print("2. Mostrar filas de espera")
        print("3. Mostrar histórico de ações")
        print("0. Voltar")
        op = input("\nEscolha: ")
        if op == "1":
            biblioteca.listar_emprestimos_atuais()
        elif op == "2":
            biblioteca.listar_filas_de_espera()
        elif op == "3":
            biblioteca.mostrar_historico()
        elif op == "0":
            break
        else:
            print("\nOpção inválida.")
            continuar()

#====================Continuar====================
def continuar():
    input('...')

if __name__ == "__main__":
    menu()

