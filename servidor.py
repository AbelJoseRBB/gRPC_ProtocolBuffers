import grpc
import tarefa_pb2_grpc
import tarefa_pb2
from concurrent import futures
import uuid
import os
import json
from google.protobuf.json_format import MessageToDict, ParseDict


#ATT = aqui é a pasta pra salvar cada tarefa em arquivo diferente
pastaTarefas = "Banco de Tarefas"
if not os.path.exists(pastaTarefas):
    os.makedirs(pastaTarefas)

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

        #salvando a tarefa em arquivo JOISON
        caminho_arquivo = os.path.join(pastaTarefas, f"{novo_id}.json")
        with open(caminho_arquivo, "w", encoding="utf-8") as f: #w de write
            json.dump(MessageToDict(tarefa, always_print_fields_with_no_presence=True), f, indent=4)

        print(f"Tarefa criada e salva: {novo_id}.json")

        return tarefa

    def ListarTarefas(self, request, context):

        resposta = tarefa_pb2.ListaReply()

        if os.path.exists(pastaTarefas):
            for arquivo in os.listdir(pastaTarefas):
                if arquivo.endswith(".json"):
                    caminho = os.path.join(pastaTarefas, arquivo)
                    with open(caminho, "r", encoding="utf-8") as f: #r de read
                        dados_json = json.load(f)
                        tarefa = tarefa_pb2.Tarefa()
                        ParseDict(dados_json, tarefa)
                        resposta.tarefas.append(tarefa)

        print(f"Listando {len(resposta.tarefas)} tarefa(s).")
        return resposta

    def AtualizarTarefa(self, request, context):
        caminho_arquivo = os.path.join(pastaTarefas, f"{request.id}.json")
        
        if not os.path.exists(caminho_arquivo):
            return tarefa_pb2.AtualizacaoReply(status= False, mensagem = "Tarefa não encontrada" )
        
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(MessageToDict(request, always_print_fields_with_no_presence=True), f, indent=4)
            
        print(f"Tarefa atualizada: {request.id}.json")
        return tarefa_pb2.AtualizacaoReply(
            status=True,
            mensagem="Tarefa atualizada",
            tarefa=request
        )

    def RemoverTarefa(self, request, context):
        caminho_arquivo = os.path.join(pastaTarefas, f"{request.id}.json")
        if not os.path.exists(caminho_arquivo):
            return tarefa_pb2.RemoverReply(status = False, mensagem = "Tarefa não encontrada")

        os.remove(caminho_arquivo)

        print("Tarefa removida")
        return tarefa_pb2.RemoverReply(status = True, mensagem = "Tarefa removida")

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
    