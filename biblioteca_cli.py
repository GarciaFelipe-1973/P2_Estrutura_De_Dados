import os

def continuar():
    input("\nPressione Enter para continuar...")
    os.system("cls" if os.name == "nt" else "clear")

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

# DANIEL EXAME: A classe LivroNode representa um livro na lista duplamente encadeada
class LivroNode:
    def __init__(self, livro_id, titulo, autor, categorias, exemplares):
        self.livro_id = livro_id
        self.titulo = titulo
        self.autor = autor
        self.categorias = categorias
        self.exemplares = exemplares
        self.anterior = None
        self.proximo = None

# DANIEL EXAME: A lista duplamente encadeada para armazenar livros
class ListaDuplaLivros:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def adicionar(self, livro_node):
        if not self.inicio:
            self.inicio = self.fim = livro_node
        else:
            self.fim.proximo = livro_node
            livro_node.anterior = self.fim
            self.fim = livro_node

    def remover_por_id(self, livro_id):
        atual = self.inicio
        while atual:
            if atual.livro_id == livro_id:
                if atual.anterior:
                    atual.anterior.proximo = atual.proximo
                else:
                    self.inicio = atual.proximo

                if atual.proximo:
                    atual.proximo.anterior = atual.anterior
                else:
                    self.fim = atual.anterior
                return True
            atual = atual.proximo
        return False

class BibliotecaCLI:
    def __init__(self):
        self.livros = {}
        self.lista_livros = ListaDuplaLivros() 
        self.usuarios = {}
        self.categorias = set()
        self.fila_espera = {}
        self.pilha_emprestimos = []
        self.historico = LinkedList()
        self.proximo_id_livro = 1
        self.proximo_id_usuario = 1

    #==================== Funções Livros ====================
    # DANIEL EXAME: validações na função livros
    def adicionar_livro(self, titulo, autor, categorias, exemplares):
        if not titulo or not isinstance(titulo, str) or not titulo.strip():
            print("\nErro: O título do livro não pode ser vazio.")
            continuar()
            return
        if not autor or not isinstance(autor, str) or not autor.strip():
            print("\nErro: O autor do livro não pode ser vazio.")
            continuar()
            return
        if not categorias or not isinstance(categorias, list) or not all(isinstance(cat, str) and cat.strip() for cat in categorias):
            print("\nErro: As categorias devem ser uma lista de strings não vazias.")
            continuar()
            return
        if not isinstance(exemplares, int) or exemplares <= 0:
            print("\nErro: O número de exemplares deve ser um inteiro positivo.")
            continuar()
            return

        for livro in self.livros.values():
            if livro["titulo"].strip().lower() == titulo.strip().lower() and \
                livro["autor"].strip().lower() == autor.strip().lower():
                print(f"\nErro: O livro \'{titulo}\' de {autor} já está cadastrado na biblioteca")
                continuar()
                return

        id_livro = self.proximo_id_livro

        self.livros[id_livro] = {
            "titulo": titulo,
            "autor": autor,
            "categorias": set(categorias),
            "exemplares": exemplares
        }

        # DANIEL EXAME: Adiciona na lista duplamente encadeada
        livro_node = LivroNode(id_livro, titulo, autor, categorias, exemplares)
        self.lista_livros.adicionar(livro_node)

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

            # DANIEL EXAME: remove livros da lista duplamente encadeada 
            self.lista_livros.remover_por_id(id_livro)

            self.historico.adicionar(f"Livro deletado: {titulo} (ID: {id_livro})")
            print(f"Livro \'{titulo}\' foi deletado com sucesso.")
        except ValueError:
            print("Entrada inválida. Digite um número válido")
        continuar()
    
    # DANIEL EXAME: Função para navegar entre os livros cadastrados 
    def navegar_livros(self):
        atual = self.lista_livros.inicio
        if not atual:
            print("Nenhum livro cadastrado.")
            return

        while atual:
            print(f"\n=== Livro ID {atual.livro_id} ===")
            print(f"Título: {atual.titulo}")
            print(f"Autor: {atual.autor}")
            print(f"Categorias: {', '.join(atual.categorias)}")
            print(f"Exemplares: {atual.exemplares}")

            comando = input("\n[P] Próximo | [A] Anterior | [S] Sair: ").strip().lower()
            if comando == 'p':
                if atual.proximo:
                    atual = atual.proximo
                else:
                    print("Último livro da lista.")
            elif comando == 'a':
                if atual.anterior:
                    atual = atual.anterior
                else:
                    print("Primeiro livro da lista.")
            elif comando == 's':
                break
            else:
                print("Comando inválido.")


    #==================== Funções Usuários ====================
    # DANIEL EXAME: validações nas funcões de cadastro de usuário 
    def cadastrar_usuario(self, nome, email, telefone, cpf):
        if not nome or not isinstance(nome, str) or not nome.strip():
            print("\nErro: O nome do usuário não pode ser vazio.")
            continuar()
            return
        if not email or not isinstance(email, str) or "@" not in email or "." not in email:
            print("\nErro: O email do usuário é inválido.")
            continuar()
            return
        if not telefone or not isinstance(telefone, str) or not telefone.strip() or not telefone.isdigit():
            print("\nErro: O telefone do usuário é inválido. Deve conter apenas números.")
            continuar()
            return
        if not cpf or not isinstance(cpf, str) or not cpf.strip() or not cpf.isdigit() or len(cpf) != 11:
            print("\nErro: O CPF do usuário é inválido. Deve conter 11 dígitos numéricos.")
            continuar()
            return

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
        print(f"Usuário \'{nome}\' cadastrado com sucesso!")
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
            print(f"Usuário \'{nome}\' deletado com sucesso.")
            
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
            self.historico.adicionar(f"{nome} emprestou \'{titulo}\'")
            print(f"Livro \'{titulo}\' emprestado para {nome}.")
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
                self.historico.adicionar(f"Livro \'{titulo}\' devolvido por {nome}. Emprestado a {nome_proximo}.")
                print(f"{nome} devolveu \'{titulo}\'. Emprestado a {nome_proximo}.")
            else:
                self.historico.adicionar(f"{nome} devolveu \'{titulo}\'")
                self.livros[id_livro]["exemplares"] += 1
                print(f"{nome} devolveu \'{titulo}\'.")
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
            print(f"Usuário adicionado à fila de espera de \'{self.livros[id_livro]['titulo']}\'.")
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
        print("\n--- Histórico de Ações ---")
        if not self.historico.head:
            print("Nenhuma ação registrada.")
        else:
            self.historico.mostrar()
        continuar()

    def desfazer_emprestimo(self):
        if not self.pilha_emprestimos:
            print("\nNão há empréstimos para desfazer.")
            continuar()
            return

        id_usuario, id_livro = self.pilha_emprestimos.pop()
        if id_livro in self.usuarios[id_usuario]["emprestimos"]:
            self.usuarios[id_usuario]["emprestimos"].remove(id_livro)
            self.livros[id_livro]["exemplares"] += 1
            titulo = self.livros[id_livro]["titulo"]
            nome = self.usuarios[id_usuario]["nome"]
            self.historico.adicionar(f"Empréstimo desfeito: {titulo} de {nome}")
            print(f"Empréstimo de \'{titulo}\' para {nome} desfeito com sucesso.")
        else:
            print("Erro: Empréstimo não encontrado para desfazer.")
        continuar()

    #==================== Funções de Busca ====================
    # DANIEL EXAME: Função para exibir livro por ID (utilizando tupla, tinha faltado na priimeira apresentação) 
    def obter_detalhes_livro_tupla(self, livro_id):
        if livro_id in self.livros:
            dados = self.livros[livro_id]
            return (dados["titulo"], dados["autor"], dados["exemplares"])
        return None

    def buscar_livros_por_titulo(self, termo):
        encontrados = []
        for id_livro, dados in self.livros.items():
            if termo.lower() in dados["titulo"].lower():
                encontrados.append((id_livro, dados))
        return encontrados

    def buscar_livros_por_autor(self, termo):
        encontrados = []
        for id_livro, dados in self.livros.items():
            if termo.lower() in dados["autor"].lower():
                encontrados.append((id_livro, dados))
        return encontrados

    def buscar_livros_por_categoria(self, termo):
        encontrados = []
        for id_livro, dados in self.livros.items():
            for categoria in dados["categorias"]:
                if termo.lower() in categoria.lower():
                    encontrados.append((id_livro, dados))
                    break
        return encontrados

    def buscar_usuarios_por_nome(self, termo):
        encontrados = []
        for id_usuario, dados in self.usuarios.items():
            if termo.lower() in dados["nome"].lower():
                encontrados.append((id_usuario, dados))
        return encontrados

    def buscar_usuarios_por_cpf(self, termo):
        encontrados = []
        for id_usuario, dados in self.usuarios.items():
            if termo == dados["cpf"]:
                encontrados.append((id_usuario, dados))
        return encontrados

    #==================== Funções de Menu ====================
    # DANIEL EXAME: mudança no visual do menu e opção de mostrar livro por ID 
    def menu_principal(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("""
            ========================================
            |        SISTEMA DE BIBLIOTECA         |
            ========================================
            | 1. Gerenciar Livros                  |
            | 2. Gerenciar Usuários                |
            | 3. Gerenciar Empréstimos             |
            | 4. Relatórios                        |
            | 5. Buscar                            |
            | 6. Sair                              |
            ========================================
            """)
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.menu_livros()
            elif opcao == '2':
                self.menu_usuarios()
            elif opcao == '3':
                self.menu_emprestimos()
            elif opcao == '4':
                self.menu_relatorios()
            elif opcao == '5':
                self.menu_busca()
            elif opcao == '6':
                print("Saindo...")
                break
            else:
                print("Opção inválida. Tente novamente.")
                continuar()

    def menu_livros(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("""
            ========================================
            |         GERENCIAR LIVROS             |
            ========================================
            | 1. Adicionar Livro                   |
            | 2. Mostrar Livros                    |
            | 3. Deletar Livro                     |
            | 4. Navegar Livros                    |
            | 5. Voltar                            |
            ========================================
            """)
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                titulo = input("Título: ")
                autor = input("Autor: ")
                categorias_str = input("Categorias (separadas por vírgula): ")
                categorias = [c.strip() for c in categorias_str.split(',') if c.strip()]
                try:
                    exemplares = int(input("Número de exemplares: "))
                except ValueError:
                    print("Número de exemplares inválido. Deve ser um número inteiro.")
                    continuar()
                    continue
                self.adicionar_livro(titulo, autor, categorias, exemplares)
            elif opcao == '2':
                self.mostrar_livros()
            elif opcao == '3':
                self.deletar_livro()
            elif opcao == '4':
                self.navegar_livros()
            elif opcao == '5':
                break
            else:
                print("Opção inválida. Tente novamente.")
                continuar()

    def menu_usuarios(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("""
            ========================================
            |         GERENCIAR USUÁRIOS           |
            ========================================
            | 1. Cadastrar Usuário                 |
            | 2. Mostrar Usuários                  |
            | 3. Deletar Usuário                   |
            | 4. Voltar                            |
            ========================================
            """)
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                nome = input("Nome: ")
                email = input("Email: ")
                telefone = input("Telefone (somente números): ")
                cpf = input("CPF (somente números): ")
                self.cadastrar_usuario(nome, email, telefone, cpf)
            elif opcao == '2':
                self.mostrar_usuarios()
            elif opcao == '3':
                self.deletar_usuario()
            elif opcao == '4':
                break
            else:
                print("Opção inválida. Tente novamente.")
                continuar()

    def menu_emprestimos(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("""
            ========================================
            |        GERENCIAR EMPRÉSTIMOS         |
            ========================================
            | 1. Emprestar Livro                   |
            | 2. Devolver Livro                    |
            | 3. Adicionar à Fila de Espera        |
            | 4. Desfazer Último Empréstimo        |
            | 5. Voltar                            |
            ========================================
            """)
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                id_usuario = self.selecionar_usuario()
                if id_usuario:
                    id_livro = self.selecionar_livro()
                    if id_livro:
                        self.emprestar_livro(id_usuario, id_livro)
            elif opcao == '2':
                id_usuario = self.selecionar_usuario()
                if id_usuario:
                    id_livro = self.selecionar_livro_para_devolver(id_usuario)
                    if id_livro:
                        self.devolver_livro(id_usuario, id_livro)
            elif opcao == '3':
                id_usuario = self.selecionar_usuario()
                if id_usuario:
                    id_livro = self.selecionar_livro_fila_de_espera()
                    if id_livro:
                        self.adicionar_fila_espera(id_usuario, id_livro)
            elif opcao == '4':
                self.desfazer_emprestimo()
            elif opcao == '5':
                break
            else:
                print("Opção inválida. Tente novamente.")
                continuar()

    def menu_relatorios(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("""
            ========================================
            |           RELATÓRIOS                 |
            ========================================
            | 1. Listar Empréstimos Atuais         |
            | 2. Listar Filas de Espera            |
            | 3. Mostrar Histórico de Ações        |
            | 4. Voltar                            |
            ========================================
            """)
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.listar_emprestimos_atuais()
            elif opcao == '2':
                self.listar_filas_de_espera()
            elif opcao == '3':
                self.mostrar_historico()
            elif opcao == '4':
                break
            else:
                print("Opção inválida. Tente novamente.")
                continuar()

    def menu_busca(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("""
            ========================================
            |             BUSCA                    |
            ========================================
            | 1. Buscar Livros por Título          |
            | 2. Buscar Livros por Autor           |
            | 3. Buscar Livros por Categoria       |
            | 4. Buscar Usuários por Nome          |
            | 5. Buscar Usuários por CPF           |
            | 6. Buscar por livro por ID (DETALHES)|
            | 7. Voltar                            |
            ========================================
            """)
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                termo = input("Digite o título ou parte dele: ")
                resultados = self.buscar_livros_por_titulo(termo)
                if resultados:
                    print("\nLivros encontrados:")
                    for id_livro, dados in resultados:
                        print(f"{id_livro}: {dados['titulo']} ({dados['autor']})")
                else:
                    print("Nenhum livro encontrado com esse título.")
                continuar()
            elif opcao == '2':
                termo = input("Digite o autor ou parte dele: ")
                resultados = self.buscar_livros_por_autor(termo)
                if resultados:
                    print("\nLivros encontrados:")
                    for id_livro, dados in resultados:
                        print(f"{id_livro}: {dados['titulo']} ({dados['autor']})")
                else:
                    print("Nenhum livro encontrado com esse autor.")
                continuar()
            elif opcao == '3':
                termo = input("Digite a categoria ou parte dela: ")
                resultados = self.buscar_livros_por_categoria(termo)
                if resultados:
                    print("\nLivros encontrados:")
                    for id_livro, dados in resultados:
                        print(f"{id_livro}: {dados['titulo']} ({dados['autor']}) - Categorias: {', '.join(dados['categorias'])}")
                else:
                    print("Nenhum livro encontrado nessa categoria.")
                continuar()
            elif opcao == '4':
                termo = input("Digite o nome do usuário ou parte dele: ")
                resultados = self.buscar_usuarios_por_nome(termo)
                if resultados:
                    print("\nUsuários encontrados:")
                    for id_usuario, dados in resultados:
                        print(f"{id_usuario}: {dados['nome']} (CPF: {dados['cpf']})")
                else:
                    print("Nenhum usuário encontrado com esse nome.")
                continuar()
            elif opcao == '5':
                termo = input("Digite o CPF do usuário: ")
                resultados = self.buscar_usuarios_por_cpf(termo)
                if resultados:
                    print("\nUsuários encontrados:")
                    for id_usuario, dados in resultados:
                        print(f"{id_usuario}: {dados['nome']} (CPF: {dados['cpf']})")
                else:
                    print("Nenhum usuário encontrado com esse CPF.")
                continuar()
            elif opcao == '6':  
                try:
                    livro_id = int(input("Digite o ID do livro: "))
                    detalhes = self.obter_detalhes_livro_tupla(livro_id)
                    if detalhes:
                        titulo, autor, exemplares = detalhes
                        print(f"\nDetalhes do Livro ID {livro_id}:")
                        print(f"Título: {titulo}")
                        print(f"Autor: {autor}")
                        print(f"Exemplares: {exemplares}")
                    else:
                        print("Livro não encontrado.")
                except ValueError:
                    print("ID inválido. Digite um número inteiro.")
                continuar()

            elif opcao == '7':
                break

            else:
                print("Opção inválida. Tente novamente.")
                continuar()

if __name__ == "__main__":
    cli = BibliotecaCLI()
    cli.menu_principal()