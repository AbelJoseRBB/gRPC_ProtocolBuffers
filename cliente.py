import grpc
import tarefa_pb2
import tarefa_pb2_grpc

# arquivo criado atualmente so para teste 
# implementar cliente interativo e persistencia em arquivos

canal = grpc.insecure_channel("localhost:50051")
stub = tarefa_pb2_grpc.GerenciarTarefasStub(canal)
request = tarefa_pb2.CriarTarefaRequest(
    nome="Estudar gRPC",
    descricao="Finalizar atividade de Sistemas Distribuidos",
    data_limite="10/09/2026",
    status=tarefa_pb2.PENDENTE,
    responsaveis=["Abel gay"]
)

resposta = stub.CriarTarefa(request)
print("Tarefa criada\n")

# testandoooooooooo
print("Buscando todas as tarefas salvas no servidor:")
resposta = stub.ListarTarefas(tarefa_pb2.ListaRequest())

print("\n--- LISTA DE TAREFAS NO SERVIDOR---")

print(resposta)