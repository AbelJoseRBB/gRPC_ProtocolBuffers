# Gerenciador de Tarefas com gRPC e Protocol Buffers

Sistema distribuído de gerenciamento de tarefas desenvolvido em **Python**, utilizando **gRPC** para comunicação entre cliente e servidor e **Protocol Buffers** para definição e serialização das mensagens.

O sistema segue uma arquitetura **cliente-servidor**, na qual um servidor central é responsável pelo gerenciamento e persistência das tarefas, enquanto múltiplos clientes podem realizar operações remotamente.

## Funcionalidades

O sistema disponibiliza quatro operações principais:

- **Criar tarefa** — cria uma nova tarefa e gera automaticamente um identificador único (UUID).
- **Listar tarefas** — retorna todas as tarefas armazenadas no servidor.
- **Atualizar tarefa** — atualiza os dados de uma tarefa existente a partir de seu ID.
- **Remover tarefa** — remove uma tarefa armazenada a partir de seu ID.

Cada tarefa possui:

- ID
- Nome
- Descrição
- Data limite
- Status
- Um ou mais responsáveis

Os status disponíveis são:

- `PENDENTE`
- `EM_ANDAMENTO`
- `CONCLUIDO`

---

## Arquitetura

A aplicação utiliza uma arquitetura cliente-servidor:


```text
Cliente 1 ─────┐
               │
               │ gRPC / Protocol Buffers
               ▼
        ┌──────────────┐
        │   Servidor   │
        │    gRPC      │
        └──────┬───────┘
               │
               │ Persistência
               ▼
       Banco de Tarefas/
          ├── <uuid>.json
          ├── <uuid>.json
          └── ...
               ▲
               │
               │ gRPC / Protocol Buffers
Cliente 2 ─────┘
```
O **servidor** concentra a lógica e a persistência dos dados. Os clientes não possuem bancos de tarefas próprios: todas as operações são enviadas ao servidor através de chamadas RPC.

Isso permite que diferentes clientes compartilhem o mesmo estado. 

---

## gRPC e Protocol Buffers

O contrato de comunicação entre cliente e servidor é definido no arquivo:

```text
tarefa.proto
```

Nele são especificadas as mensagens utilizadas pelo sistema e os métodos RPC disponíveis.

O serviço principal é:

```proto
service GerenciarTarefas {
    rpc CriarTarefa(CriarTarefaRequest) returns (Tarefa);
    rpc ListarTarefas(ListaRequest) returns (ListaReply);
    rpc AtualizarTarefa(Tarefa) returns (AtualizacaoReply);
    rpc RemoverTarefa(RemoverRequest) returns (RemoverReply);
}
```

Neste projeto são utilizados **RPCs unários (Unary RPC)**, ou seja, cada chamada envia uma requisição e recebe uma resposta.

O Protocol Buffers é responsável pela definição estruturada e serialização das mensagens utilizadas pelo gRPC durante a comunicação.

> **Observação:** JSON é utilizado somente para a persistência das tarefas no servidor. A comunicação entre clientes e servidor é realizada através de gRPC e Protocol Buffers.

---

## Estrutura do projeto

```text
gRPC_ProtocolBuffers/
│
├── cliente.py
├── servidor.py
├── tarefa.proto
├── tarefa_pb2.py
├── tarefa_pb2_grpc.py
├── requirements.txt
├── .gitignore
│
└── Banco de Tarefas/
    └── <uuid>.json
```

### Principais arquivos

**`tarefa.proto`**  
Define as mensagens, tipos, enumerações e serviços RPC utilizados pelo sistema.

**`tarefa_pb2.py`**  
Arquivo gerado automaticamente pelo compilador do Protocol Buffers contendo as classes das mensagens.

**`tarefa_pb2_grpc.py`**  
Arquivo gerado automaticamente contendo as estruturas utilizadas pelo gRPC, como `Servicer` e `Stub`.

**`servidor.py`**  
Implementa os métodos definidos no serviço gRPC, além de realizar a persistência das tarefas.

**`cliente.py`**  
Interface de linha de comando utilizada para realizar chamadas RPC ao servidor.

**`Banco de Tarefas/`**  
Diretório criado automaticamente pelo servidor para persistência. Cada tarefa é armazenada em um arquivo JSON independente.

> Os arquivos `tarefa_pb2.py` e `tarefa_pb2_grpc.py` são gerados automaticamente e não devem ser alterados manualmente.

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd gRPC_ProtocolBuffers
```

### 2. Crie um ambiente virtual

No Windows Powershell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Caso necessário, as principais dependências podem ser instaladas diretamente:

```bash
pip install grpcio grpcio-tools protobuf
```

---

##  Compilando o arquivo `.proto`

Após criar ou modificar `tarefa.proto`, gere novamente os arquivos Python:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tarefa.proto
```

Esse comando gera:

```text
tarefa_pb2.py
tarefa_pb2_grpc.py
```

Sempre recompile o `.proto` caso seu contrato de comunicação seja alterado.

---

##  Executando o sistema

### Servidor

Na máquina responsável pelo servidor:

```bash
python servidor.py
```

Por padrão, o servidor utiliza a porta: `50051`

O servidor permanece aguardando requisições dos clientes.

### Cliente local

Para executar cliente e servidor na mesma máquina, em outro terminal, execute:

```bash
python cliente.py
```

O menu permite selecionar as operações disponíveis:

```text
--------------- Gerenciador de Tarefas ---------------

1. Criar Tarefa
2. Listar Tarefas
3. Atualizar Tarefa
4. Remover Tarefa
0. Sair
```

---

##  Executando em máquinas diferentes

O sistema também permite que clientes sejam executados em computadores diferentes do servidor.

Primeiro, descubra o endereço IPv4 da máquina que executará o servidor.

Por exemplo:

```text
IPv4: 192.168.0.10
```

No arquivo `cliente.py`, substitua `"localhost"` pelo endereço IP do servidor:

```python
canal = grpc.insecure_channel("192.168.0.10:50051")
```

A arquitetura passa a ser:

```text
     Servidor
192.168.0.10:50051
        ▲
        │
   ┌────┴────┐
   │         │
Cliente 1   Cliente 2
```

As máquinas devem possuir conectividade de rede entre si e a porta `50051` deve estar acessível.

Caso a conexão seja bloqueada, verifique as configurações de firewall da máquina servidor.

---


## 🔁 Fluxo de uma requisição

Exemplo da criação de uma tarefa:

```text
1. Cliente cria uma CriarTarefaRequest
                    │
                    ▼
2. Stub realiza CriarTarefa(request)
                    │
                    ▼
3. Protocol Buffers serializa a mensagem
                    │
                    ▼
4. gRPC envia a requisição pela rede
                    │
                    ▼
5. Servidor recebe e desserializa a mensagem
                    │
                    ▼
6. Servidor gera um UUID
                    │
                    ▼
7. Tarefa é persistida em JSON
                    │
                    ▼
8. Servidor retorna uma Tarefa
                    │
                    ▼
9. Cliente recebe a resposta
```

---

## Tecnologias utilizadas

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white) &nbsp;&nbsp;&nbsp; ![gRPC](https://img.shields.io/badge/gRPC-Protocol-244c5a?logo=google&logoColor=white) &nbsp;&nbsp;&nbsp; ![Protocol Buffers](https://img.shields.io/badge/Protocol%20Buffers-Protobuf-blue) &nbsp;&nbsp;&nbsp; ![JSON](https://img.shields.io/badge/JSON-Persistência-black?logo=json) &nbsp;&nbsp;&nbsp; ![Git](https://img.shields.io/badge/Git-Versionamento-orange?logo=git&logoColor=white)

---

## Autores

- Abel José Rocha Barros Bezerra
- Wendell Moura Leite
- Guilherme Miller Gama Cardoso
- Victor Henrick Santos Andrade 
