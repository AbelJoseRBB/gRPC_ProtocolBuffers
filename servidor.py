import grpc
import tarefa_pb2_grpc
import tarefa_pb2
from concurrent import futures
import uuid

class GerenciadorTarefas(tarefa_pb2_grpc.GerenciarTarefasServicer):
    def CriarTarefa(self, request, context):
        
        novo_id = str(uuid.uuid4())

        tarefa = tarefa_pb2.Tarefa(
            id= novo_id, 
            nome = request.nome, 
            descricao = request.descricao, 
            data_limite = request.data_limite, 
            status = request.status, 
            responsaveis = request.responsaveis
        )
        
        return tarefa
        

def iniciarServer():
    # define o numero maximo de threads a serem usadas
    tp = futures.ThreadPoolExecutor(max_workers = 10)
    servidor = grpc.server(thread_pool = tp)

    # registra o gerenciador no servidor 
    gerenciador = GerenciadorTarefas()
    tarefa_pb2_grpc.add_GerenciarTarefasServicer_to_server(gerenciador, servidor)

    # configura o servidor na porta 50051
    servidor.add_insecure_port("[::]:50051")
    servidor.start()
    servidor.wait_for_termination()

if __name__ == "__main__":
    iniciarServer()
    