import os

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

    #==================== Funções Livros ====================

    def adicionar_livro(self, titulo, autor, categorias, exemplares):
        for livro in self.livros.values():
            if livro["titulo"].strip().lower() == titulo.strip().lower() and \
                livro["autor"].strip().lower() == autor.strip().lower():
                print(f"\nErro: O livro '{titulo}' de {autor} já está cadastrado na biblioteca")
                continuar()
                return
        
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
        else:
            for id_livro, dados in self.livros.items():
                print(f"{id_livro}: {dados['titulo']} ({dados['autor']}) - Categorias: {', '.join(dados['categorias'])} - Exemplares: {dados['exemplares']}")
        continuar()
        
    def deletar_livro(self):
        if not self.livros:
            print("\nNenhum livro cadastrado.")
            continuar()
            return
        
        print("\n--- Livros Cadastrados ---")
        for id_livro, dados in self.livros.items():
            print(f"{id_livro}: {dados['titulo']} ({dados['autor']}) - Exemplares: {dados['exemplares']}")
            
        try:
            id_livro = int(input("\nDigite o ID do livro que deseja deletar (0 para voltar): "))
            if id_livro == 0:
                return
            if id_livro not in self.livros:
                print("ID inválido.")
                continuar()
                return
            
            livro_emprestado = False

            for usuario in self.usuarios.values():
                if id_livro in usuario["emprestimos"]:
                    livro_emprestado = True
                    break
                
            if livro_emprestado == True:
                print("Esse livro está emprestado para alguém")
                continuar()
                return
        
            titulo = self.livros[id_livro]["titulo"]
            del self.livros[id_livro]
            
            if id_livro in self.fila_espera:
                del self.fila_espera[id_livro]
                
            self.historico.adicionar(f"Livro deletado: {titulo} (ID: {id_livro})")
            print(f"Livro '{titulo}' foi deletado com sucesso.")
        except ValueError:
            print("Entrada inválida. Digite um número válido")
        continuar()
            


    #==================== Funções Usuários ====================

    def cadastrar_usuario(self, nome, email, telefone, cpf):
        for usuario in self.usuarios.values():
            if usuario["cpf"] == cpf:
                print(f"\nErro: Já existe um usuário cadastrado com o CPF {cpf}.")
                continuar()
                return

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
        print(f"Usuário '{nome}' cadastrado com sucesso!")
        continuar()

    def mostrar_usuarios(self):
        print("\nUsuários cadastrados:")
        if not self.usuarios:
            print("Nenhum usuário cadastrado.")
        else:
            for id_user, info in self.usuarios.items():
                livros = [self.livros[l]["titulo"] for l in info["emprestimos"]]
                print(f"\nID: {id_user} - Nome: {info['nome']} - Email: {info['email']} - Telefone: {info['telefone']} - CPF: {info['cpf']}")
                print(f"Empréstimos: {', '.join(livros) if livros else 'Nenhum'}")
        continuar()
        
    def deletar_usuario(self):
        if not self.usuarios:
            print("\nNenhum usuário cadastrado")
            continuar()
            return

        print("\n--- Usuários Cadastrados ---")
        for id_user, info in self.usuarios.items():
            print(f"{id_user}: {info['nome']} - Email: {info['email']} - Empréstimos: {len(info['emprestimos'])}")
            
        try:
            id_usuario = int(input("\nDigite o ID do usuário que deseja deletar (0 para voltar): "))
            if id_usuario == 0:
                return
            elif id_usuario not in self.usuarios:
                print("ID inválido.")
                continuar()
                return
            elif self.usuarios[id_usuario]["emprestimos"]:
                print("Este usuário possui livros emprestados. Devolva todos os livros antes de excluí-lo.")
                continuar()
                return
            
            nome = self.usuarios[id_usuario]["nome"]
            del self.usuarios[id_usuario]
            
            for fila in self.fila_espera.values():
                if id_usuario in fila:
                    fila.remove(id_usuario)
                
            self.historico.adicionar(f"Usuário deletado: {nome} (ID: {id_usuario})")
            print(f"Usuário '{nome}' deletado com sucesso.")
            
        except ValueError:
            print("ID inválido")
        continuar()
    #==================== Funções Empréstimos ====================

    def selecionar_usuario(self):
        if not self.usuarios:
            print("\nNenhum usuário cadastrado.")
            continuar()
            return None

        print("\n--- Usuários Cadastrados ---")
        for id_user, info in self.usuarios.items():
            livros = [self.livros[lid]['titulo'] for lid in info['emprestimos']]
            print(f"{id_user}: {info['nome']} - Empréstimos: {', '.join(livros) if livros else 'Nenhum'}")

        while True:
            try:
                uid = int(input("\nID do usuário (0 para voltar): "))
                if uid == 0:
                    return None
                if uid in self.usuarios:
                    return uid
                print("ID inválido.")
            except ValueError:
                print("Digite um número válido.")

    def selecionar_livro(self):
        if not self.livros:
            print("\nNenhum livro cadastrado.")
            continuar()
            return None

        print("\n--- Livros Disponíveis ---")
        for id_livro, dados in self.livros.items():
            print(f"{id_livro}: {dados['titulo']} ({dados['autor']}) - Exemplares: {dados['exemplares']}")

        while True:
            try:
                lid = int(input("\nID do livro (0 para voltar): "))
                if lid == 0:
                    return None
                if lid in self.livros and self.livros[lid]["exemplares"] > 0:
                    return lid
                print("ID inválido ou sem exemplares.")
            except ValueError:
                print("Digite um número válido.")

    def selecionar_livro_para_devolver(self, id_usuario):
        emprestimos = self.usuarios[id_usuario]["emprestimos"]
        if not emprestimos:
            print("Usuário não possui livros para devolver.")
            continuar()
            return None

        print("\n--- Livros emprestados pelo usuário ---")
        for lid in emprestimos:
            titulo = self.livros[lid]["titulo"]
            print(f"{lid}: {titulo}")

        while True:
            try:
                lid = int(input("\nSelecione o ID do livro para devolver ou digite 0 para voltar: "))
                if lid == 0:
                    print("Voltando ao menu anterior...")
                    return None
                elif lid in emprestimos:
                    return lid
                else:
                    print("ID inválido. Selecione um dos livros que o usuário possui.")
            except ValueError:
                print("Entrada inválida, por favor insira um número válido.")
                
    def selecionar_livro_fila_de_espera(self):
        if not self.livros:
            print("\nNenhum livro cadastrado.")
            continuar()
            return None

        print("\n--- Livros Disponíveis ---")
        for id_livro, dados in self.livros.items():
            print(f"{id_livro}: {dados['titulo']} ({dados['autor']}) - Exemplares: {dados['exemplares']}")

        while True:
            try:
                lid = int(input("\nID do livro (0 para voltar): "))
                if lid == 0:
                    return None
                if lid in self.livros:
                    return lid
                print("ID inválido.")
            except ValueError:
                print("Digite um número válido.")

    def emprestar_livro(self, id_usuario, id_livro):
        if id_livro in self.usuarios[id_usuario]["emprestimos"]:
            print("Usuário já possui este livro.")
        elif self.fila_espera[id_livro] and self.fila_espera[id_livro][0] != id_usuario:
            print("Livro está reservado por outro usuário.")
        else:
            self.usuarios[id_usuario]["emprestimos"].append(id_livro)
            self.pilha_emprestimos.append((id_usuario, id_livro))
            self.livros[id_livro]["exemplares"] -= 1

            if self.fila_espera[id_livro] and self.fila_espera[id_livro][0] == id_usuario:
                self.fila_espera[id_livro].pop(0)

            titulo = self.livros[id_livro]["titulo"]
            nome = self.usuarios[id_usuario]["nome"]
            self.historico.adicionar(f"{nome} emprestou '{titulo}'")
            print(f"Livro '{titulo}' emprestado para {nome}.")
        continuar()

    def devolver_livro(self, id_usuario, id_livro):
        if id_livro in self.usuarios[id_usuario]["emprestimos"]:
            self.usuarios[id_usuario]["emprestimos"].remove(id_livro)
            titulo = self.livros[id_livro]["titulo"]
            nome = self.usuarios[id_usuario]["nome"]

            if self.fila_espera[id_livro]:
                proximo_usuario = self.fila_espera[id_livro].pop(0)
                self.usuarios[proximo_usuario]["emprestimos"].append(id_livro)
                nome_proximo = self.usuarios[proximo_usuario]["nome"]
                self.historico.adicionar(f"Livro '{titulo}' devolvido por {nome}. Emprestado a {nome_proximo}.")
                print(f"{nome} devolveu '{titulo}'. Emprestado a {nome_proximo}.")
            else:
                self.historico.adicionar(f"{nome} devolveu '{titulo}'")
                self.livros[id_livro]["exemplares"] += 1
                print(f"{nome} devolveu '{titulo}'.")
        else:
            print("Empréstimo não encontrado.")
        continuar()

    def adicionar_fila_espera(self, id_usuario, id_livro):
        if self.livros[id_livro]["exemplares"] > 0:
            print("Aviso: Esse livro está disponível para empréstimo atualmente.")
            continuar()
            return        
        
        if id_usuario not in self.fila_espera[id_livro]:
            self.fila_espera[id_livro].append(id_usuario)
            self.historico.adicionar(f"Usuário {id_usuario} entrou na fila para o livro {id_livro}")
            print(f"Usuário adicionado à fila de espera de '{self.livros[id_livro]['titulo']}'.")
        else:
            print("Usuário já está na fila deste livro.")
        continuar()

    #==================== Funções Relatórios ====================

    def listar_emprestimos_atuais(self):
        print("\n--- Empréstimos Atuais ---")
        encontrou = False
        for uid, dados in self.usuarios.items():
            if dados["emprestimos"]:
                encontrou = True
                nome = dados["nome"]
                livros = [self.livros[lid]["titulo"] for lid in dados["emprestimos"]]
                print(f"{nome} está com: {', '.join(livros)}")
        if not encontrou:
            print("Nenhum empréstimo ativo.")
        continuar()

    def listar_filas_de_espera(self):
        print("\n--- Filas de Espera ---")
        encontrou = False
        for lid, fila in self.fila_espera.items():
            if fila:
                encontrou = True
                titulo = self.livros[lid]["titulo"]
                nomes = [self.usuarios[uid]["nome"] for uid in fila]
                print(f"Livro: {titulo} - Fila: {', '.join(nomes)}")
        if not encontrou:
            print("Nenhuma fila de espera ativa.")
        continuar()

    def mostrar_historico(self):
        print("\nHistórico de ações:")
        if not self.historico.head:
            print("Nenhuma ação registrada ainda.")
        else:
            self.historico.mostrar()
        continuar()

#==================== Menus ====================

def menu():
    biblioteca = BibliotecaCLI()
    while True:
        print("\n===== Biblioteca CLI =====")
        print("1. Gerenciar livros")
        print("2. Gerenciar usuários")
        print("3. Empréstimos")
        print("4. Relatórios e histórico")
        print("5. Limpar terminal")
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
        elif op == "5":
            limpar_terminal()
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
            continuar()

def submenu_livros(biblioteca):
    while True:
        print("\n--- Gerenciar Livros ---")
        print("1. Adicionar livro")
        print("2. Deletar livro")
        print("3. Mostrar livros")
        print("0. Voltar")
        op = input("Escolha: ")
        if op == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            categorias = input("Categorias (separadas por vírgula): ").split(",")
            categorias = [c.strip() for c in categorias if c.strip()]
            while True:
                try:
                    exemplares = int(input("Quantidade de exemplares: "))
                    break
                except ValueError:
                    print("Erro: Exemplares deve ser numérico.")
            biblioteca.adicionar_livro(titulo, autor, categorias, exemplares)
        elif op == "2":
            biblioteca.deletar_livro()
        elif op == "3":
            biblioteca.mostrar_livros()
        elif op == "0":
            break
        else:
            print("Opção inválida.")
            continuar()

def submenu_usuarios(biblioteca):
    while True:
        print("\n--- Gerenciar Usuários ---")
        print("1. Cadastrar usuário")
        print("2. Deletar usuário")
        print("3. Mostrar usuários")
        print("0. Voltar")
        op = input("Escolha: ")
        if op == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            while True:
                telefone = input("Telefone: ")
                try:
                    telefone = int(telefone)
                    break
                except ValueError:
                    print("\nErro: Telefone deve ser um valor númerico! Tente novamente")
            while True:
                cpf = input("CPF: ")
                try:
                    cpf = int(cpf)
                    break
                except ValueError:
                    print("\nErro: CPF deve ser um valor númerico! Tente novamente")
            biblioteca.cadastrar_usuario(nome, email, telefone, cpf)
        elif op == "2":
            biblioteca.deletar_usuario()
        elif op == "3":
            biblioteca.mostrar_usuarios()
        elif op == "0":
            break
        else:
            print("Opção inválida.")
            continuar()

def submenu_emprestimos(biblioteca):
    while True:
        print("\n--- Empréstimos ---")
        print("1. Emprestar livro")
        print("2. Devolver livro")
        print("3. Adicionar à fila de espera")
        print("0. Voltar")
        op = input("Escolha: ")
        if op == "1":
            uid = biblioteca.selecionar_usuario()
            if uid is not None:
                lid = biblioteca.selecionar_livro()
                if lid is not None:
                    biblioteca.emprestar_livro(uid, lid)
        elif op == "2":
            uid = biblioteca.selecionar_usuario()
            if uid is not None:
                lid = biblioteca.selecionar_livro_para_devolver(uid)
                if lid is not None:
                    biblioteca.devolver_livro(uid, lid)
        elif op == "3":
            uid = biblioteca.selecionar_usuario()
            if uid is not None:
                lid = biblioteca.selecionar_livro_fila_de_espera()
                if lid is not None:
                    biblioteca.adicionar_fila_espera(uid, lid)
        elif op == "0":
            break
        else:
            print("Opção inválida.")
            continuar()

def submenu_relatorios(biblioteca):
    while True:
        print("\n--- Relatórios e Histórico ---")
        print("1. Listar empréstimos atuais")
        print("2. Mostrar filas de espera")
        print("3. Mostrar histórico de ações")
        print("0. Voltar")
        op = input("Escolha: ")
        if op == "1":
            biblioteca.listar_emprestimos_atuais()
        elif op == "2":
            biblioteca.listar_filas_de_espera()
        elif op == "3":
            biblioteca.mostrar_historico()
        elif op == "0":
            break
        else:
            print("Opção inválida.")
            continuar()

def continuar():
    input("Pressione ENTER para continuar...")
    
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    menu()
