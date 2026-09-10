import grpc
import tarefa_pb2
import tarefa_pb2_grpc

# Substituir "localhost" pelo ip do server
canal = grpc.insecure_channel("localhost:50051")
stub = tarefa_pb2_grpc.GerenciarTarefasStub(canal)

while(True):
    print("--------------- Gerenciador de Tarefas ---------------")
    print("1. Criar Tarefa")
    print("2. Listar Tarefas")
    print("3. Atualizar Tarefa")
    print("4. Remover Tarefa")
    print("0. Sair")
    print("Selecione a operação que deseja fazer:")
    op = input()
    print()
    if op == "1":
        print("Digite o nome da sua tarefa:")
        nomeT = input()
        print("Digite a descrição da sua tarefa:")
        descricaT = input()
        print("Digite a data de entrega(dd/mm/aa):")
        dataT = input()
        print("Status: 0. Pendente  | 1. Em Andamento  | 2. Concluida")
        statusT = int(input())
        print("Digite os participantes: ")
        participantesT = input()
        participantesT = participantesT.split(", ")
        print()
        
        criarRequest = tarefa_pb2.CriarTarefaRequest(
            nome = nomeT,
            descricao = descricaT,
            data_limite= dataT,
            status= statusT,
            responsaveis= participantesT
        )

        resposta = stub.CriarTarefa(criarRequest)
        print(resposta)
        print()

    elif op == "2": 
        resposta = stub.ListarTarefas(tarefa_pb2.ListaRequest())
        print(resposta)
        print()

    elif op == "3":
        print("Digite o id de sua tarefa:")
        idT = input()
        print("Digite o nome da sua tarefa:")
        nomeT = input()
        print("Digite a descrição da sua tarefa:")
        descricaT = input()
        print("Digite a data de entrega(dd/mm/aa):")
        dataT = input()
        print("Status: 0. Pendente  | 1. Em Andamento  | 2. Concluida")
        statusT = int(input())
        print("Digite os participantes: ")
        participantesT = input()
        participantesT = participantesT.split(", ")
        print()

        attRequest = tarefa_pb2.Tarefa(
            id = idT,
            nome = nomeT,
            descricao = descricaT,
            data_limite= dataT,
            status= statusT,
            responsaveis= participantesT
        )

        resposta = stub.AtualizarTarefa(attRequest)
        print(resposta.mensagem)
        print()

    elif op == "4":
        print("Digite o id de sua tarefa:")
        idT = input()
        print()
        
        remRequest = tarefa_pb2.RemoverRequest(id = idT)
        resposta = stub.RemoverTarefa(remRequest)
        print(resposta.mensagem)
        print()

    elif op == "0":
        print("Até a próxima :D")
        print()
        break

    else:
        print("Opção Inváida")
        print()

